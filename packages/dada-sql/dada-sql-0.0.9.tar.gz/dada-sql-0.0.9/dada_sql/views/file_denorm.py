import logging

from dada_types import T
from dada_types.dictionary import TYPE_NAMES
import dada_settings

from dada_sql.core import SQLQuery

logger = logging.getLogger()


class FileDenorm(SQLQuery):
    """
    Create a table of files with all fields mapped out as
    separate columns and folders, desktops, and themes joined in.
    """

    __abstract__ = False
    __materialized__ = "table"
    __schema__ = "search"
    __table__ = "file_field"

    params = {
        "file_type": {
            "info": "The file type to query for (this will limit the available fields to select from to those which apply to this file type)",
            "type": "text",
            "options": settings.FILE_DEFAULTS_FILE_TYPES + ["all"],
            "default": None,
        },
        "file_subtype": {
            "info": "The file subtype to query for (this will limit the available fields to select from to those which apply to this file subtype)",
            "type": "text",
            "options": settings.FILE_DEFAULTS_FILE_SUBTYPES + ["all"],
            "default": None,
        },
        "field_type": {
            "info": "The field type to query for (this will limit the available fields to select from to those which apply to this field type)",
            "type": "text",
            "options": TYPE_NAMES,
            "default": "all",
        },
        "folder_ids": {
            "info": "Folder IDs to limit the file results to",
            "type": "int_array",
            "default": [],
        },
        "select": {
            "info": "The list of fields to include in the results",
            "type": "text_array",
            "default": ["all"],
        },
        "exclude": {
            "info": "The list of fields to exclude from the results",
            "type": "text_array",
            "default": [],
        },
        "sort_by": {
            "info": "The field name to use for ordering the query results",
            "type": "text",
            "default": "created_at",
        },
        "sort_dir": {
            "info": "The direction to order the query results",
            "type": "text",
            "default": "DESC",
            "options": ["ASC", "DESC"],
        },
    }

    # internal
    _file_sql = None

    @property
    def is_select_all(self):
        """
        Is this a select all query?
        """
        return "all" in self.params["select"]

    @property
    def has_file_type_filter(self):
        """"""
        return self.params["file_type"] is not None

    @property
    def has_file_subtype_filter(self):
        """"""
        return self.params["file_subtype"] is not None

    @property
    def has_field_type_filter(self):
        """"""
        return self.params["field_type"] is not None

    @property
    def is_select_all_field_types(self):
        """"""
        return self.params.get("field_type", None) == "all"

    @property
    def has_field_filter(self):
        """"""
        return any(
            [
                self.has_file_type_filter,
                self.has_file_subtype_filter,
                self.has_field_type_filter,
            ]
        )

    @property
    def has_folder_id_filter(self):
        """"""
        return len(self.params.get("folder_ids", [])) != 0

    @property
    def ext_fields_to_select_filter(self):
        """
        A filter for the fields query
        """
        fields = "','".join(self.ext_fields_to_select)
        return f"('{fields}')"

    @property
    def base_fields_sql(self):
        """
        The base query to fetch a list of fields
        """
        return """
          SELECT 
            name, type
          FROM 
            field 
          WHERE 
            1=1 
        """

    @property
    def fields_sql(self):
        """
        Query to get the initial list of fields to join/query for.
        """
        filters = []

        # add subtype filters
        for t in ["file_type", "file_subtype"]:
            if self.params.get(t, None):
                filters.append(f"'{self.params[t]}' IN accepts_{t}s")

        # add field type filter
        if self.has_field_type_filter and not self.is_select_all_field_types:
            filters.append(f"type = '{self.params['field_type']}'")

        # add optional select filter
        if not self.is_select_all:
            filters.append(f"name IN {self.ext_fields_to_select_filter}")

        return self.base_fields_sql + "\n\tAND ".join(filters)

    def get_fields(self):
        """
        Fetch external field names via query.
        """
        return [
            field
            for field in self.exec(self.fields_sql)
            if field["name"] not in self.params["exclude"]
        ]

    @property
    def file_sql(self):
        """
        Generate the File SQL
        """
        if not self._file_sql:
            # get internal select statements
            int_select_statements = ",\n\t".join(
                [f"file.{f}" for f in self.core_fields_to_select]
            )

            # generate fields to select based on type /searchable status
            fields_to_select = list(
                map(self._gen_select_statement_for_field, self.get_fields())
            )
            field_select_statements = ",\n\t".join(fields_to_select)

            self._file_sql = f"""
            SELECT 
            {int_select_statements},
            {field_select_statements}
            FROM
              file
            """
        return self._file_sql

    @property
    def folder_sql(self):
        """
        Get a list of folder slugs per file
        """
        return """
          SELECT 
            file_id,
            ARRAY_AGG(folder.slug) as folders
          FROM
            file_folder 
          LEFT JOIN
            folder ON folder.id = file_folder.folder_id
          GROUP BY 
            1
        """

    @property
    def desktop_sql(self):
        """
        Get a list of desktop slugs per file
        """
        return """
          SELECT 
            file_id,
            ARRAY_AGG(desktop.slug) as desktops
          FROM
            file_folder 
          LEFT JOIN
            folder ON folder.id = file_folder.folder_id
          LEFT JOIN
            folder_desktop ON folder.id = folder_desktop.folder_id
          LEFT JOIN
            desktop ON folder_desktop.desktop_id = desktop.id
          GROUP BY 
            1
        """

    @property
    def tag_sql(self):
        """
        Get a list of tag slugs per file
        """
        return """
          SELECT 
            file_id,
            ARRAY_AGG(tag.slug) as tags
          FROM
            file_tag 
          LEFT JOIN
            tag ON tag.id = file_tag.tag_id
          GROUP BY 
            1
        """

    @property
    def theme_sql(self):
        """
        Get each file's theme
        """
        return """
          SELECT 
            file_id,
            theme.id as theme_id,
            theme.name as theme_name,
            theme.emoji as theme_emoji,
            theme.fields as theme_fields
          FROM
            file_theme
          LEFT JOIN
            theme ON theme.id = file_theme.theme_id
        """

    @property
    def order_by(self):
        return f"ORDER BY {self.params['sort_by']} {self.params['sort_dir']}"

    @property
    def sql(self):
        """
        The Full Denormalized File  query.
        """
        return f"""
          WITH file_folder_agg AS (
            {self.folder_sql}

          ), file_desktop_agg AS (
            {self.desktop_sql}

          ),
          file_tag_agg AS (
            {self.tag_sql}

          ), 
          file_theme_agg AS (
            {self.theme_sql}

          ),
          file_fields_join AS (
            {self.file_sql}

          ),
          joined AS (
            SELECT 
              file_fields_join.*,
              file_folder_agg.folders,
              file_desktop_add.desktops,
              file_tag_add.tags,
              file_theme.*
            FROM 
              file_fields_join 
            LEFT JOIN 
              file_folder_agg ON file_fields_join.id = file_folder_agg.file_id
            LEFT JOIN 
              file_desktop_agg ON file_felds_join.id = file_desktop_agg.file_id
            LEFT JOIN 
              file_tag_agg ON file_felds_join.id = file_tag_agg.file_id
            LEFT JOIN 
              file_theme_agg ON file_felds_join.id = file_theme_agg.file_id
          )
          SELECT 
            * 
          FROM 
            joined 
          {self.order_by}
        """
