import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Establish a database connection. Associate with `g` object to reuse
    connection if get_db is called multiple times in the same request."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize a new database."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register the `close_db` and `init_db_command` functions with the app instance."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
