"""
A query is a composable class that you can use to generate and execute arbitrary SQL queries
"""
import logging

from dada_types import SerializableObject, Parameters

VALID_MATERIALIZATIONS = ["results", "ephemeral", "table", "view", "mat_view"]


class SQLQuery(SerializableObject):

    __abstract__ = True
    __materialized__ = None
    __schema__ = None
    __table__ = None
    __exec_func__ = None
    params = []

    _sql = None

    def __init__(
        self,
        exec_func=None,
        materialized="ephemeral",
        schema="public",
        table=None,
        **kwargs,
    ):
        self.__materialized__ = self.__materialized__ or materialized
        self.__table__ = self.__table__ or table
        self.__schema__ = self.__schema__ or schema
        self.__exec_func__ = self.__exec_func__ or exec_func
        self.params = Parameters(**self.params).validate(**kwargs)

    def _validate(self):
        if not self.__materialized__ in VALID_MATERIALIZATIONS:
            raise ValueError(
                f'{self.__materialized__} is not a valid materialization choose from: {", ".join(VALID_MATERIALIZATIONS)}'
            )

    def exec(self, sql):
        """
        Execute a sql statement.
        """
        return self.__exec_func__(sql)

    @property
    def table_name(self):
        """
        Safe table name
        """
        return f'"{self.__schema__}"."{self.__table__}"'

    @property
    def tmp_table(self):
        """
        Safe table name
        """
        return f"tmp_{self.__table__}"

    @property
    def tmp_table_name(self):
        """
        Safe table name
        """
        return f'"{self.__schema__}"."{self.tmp_table}"'

    @property
    def backup_table(self):
        """
        Safe table name
        """
        return f"backup_{self.__table__}"

    @property
    def backup_table_name(self):
        """
        Safe table name
        """
        return f'"{self.__schema__}"."{self.backup_table}"'

    @property
    def sql_mat_type(self):
        """
        mapping to sql keywords
        """
        return {"table": "TABLE", "view": "VIEW", "mat_view": "MATERIALIZED VIEW"}.get(
            self.__materialized__, None
        )

    def table_exists(self):
        """"""
        q = f"""
        SELECT EXISTS (
          SELECT FROM information_schema.tables 
            WHERE  table_schema = '{self.__schema__}'
            AND    table_name   = '{self.__table__}'
        );"""
        for row in self.exec(q):
            if row["exists"]:
                return True
        return False

    def view_exists(self):
        """"""
        q = f"""
        SELECT EXISTS (
          SELECT FROM information_schema.views 
          WHERE  table_schema = '{self.__schema__}'
          AND    table_name   = '{self.__table__}'
        );"""
        for row in self.exec(q):
            if row["exists"]:
                return True
        return False

    def mat_view_exists(self):
        """"""
        q = f"""
        SELECT EXISTS (
          SELECT FROM pg_matviews 
          WHERE  schemaname = '{self.__schema__}'
          AND    matviewname  = '{self.__table__}'
        );"""
        for row in self.exec(q):
            if row["exists"]:
                return True
        return False

    def exists(self):
        """
        Check if various materializations exists
        """
        fx = {
            "table": self.table_exists,
            "view": self.view_exists,
            "mat_view": self.mat_view_exists,
        }.get(self.__materialized__, None)
        if not fx:
            return False
        return fx()

    @property
    def sql(self):
        """
        Generate the sql from the template.
        """
        raise NotImplementedError("You must define a `sql` property for a query")

    def create_schema(self):
        """
        Create this schema
        """
        return self.exec(f'CREATE SCHEMA IF NOT EXISTS "{self.__schema__}";')

    def materialize_sql(self, name):
        """
        Create a table from the query
        """
        return f"""
            CREATE {self.sql_mat_type} {name} AS (
                {self.sql}
            );"""

    def rename_sql(self, from_name, to_name):
        """
        generate sql to rename a table
        """
        return f"ALTER {self.sql_mat_type} {from_name} RENAME TO {to_name};"

    def drop_sql(self, name):
        """
        generate sql to drop a table
        """
        return f"DROP {self.sql_mat_type} {name} CASCADE;"

    def update_sql(self):
        """"""
        return f"""
        BEGIN;
        -- create a temporary table from the query
        {self.materialize_sql(self.tmp_table_name)}
        -- backup the current table to the "backup" table
        {self.rename_sql(self.table_name, self.backup_table)}
        -- overwrite the current table with the temp table
        {self.rename_sql(self.tmp_table_name, self.__table__)}
        -- drop the backup table
        {self.drop_sql(self.backup_table_name)}
        COMMIT;
        """

    def run_materialization(self):
        """
        Run a materialization (view/table/mat_view)
        """
        # ensure schema presence
        self.create_schema()

        # if the table does not yet exist, just materialize it
        if not self.exists():
            return self.exec(self.materialize_sql(self.table_name))
        # otherwise overwrite it in a transaction-safe manner
        return self.exec(self.update_sql())

    def run(self):
        """
        Run the configured materialization
        """
        return {
            "results": lambda: self.exec(self.sql),
            "ephemeral": lambda: self.sql,
            "table": self.run_materialization,
            "view": self.run_materialization,
            "mat_view": self.run_materialization,
        }.get(self.__materialized__)()

    def refresh(self):
        """
        Refresh (only for materialized views)
        """
        if not self.__materialized__ == "mat_view":
            raise ValueError("refresh only applies to materialized views")
        if not self.exists():
            raise ValueError(f"Materialized View {self.table_name} does not exist yet")
        return self.exec(f"REFRESH MATERIALIZED VIEW {self.table_name};")

    def to_dict(self):
        """
        Serialize this query as a dictionary
        """
        return {
            "name": self.object_name,
            "title": self.object_title,
            "info": self.object_description,
            "materialized": self.__materialized__,
            "schema": self.__schema__,
            "table": self.__table__,
            "params": self.params,
            "sql": self.sql,
        }
