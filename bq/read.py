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

"""Provides class for uploading data to big query."""

import numpy as np

from google.cloud import bigquery
from google.api_core.exceptions import BadRequest, NotFound
from bq import query


class Reader:
    """Read data / metadata from BigQuery."""

    client = bigquery.Client()

    def __init__(self, project_id: str):
        """Initialize self.

        Args:
            project_id (str): Google Cloud project ID.
        """
        self.project_id = project_id
        self.query = query.Query(self.project_id)

    def __get_table_id(self, dataset: str, table: str) -> str:
        """concatenates input to fully qualified BigQuery table name.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            str: Fully qualified BigQuery table name.
        """
        return self.project_id + "." + dataset + "." + table

    def __df_to_list(self, dataframe):

        if len(dataframe) > 0:
            values = [item for sublist in dataframe.values.tolist() for item in sublist]
            return values
        else:
            return []

    def get_table_info(self, dataset: str, table: str) -> dict:
        """read a table in BigQuery.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            google.cloud.bigquery.table.Table: Table properties.
        """
        return __class__.client.get_table(self.__get_table_id(dataset, table))

    def read_bq_schema(self, dataset: str, table: str):

        try:
            table_info = __class__.client.get_table(self.__get_table_id(dataset, table))
            return [field.to_api_repr() for field in table_info.schema]
        except BadRequest:
            return []

    def read_table_field(self, dataset: str, table: str, field: str) -> list:

        sql = self.query.read_table_field(dataset, table, field)
        job = __class__.client.query(sql)
        if not job.errors:
            df = job.result().to_dataframe()
            return self.__df_to_list(df)
        else:
            return []

    def read_table_fields(
        self,
        dataset: str,
        table: str,
        fields: list,
        client_field: str = "none",
        client_value: str = "000",
    ) -> list:

        sql = self.query.read_table_fields(
            dataset, table, fields, client_field, client_value
        )
        job = __class__.client.query(sql)
        if not job.errors:
            df = job.result().to_dataframe()
            return df.to_dict(orient="records")
        else:
            return []

    def __convert_ndarray_to_list(self, l: list) -> list:

        for li in l:
            for k in li.keys():
                if isinstance(li[k], np.ndarray):
                    li.update({k: li[k].tolist()})
                    self.__convert_ndarray_to_list(li[k])
        return l

    def read_table_fields_with_repeated_records(
        self,
        dataset: str,
        table: str,
        fields: list,
        client_field: str = "none",
        client_value: str = "000",
    ) -> list:

        sql = self.query.read_table_fields(
            dataset, table, fields, client_field, client_value
        )
        job = __class__.client.query(sql)
        results = []
        if not job.errors:
            rows = job.result().to_dataframe().to_dict(orient="records")
            results = self.__convert_ndarray_to_list(rows)
            return results

        else:
            return results

    def read_header_fields(
        self,
        dataset: str,
        table: str,
        fields: list,
        client_field: str,
        client_value: str,
        link_field: str,
        link_value: str,
    ) -> list:

        sql = self.query.read_header_fields(
            dataset, table, fields, client_field, client_value, link_field, link_value
        )
        job = __class__.client.query(sql)
        if not job.errors:
            df = job.result().to_dataframe()
            return df.to_dict(orient="records")
        else:
            return []

    # TODO: Refactor to generic query with generic where clause
    def read_fields_with_date_and_key_filter(
        self,
        dataset: str,
        table: str,
        fields: list,
        date_field: str,
        date_value: str,
        key_field: str,
        key_value: str,
    ) -> list:

        sql = self.query.read_fields_with_date_and_key_filter(
            dataset, table, fields, date_field, date_value, key_field, key_value
        )
        job = __class__.client.query(sql)
        if not job.errors:
            df = job.result().to_dataframe()
            return df.to_dict(orient="records")
        else:
            return []

    def get_table(self, dataset: str, table: str):
        """read a table in BigQuery.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            google.cloud.bigquery.table.Table: Table properties.
        """
        return __class__.client.get_table(self.__get_table_id(dataset, table))

    def table_exists(self, dataset: str, table: str) -> bool:
        """Check if a BigQuery table exists

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            bool: true (exists) or false (does not exist)
        """
        try:
            __class__.client.get_table(self.__get_table_id(dataset, table))
            return True
        except NotFound:
            return False

    def read_sap_schema(self, dataset: str, table: str) -> list:

        # TODO: Check if pandas_gbq performs better?
        # https://googleapis.dev/python/pandas-gbq/latest/reading.html
        sql = self.query.read_sap_schema(dataset, table)
        try:
            df = __class__.client.query(sql).result().to_dataframe()
            return df.to_dict(orient="records")
        except BadRequest:
            return []

    def read_sap_domain(self, dataset: str, domain: str) -> list:

        # TODO: Check if pandas_gbq performs better?
        # https://googleapis.dev/python/pandas-gbq/latest/reading.html
        sql = self.query.read_sap_domain(dataset, domain)
        try:
            df = __class__.client.query(sql).result().to_dataframe()
            return self.__df_to_list(df)
        except BadRequest:
            return []

    def read_sap_checkfield(self, dataset: str, checktable: str, domname: str) -> str:

        # TODO: Check if pandas_gbq performs better?
        # https://googleapis.dev/python/pandas-gbq/latest/reading.html
        sql = self.query.read_sap_checkfield(dataset, checktable, domname)
        job = __class__.client.query(sql)
        if not job.errors:
            return job.result().to_dataframe().value.tolist()[0][0]
        else:
            return ""
