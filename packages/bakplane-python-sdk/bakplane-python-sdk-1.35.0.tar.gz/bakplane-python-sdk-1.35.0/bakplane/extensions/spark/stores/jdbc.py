import random
import typing
import urllib.parse
import tempfile

from datetime import datetime
from timeit import default_timer as timer

from sqlalchemy import Column, Table, MetaData, create_engine, DateTime

from bakplane.bakplane_pb2 import (
    ResolveResourcePathResponse,
    ResolveResourceIntentResponse,
    ComparisonType,
)
from bakplane.extensions.base import (
    WriteResponse,
    WriteRequest,
    ReadResponse,
    ReadAllRequest,
    ReadRequest,
    ReadRequestBuildingBlocks,
    DataStoreHelper,
    INFINITY_PROXY_DATE
)
from bakplane.extensions.spark.utils import (
    to_spark_save_mode,
    timestamp_to_date_string,
    datetime_to_date_string,
)
from bakplane.utils import to_execution_statistics


class JDBCStoreHelper(DataStoreHelper):
    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            port: int,
            database: str,
            schema_name: str,
            driver: str,
            table_prefixes: typing.List[str] = None
    ):
        self.metadata = MetaData()
        self.engine = create_engine(
            f"{driver}://{user}:{password}@{host}:{port}/{database}",
            executemany_values_page_size=10000,
            executemany_batch_page_size=500,
            executemany_mode='batch',
        )
        self.schema_name = schema_name
        self.table_prefixes = table_prefixes

    def create_temporary_table(
            self,
            prefix: str,
            columns: typing.List[Column],
            rows: typing.List[typing.Dict[str, typing.Any]],
    ) -> Table:

        for c in columns:
            c.table = None

        tbl = Table(
            prefix
            + "_"
            + str(int(datetime.utcnow().timestamp()))
            + "_"
            + str(random.randint(1, 1000)),
            self.metadata,
            *columns,
            schema=self.schema_name,
        )

        tbl.create(bind=self.engine)
        self.engine.execute(tbl.insert(), rows)

        return tbl


def __build_read_all_query(
        r: ReadAllRequest, res: ResolveResourcePathResponse
) -> str:
    return f'select {", ".join(r.columns)} from {res.context["schema_name"]}.{res.context["table_name"]}'


def __add_effective_dating_constraint(blocks: ReadRequestBuildingBlocks, res: ResolveResourceIntentResponse, r: ReadRequest):
    a = blocks.asset_table

    if r.effective_dating is None:
        return



    if blocks.effective_dating_table is not None:
        blocks.constraints.append(
            blocks.effective_dating_table.c.dt >= a.c.effective_start_dt
        )

        blocks.constraints.append(
            blocks.effective_dating_table.c.dt < a.c.effective_end_dt
        )
    else:
        blocks.constraints.append(
            a.c.effective_start_dt
            <= timestamp_to_date_string(
                res.effective_dating.end_dt.seconds
            )
        )
        blocks.constraints.append(
            a.c.effective_end_dt
            >= timestamp_to_date_string(
                res.effective_dating.start_dt.seconds
            )
        )


def __add_valid_dating_constraint(blocks: ReadRequestBuildingBlocks, res: ResolveResourceIntentResponse):
    a = blocks.asset_table

    if blocks.valid_dating_table is not None:
        blocks.constraints.append(
            blocks.valid_dating_table.c.dt >= a.c.valid_start_dt
        )

        blocks.constraints.append(
            blocks.valid_dating_table.c.dt < a.c.valid_end_dt
        )


def __populate_building_blocks_effective_dating(helper: DataStoreHelper, blocks: ReadRequestBuildingBlocks, r: ReadRequest):

    if r.effective_dating is None:
        return

    if isinstance(r.effective_dating, list):
        blocks.effective_dating_table = helper.create_temporary_table('t_dating', [Column('dt', DateTime, nullable=False)], [{'dt': x} for x in r.get_resolved_effective_dating()])
    elif isinstance(r.effective_dating, tuple):
        start, end = r.effective_dating

        blocks.effective_start_dt = start
        blocks.effective_end_dt = end
    elif isinstance(r.effective_dating, datetime):
        blocks.effective_start_dt = r.effective_dating
        blocks.effective_end_dt = INFINITY_PROXY_DATE
    else:
        raise ValueError('Effective dating has unknown type.')


def __populate_building_blocks_valid_dating(helper: DataStoreHelper, blocks: ReadRequestBuildingBlocks, r: ReadRequest):

    if r.valid_dating is None:
        return

    if isinstance(r.valid_dating, list):
        blocks.valid_dating_table = helper.create_temporary_table('t_dating', [Column('dt', DateTime, nullable=False)], [{'dt': x} for x in r.get_resolved_valid_dating()])
    elif isinstance(r.valid_dating, tuple):
        start, end = r.valid_dating

        blocks.valid_start_dt = start
        blocks.valid_end_dt = end

    elif isinstance(r.valid_dating, datetime):
        blocks.valid_start_dt = r.valid_dating
        blocks.valid_end_dt = INFINITY_PROXY_DATE
    else:
        raise ValueError('Valid dating has unknown type.')


