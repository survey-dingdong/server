import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations.ops import AddColumnOp, AlterColumnOp, MigrateOperation
from alembic.runtime.migration import MigrationContext
from alembic.script.revision import Revision
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future.engine import Connection
from sqlalchemy.schema import MetaData

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _app_init() -> MetaData:
    from app.project.domain.entity import (
        ExperimentParticipantTimeslot,
        ExperimentProject,
        ExperimentTimeslot,
    )
    from app.user.domain.entity import User, UserOauth
    from app.workspace.domain.entity import Workspace
    from core.config import config as server_config
    from core.db import Base

    config.set_main_option("sqlalchemy.url", str(server_config.DB_URL))
    return Base.metadata


target_metadata = _app_init()


writer = rewriter.Rewriter()


@writer.rewrites(AddColumnOp)
def _(
    context: MigrationContext,
    revision: Revision,
    op: AddColumnOp,
) -> list[MigrateOperation]:
    if op.column.nullable:
        return [op]
    else:
        op.column.nullable = True
        return [
            op,
            AlterColumnOp(
                op.table_name,
                op.column.name,
                modify_nullable=False,
                existing_type=op.column.type,
            ),
        ]


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations input 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=lambda *args: True,
        literal_binds=True,
        compare_server_default=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=lambda *args: True,
        sqlalchemy_module_prefix="sa.",
        process_revision_directives=writer,
        compare_server_default=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations input 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    from core.config import config as server_config

    connectable = create_engine(
        server_config.DB_URL.replace("aiomysql", "pymysql"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
