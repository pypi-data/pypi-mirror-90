"""
A separate API Program for running admin tasks in the app context
"""

import logging

from flask_migrate import Migrate
import click

# core objects
from dada.factory import create_app
from dada.queue.core import celery
from dada.models.core import db, db_execute, s3conn, rdsconn

# Type Helpers
from dada_types import T
from dada_types.flt import FilterString

# pass in full utils library to shell context
import dada_utils as utils

# MODELS
from dada.models.desktop import Desktop
from dada.models.field import Field, FieldCache
from dada.models.file import File
from dada.models.folder import Folder
from dada.models.tag import Tag
from dada.models.user import User

# etc.
import dada_settings

# initialize app / plugins
app = create_app(celery=celery)
migrate = Migrate(app, db)
CLI_ADMIN_LOGGER = logging.getLogger()
LINE_HEADER = f"{'*%!'*20}\r\n"

# initialize the shell contenxt
@app.shell_context_processor
def make_shell_context():
    return dict(
        # core connections
        app=app,
        db=db,
        db_execute=db_execute,
        s3conn=s3conn,
        rdsconn=rdsconn,
        utils=utils,
        settings=dada_settings,
        Field=Field,
        FieldCache=FieldCache,
        File=File,
        Tag=Tag,
        User=User,
        Folder=Folder,
        Desktop=Desktop,
    )


# ///////////////////
# ADMIN COMMANDS
# ///////////////////


@app.cli.command(help="Initialize the Database")
def db_init():
    """"""
    db.configure_mappers()  # for sqlalchemy searchable
    db.create_all(bind=None, app=app)
    db.session.commit()


@app.cli.command(help="Create built-in defaults in the database")
def db_create_defaults():
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default users...")
    User.create_defaults()
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default tags...")
    Tag.create_defaults(user_id=1)
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default fields...")
    Field.create_defaults(tag_id=[1, 2])
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default desktops...")
    Desktop.create_defaults(user_id=1, tag_id=[2])
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default folders...")
    Folder.create_defaults(user_id=1, tag_id=[1, 2])
    CLI_ADMIN_LOGGER.info(f"{LINE_HEADER}creating default files...")
    File.create_defaults(user_id=1, tag_id=[1, 2])
    # CLI_ADMIN_LOGGER.info("Constructing file-field search view...")
    # FileDenorm().run()
    db.session.commit()


@app.cli.command(help="[WARNING] Drop the databsase")
def db_drop():
    if click.prompt(
        f"{LINE_HEADER}Are you sure you want to lose all your data?", bool=True
    ):
        db.drop_all(bind=None)


def run():
    """
    Run the admin CLI.
    """
    app.cli()