def __build_read_query(
        r: ReadRequest,
        res: ResolveResourceIntentResponse,
        dialect,
        store_helper: DataStoreHelper,
) -> str:
    from sqlalchemy import (
        Table,
        MetaData,
        Column,
        select,
        and_,
    )

    metadata: MetaData = MetaData()

    src_tbl: Table = Table(
        res.table_name,
        metadata,
        *[Column(x.name) for x in res.columns],
        schema=res.schema_name,
    )

    mapping_tbl: Table = Table(
        res.mapping.table_name,
        metadata,
        *[Column(x.name) for x in res.mapping.columns],
        schema=res.mapping.schema_name,
    )

    a = src_tbl.alias("a")

    mapping_columns = []
    for column in res.mapping.columns:
        if not column.is_effective_dating:
            mapping_columns.append(
                mapping_tbl.c.get(column.name).label(column.name)
            )

    m = mapping_tbl.alias("m")
    clauses = []
    for clause in res.mapping.clauses:
        if clause.comparison == ComparisonType.EQ:
            clauses.append(
                m.c.get(clause.mapping_field_name)
                == a.c.get(clause.resource_field_name)
            )

    blocks = ReadRequestBuildingBlocks(
        mapping_table=m,
        asset_table=a,
        selectable=m.join(a, and_(*clauses)),
        knowledge_dt=r.knowledge_dt,
        constraints=[and_(*[
            datetime_to_date_string(r.knowledge_dt) >= a.c.knowledge_start_dt,
            datetime_to_date_string(r.knowledge_dt) < a.c.knowledge_end_dt,
        ])],
    )

    __populate_building_blocks_effective_dating(store_helper, blocks, r)
    __populate_building_blocks_valid_dating(store_helper, blocks, r)

    if (r.columns is None or len(r.columns) <= 0) and r.query_builder is None:
        raise RuntimeError("You must provide a set of columns.")

    if r.query_builder:
        res = r.query_builder(blocks)
    else:
        blocks.columns = [a.c.get(x) for x in r.columns if x in a.c]

        if r.additional_constraints is not None:
            blocks.constraints.append(r.additional_constraints(blocks))

        if r.effective_dating is not None:
            blocks.constraints.append(
                a.c.effective_start_dt <= blocks.mapping_table.c.effective_end_dt
            )

            blocks.constraints.append(
                a.c.effective_end_dt >= blocks.mapping_table.c.effective_start_dt
            )
        else:
            blocks.constraints.append(
                a.c.valid_start_dt <= blocks.mapping_table.c.effective_end_dt
            )

            blocks.constraints.append(
                a.c.valid_end_dt >= blocks.mapping_table.c.effective_start_dt
            )

        __add_valid_dating_constraint(blocks, res)

        if r.effective_dating_hint is None:
            __add_effective_dating_constraint(blocks, res, r)

        else:
            if isinstance(r.effective_dating_hint, tuple):
                s = datetime_to_date_string(
                    typing.cast(datetime, r.effective_dating_hint[0])
                )
                e = datetime_to_date_string(
                    typing.cast(datetime, r.effective_dating_hint[1])
                )

                blocks.constraints.append(a.c.effective_start_dt <= e)
                blocks.constraints.append(a.c.effective_end_dt >= s)
            elif isinstance(r.effective_dating_hint, str):
                col = typing.cast(str, r.effective_dating_hint)

                s = col + "_start_dt"
                e = col + "_end_dt"

                blocks.constraints.append(a.c.effective_start_dt <= m.c.get(e))
                blocks.constraints.append(a.c.effective_end_dt >= m.c.get(s))
            else:
                raise RuntimeError("Invalid type for effective_dating_hint.")

        if r.modifiers:
            for m in r.modifiers:
                blocks = m.execute(blocks, store_helper)

        res = (
            select(blocks.columns)
                .select_from(blocks.selectable)
                .where(and_(*blocks.constraints))
        )

    query = str(
        res.compile(dialect=dialect, compile_kwargs={"literal_binds": True}, )
    )

    return query


def write_fn(
        r: WriteRequest, res: ResolveResourcePathResponse, driver: str, url: str
) -> WriteResponse:
    start = timer()

    r.df.write.format("jdbc").mode(to_spark_save_mode(r.mode)).option(
        "driver", driver
    ).option("url", url).option(
        "dbtable", f"{res.context['schema_name']}.{res.context['table_name']}"
    ).option(
        "user", res.context["username"]
    ).option(
        "password", urllib.parse.unquote(res.context["password"])
    ).save()

    end = timer()

    return WriteResponse(
        execution_statistics=to_execution_statistics(start, end)
    )


def __read_query(
        spark, url: str, driver: str, query: str, user: str, password: str
):
    start = timer()

    df = (
        spark.read.format("jdbc")
            .option("url", url)
            .option("query", query)
            .option("user", user)
            .option("password", urllib.parse.unquote(password))
            .option("driver", driver)
            .load()
    )

    end = timer()

    return ReadResponse(
        df=df,
        execution_statistics=to_execution_statistics(start, end),
        context={"query": query, },
    )


def read_all_fn(
        ctx: typing.Any,
        r: ReadAllRequest,
        res: ResolveResourcePathResponse,
        url: str,
        driver: str,
) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_all_query(r, res),
        user=res.context["username"],
        password=res.context["password"],
    )


def read_fn(
        ctx: typing.Any,
        r: ReadRequest,
        res: ResolveResourceIntentResponse,
        dialect,
        url: str,
        driver: str,
        store_helper: DataStoreHelper,
) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_query(r, res, dialect, store_helper),
        user=res.context["username"],
        password=res.context["password"],
    )
