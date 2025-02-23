import hashlib
import importlib
import logging
import sys
from asyncio import get_event_loop
from datetime import datetime
from os import listdir, path
from os.path import isfile, join
from types import ModuleType
from typing import List, Union

from alembic import context
from sqlalchemy import DateTime, String
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker

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

        bind: Mapped[str] = mapped_column(String(255), primary_key=True)
        module_name: Mapped[str] = mapped_column(String(255), primary_key=True)
        signature: Mapped[str] = mapped_column(String(255), nullable=False)
        alembic_head_revisions: Mapped[str] = mapped_column(
            String(255), nullable=False, default=str(context.get_head_revision())
        )

        processed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now)

    return FixtureMigration


fixture_migration_models = {}
for name in db_names:
    fixture_migration_models[name] = generate_fixture_migration_model(sa_manager.get_bind(name).declarative_base)


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


class FixtureHandler:
    alembic_path = path.dirname(path.realpath(__file__))
    fixtures_path = alembic_path + "/fixtures"
    logger = logging.getLogger("alembic.runtime.fixtures")

    @classmethod
    def _calculate_signature(cls, fixture_module: ModuleType) -> str:
        """
        Calculate the SHA-256 signature for a fixture module's corresponding file.

        This method computes a unique hash for the content of a specific Python source
        file associated with a given fixture module. The hash is calculated using the
        SHA-256 algorithm, ensuring a consistent and secure checksum.

        Args:
            fixture_module (ModuleType): The module whose associated file's signature
                needs to be calculated.

        Returns:
            str: The hexadecimal SHA-256 hash of the file content.
        """
        file_path = f"{cls.fixtures_path}/{fixture_module.__name__[9:]}.py"
        hasher = hashlib.sha256()
        with open(file_path, "rb") as file:
            hasher.update(file.read())
        return hasher.hexdigest()

    @classmethod
    def _get_fixture_modules(cls) -> List[ModuleType]:
        """
        This private class method is responsible for retrieving modules from the fixtures
        directory defined by the class attributes. It dynamically imports Python modules
        located in the specified fixtures directory and filters out non-Python files
        or the __init__.py file. It adds the Alembic path to the system path to ensure
        successful imports.

        Parameters
        ----------
        None

        Returns
        -------
        List[ModuleType]
            A list of imported module objects dynamically loaded from the fixtures
            directory.
        """
        sys.path.append(cls.alembic_path)
        return [
            importlib.import_module(f"fixtures.{f[:-3]}")
            for f in listdir(cls.fixtures_path)
            if isfile(join(cls.fixtures_path, f)) and f.endswith(".py") and f != "__init__.py"
        ]

    @classmethod
    def _fixture_already_migrated(cls, fixture_migration, signature) -> bool:
        """
        Determines if a fixture has already been migrated based on the given fixture
        migration and its signature.

        The method examines the provided fixture migration data and its signature to
        decide whether the fixture has already been processed. If the signatures do not
        match, a warning is logged to indicate potential modifications. Otherwise, a debug
        message is logged to confirm prior processing. The return value indicates whether
        the fixture should be skipped.

        Args:
        fixture_migration (FixtureMigration | None): An object representing the migration
            details of a fixture. Can be None.
        signature (str): A unique string indicating the signature of the current fixture.

        Returns:
        bool: True if the fixture has already been migrated and should not be processed
            again; False otherwise.
        """
        if fixture_migration:
            if signature != fixture_migration.signature:
                cls.logger.warning(
                    f"Signature mismatch for `{fixture_migration.module_name}` fixture."
                    f" The file has been already processed but has been modified"
                    f" since then. It will not be processed again."
                )
            else:
                cls.logger.debug(
                    f"`{fixture_migration.module_name}` fixtures already processed for `{fixture_migration.bind}` bind"
                )
            return True
        return False

    @classmethod
    def _add_fixture_data_to_session(
        cls,
        bind_name: str,
        fixture_module: ModuleType,
        session: Union[Session, AsyncSession],
        signature: str,
    ):
        """
        Adds fixture data and migration model to the given session.

        This method interacts with the database session to add predefined fixture data
        and creates a corresponding migration model for tracking purposes. The fixture
        data is retrieved from the specified fixture module, based on the provided bind
        name. The migration model contains metadata about the fixture module and its
        signature.

        Args:
            bind_name (str): The binding name used to fetch fixture data from the
                fixture module.
            fixture_module (ModuleType): The module containing fixture data and fixture
                metadata definitions.
            session (Union[Session, AsyncSession]): A database session where fixture
                data and migration models are added.
            signature (str): A unique signature representing the state of the fixture
                module.

        Returns:
            None
        """
        session.add_all(fixture_module.fixtures.get(bind_name, []))
        session.add(
            fixture_migration_models[bind_name](
                bind=bind_name,
                module_name=f"{fixture_module.__name__}",
                signature=signature,
            )
        )

    @classmethod
    async def a_migrate_fixtures(cls, bind_name: str, session: async_sessionmaker[AsyncSession]):
        """
        Perform asynchronous migration of fixture data modules for a specific database bind.

        This method iterates over fixture data modules, calculates their signatures, and determines
        whether fixtures have already been migrated for a specific database bind. If not, it migrates
        them by adding the data to the session and commits the changes. If an error occurs during
        the commit, it rolls back the session. Logs are produced at each significant step.

        Args:
            bind_name: The name of the database bind for which the fixtures are being migrated.
            session: An instance of `async_sessionmaker[AsyncSession]` used for interacting with
                     the database.

        Raises:
            Exception: If a commit to the database fails.

        Returns:
            None
        """
        modules = cls._get_fixture_modules()
        async with session() as session:
            for fixture_module in modules:
                cls.logger.debug(f"Creating `{fixture_module.__name__}` fixtures for `{bind_name}` bind")
                fixture_migration = await session.get(
                    fixture_migration_models[bind_name],
                    (bind_name, f"{fixture_module.__name__}"),
                )

                signature = cls._calculate_signature(fixture_module)
                if cls._fixture_already_migrated(fixture_migration, signature):
                    continue

                cls._add_fixture_data_to_session(bind_name, fixture_module, session, signature)
                try:
                    await session.commit()
                    cls.logger.info(f"`{fixture_module.__name__}` fixtures correctly created for `{bind_name}` bind")
                except Exception:
                    cls.logger.error(
                        f"`{fixture_module.__name__}` fixtures failed to apply to `{bind_name}` bind",
                        exc_info=True,
                    )
                    await session.rollback()

    @classmethod
    def migrate_fixtures(cls, bind_name: str, session: sessionmaker[Session]):
        """
        Migrate fixture data for a specified bind to the database session. This process involves identifying
        fixture modules, calculating their signatures, checking if a module's data is already migrated, and
        applying the fixture data if necessary. The migration process is committed to the session or rolled back
        in case of failure.

        Parameters:
        cls: Type[CurrentClassType]
            The class on which the method is being called.
        bind_name: str
            The name of the database bind to which the fixtures are being migrated.
        session: sessionmaker[Session]
            The SQLAlchemy session maker instance used for initiating the session.

        Raises:
        None explicitly raised but may propagate exceptions during database operations.
        """
        modules = cls._get_fixture_modules()
        with session() as session:
            for fixture_module in modules:
                cls.logger.debug(f"Creating `{fixture_module.__name__}` fixtures for `{bind_name}` bind")
                fixture_migration = session.get(
                    fixture_migration_models[bind_name],
                    (bind_name, f"{fixture_module.__name__}"),
                )

                signature = cls._calculate_signature(fixture_module)
                if cls._fixture_already_migrated(fixture_migration, signature):
                    continue

                cls._add_fixture_data_to_session(bind_name, fixture_module, session, signature)
                try:
                    session.commit()
                    cls.logger.info(f"`{fixture_module.__name__}` fixtures correctly created for `{bind_name}` bind")
                except Exception:
                    session.rollback()
                    cls.logger.error(f"`{fixture_module.__name__}` fixtures failed to apply to `{bind_name}` bind")


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
                render_as_batch=True,
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def do_run_migration(conn, name):
    context.configure(
        connection=conn,
        upgrade_token=f"{name}_upgrades",
        downgrade_token=f"{name}_downgrades",
        target_metadata=target_metadata.get(name),
        render_as_batch=True,
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
            else:
                do_run_migration(rec["connection"], name)

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

        if context.config.cmd_opts.cmd[0].__name__ == "upgrade":
            for name, rec in engines.items():
                if isinstance(rec["engine"], AsyncEngine):
                    await FixtureHandler.a_migrate_fixtures(
                        bind_name=name,
                        session=async_sessionmaker(bind=rec["connection"]),
                    )
                else:
                    FixtureHandler.migrate_fixtures(bind_name=name, session=sessionmaker(bind=rec["connection"]))
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
