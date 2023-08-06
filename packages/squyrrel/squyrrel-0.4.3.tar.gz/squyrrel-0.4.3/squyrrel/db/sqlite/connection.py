import sqlite3

from squyrrel.db.connection import SqlDatabaseConnection


class SqliteConnection(SqlDatabaseConnection):

    database_error_cls = sqlite3.Error
    integrity_error_cls = sqlite3.IntegrityError

    def connect(self, filename, select_version=False, foreign_keys=True, **kwargs):
        self.filename = filename

        self.c = sqlite3.connect(self.filename, **kwargs)
        if select_version:
            self.execute('SELECT sqlite_version();')
        if foreign_keys:
            self.execute('PRAGMA foreign_keys = ON;')
