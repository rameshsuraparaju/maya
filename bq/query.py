# MIT License

# Copyright (c) 2025 rameshsuraparaju

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides sql queries."""


class Query:
    """Build SQL Queries"""

    def __init__(self, project_id):
        self.project_id = project_id

    def __validate(self, dataset, table) -> bool:
        if dataset == '' or table == '':
            raise ValueError from None
        return True

    def __get_tablename(self, dataset, table) -> str:

        if self.__validate(dataset, table):
            return self.project_id + \
                    '.' + dataset + \
                    '.' + table

    def read_table_all(self, dataset: str, table: str) -> str:

        return 'SELECT * FROM `' \
            + self.__get_tablename(dataset, table) + \
            '`;'

    def read_table_field(self, dataset: str, table: str, field: str) -> str:

        return 'SELECT '+ field +' FROM `' \
            + self.__get_tablename(dataset, table) + \
            '`;'

    def read_table_fields(self,
                          dataset: str,
                          table: str,
                          fields: list,
                          client_field: str = 'none',
                          client_value: str = '000') -> str:

        if client_field == 'none' and client_value == '000':
            return f'SELECT {", ".join(fields)} FROM \
                    `{self.__get_tablename(dataset, table)}`;'
        else:
            return f'SELECT {", ".join(fields)} FROM \
                    `{self.__get_tablename(dataset, table)}` \
                    WHERE {client_field} = "{client_value}";'

    # TODO refactor to merge into one query generator method
    def read_header_fields(self,
                          dataset: str,
                          table: str,
                          fields: list,
                          client_field: str,
                          client_value: str,
                          link_field: str,
                          link_value) -> str:

        return f'SELECT {", ".join(fields)} FROM \
                `{self.__get_tablename(dataset, table)}` \
                WHERE {client_field} = "{client_value}" \
                    AND {link_field} = "{link_value}";'

    # TODO refactor to merge into one query generator method
    def read_fields_with_date_and_key_filter(
        self,
        dataset: str,
        table: str,
        fields: list,
        date_field: str,
        date_value: str,
        key_field: str,
        key_value: str,
    ) -> str:

        return f'SELECT {", ".join(fields)} FROM \
                `{self.__get_tablename(dataset, table)}` \
                WHERE {date_field} = "{date_value}" \
                    AND {key_field} = "{key_value}";'

    def truncate_table(self, dataset, table):

        return 'TRUNCATE TABLE `' \
            + self.__get_tablename(dataset, table) + \
             '`;'

    def read_sap_schema(self, dataset, table) -> str:

        return 'SELECT  fieldname, \
                        keyflag, \
                        checktable, \
                        inttype as saptype, \
                        CAST(intlen AS INT64) AS length, \
                        CAST(decimals AS INT64) AS decimals, \
                        domname \
                FROM `' \
            + self.__get_tablename(dataset, 'dd03l') + \
            '` WHERE tabname = "' + table.upper() + \
            '" ORDER BY position;'

    def read_sap_domain(self, dataset, domname) -> str:

        return 'SELECT ddtext AS values \
                FROM `' \
                + self.__get_tablename(dataset, 'dd07t') + \
                '` WHERE domname = "' + domname.upper() + \
                '" AND ddlanguage = "E" ORDER BY valpos;'

    def read_sap_checkfield(self, dataset, checktable, domname) -> str:

        return 'SELECT fieldname \
                FROM `'\
                + self.__get_tablename(dataset, 'dd03l') + \
                '` WHERE tabname = "' + checktable.upper() + \
                ' AND domname = "' + domname.upper() + ';'
