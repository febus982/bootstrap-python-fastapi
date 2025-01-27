import hashlib
import importlib
import logging
import sys
from asyncio import get_event_loop
from datetime import datetime, timezone
from os import listdir, path
from os.path import isfile, join

from sqlalchemy import Table, Column, String, DateTime, UniqueConstraint, text, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import registry, sessionmaker, Mapped, mapped_column

from alembic import context
from common.bootstrap import application_init
from common.config import AppConfig

USE_TWOPHASE = False


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# gather section names referring to different
# databases.  These are named "engine1", "engine2"
# in the sample .ini file.
# db_names = config.get_main_option("databases")

di_container = application_init(AppConfig()).di_container
logger = logging.getLogger("alembic.env")
sa_manager = di_container.SQLAlchemyBindManager()

target_metadata = sa_manager.get_bind_mappers_metadata()
db_names = target_metadata.keys()
config.set_main_option("databases", ",".join(db_names))

def generate_fixture_migration_model(declarative_base: type):
    class FixtureMigration(declarative_base):
        __tablename__ = "alembic_fixtures"

        bind: Mapped[str] = mapped_column(String(), primary_key=True)
        filename: Mapped[str] = mapped_column(String(), primary_key=True)
        signature: Mapped[str] = mapped_column(String(), nullable=False)
        processed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now)
    return FixtureMigration

fixture_migration_models = {}
for name in db_names:
    fixture_migration_models[name] = generate_fixture_migration_model(
        sa_manager.get_bind(name).declarative_base
    )


# add your model's MetaData objects here
# for 'autogenerate' support.  These must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a "copy" of
# a MetaData is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# }


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        hasher.update(file.read())
    return hasher.hexdigest()

async def a_migrate_fixtures(bind_name: str, Session: async_sessionmaker[AsyncSession]) -> str:
    alembic_path = path.dirname(path.realpath(__file__))
    fixtures_path = alembic_path + "/fixtures"
    sys.path.append(alembic_path)
    module_names = [
        f[:-3] for f in listdir(fixtures_path)
        if isfile(join(fixtures_path, f))
        and f.endswith(".py")
        and f != "__init__.py"
    ]
    async with Session() as session:
        for module_name in module_names:
            logging.debug(f"Creating {module_name} fixtures for {bind_name}")
            m = importlib.import_module(f"fixtures.{module_name}")
            fixture_migration = await session.get(
                fixture_migration_models[bind_name],
                (bind_name, f"{module_name}.py")
            )
            signature = calculate_md5(f"{fixtures_path}/{module_name}.py")
            if fixture_migration:
                if signature != fixture_migration.signature:
                    logging.warning(f"Signature mismatch for {fixture_migration.filename} fixture. The file has been modified after being processed.")
                logging.debug(f"{module_name} fixtures already migrated for {bind_name}")
                continue

            session.add_all(m.fixtures().get(bind_name, []))
            session.add(fixture_migration_models[bind_name](
                bind=bind_name,
                filename=f"{module_name}.py",
                signature=signature,
            ))
            try:
                await session.commit()
                logging.info(f"{module_name} fixtures correctly created for {bind_name}")
            except:
                await session.rollback()
                logging.error(f"{module_name} fixtures failed to apply to {bind_name}")



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines = {}
    for name in db_names:
        engines[name] = {}
        engines[name]["url"] = sa_manager.get_bind(name).engine.url

    for name, rec in engines.items():
        logger.info(f"Migrating database {name}")
        file_ = f"{name}.sql"
        logger.info(f"Writing output to {file_}")
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=target_metadata.get(name),
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def do_run_migration(conn, name):
    context.configure(
        connection=conn,
        upgrade_token=f"{name}_upgrades",
        downgrade_token=f"{name}_downgrades",
        target_metadata=target_metadata.get(name),
    )
    context.run_migrations(engine_name=name)


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines = {}
    for name in db_names:
        engines[name] = {}
        engines[name]["engine"] = sa_manager.get_bind(name).engine

    for name, rec in engines.items():
        engine = rec["engine"]
        if isinstance(engine, AsyncEngine):
            rec["connection"] = conn = await engine.connect()

            if USE_TWOPHASE:
                rec["transaction"] = await conn.begin_twophase()
            else:
                rec["transaction"] = await conn.begin()
        else:
            rec["connection"] = conn = engine.connect()

            if USE_TWOPHASE:
                rec["transaction"] = conn.begin_twophase()
            else:
                rec["transaction"] = conn.begin()

    try:
        for name, rec in engines.items():
            logger.info(f"Migrating database {name}")
            if isinstance(rec["engine"], AsyncEngine):
                def migration_callable(*args, **kwargs):
                    return do_run_migration(*args, name=name, **kwargs)

                await rec["connection"].run_sync(migration_callable)
                Session = async_sessionmaker(bind=rec["connection"])
                await a_migrate_fixtures(bind_name=name, Session=Session)

            else:
                do_run_migration(rec["connection"], name)
                # Session = sessionmaker(bind=rec["connection"])
                # session = Session()

        if USE_TWOPHASE:
            for rec in engines.values():
                if isinstance(rec["engine"], AsyncEngine):
                    await rec["transaction"].prepare()
                else:
                    rec["transaction"].prepare()

        for rec in engines.values():
            if isinstance(rec["engine"], AsyncEngine):
                await rec["transaction"].commit()
            else:
                rec["transaction"].commit()
    except:
        for rec in engines.values():
            if isinstance(rec["engine"], AsyncEngine):
                await rec["transaction"].rollback()
            else:
                rec["transaction"].rollback()
        raise
    finally:
        for rec in engines.values():
            if isinstance(rec["engine"], AsyncEngine):
                await rec["connection"].close()
            else:
                rec["connection"].close()


background_tasks = set()

if context.is_offline_mode():
    run_migrations_offline()
else:
    loop = get_event_loop()
    if loop.is_running():
        task = loop.create_task(run_migrations_online())
        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)

        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)
    else:
        loop.run_until_complete(run_migrations_online())
