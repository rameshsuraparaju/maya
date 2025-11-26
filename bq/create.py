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

"""Provides class for creating artefacts in big query."""

from google.cloud import bigquery

from bq.read import Reader


class Create:
    """Create artefacts in BigQuery."""

    client = bigquery.Client()

    def __init__(self, project_id: str):
        """Initialize self.

        Args:
            project_id (str): Google Cloud project ID.
        """
        self.project_id = project_id
        self.reader = Reader(project_id)

    def __get_table_id(self, dataset: str, table: str):
        """concatenates input to fully qualified BigQuery table name.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            str: Fully qualified BigQuery table name.
        """
        return self.project_id + "." + dataset + "." + table

    def __gen_bq_schema(self, field_spec: list):
        """Generates BigQuery schema as array of bigquery.SchemaField objects

        Args:
            field_spec (list): filed (table column) specifictaions for BigQuery.
        """

        sap_type_map = {
            "b": "INT1",
            "s": "INT2",
            "I": "INT4",
            "8": "INT8",
            "F": "FLOAT",
            "P": "NUMERIC",
            "a": "DECIMAL",
            "e": "NUMERIC",
            "N": "STRING",
            "X": "STRING",
            "y": "STRING",
            "C": "STRING",
            "g": "STRING",
            "?": "STRING",
            "&": "STRING",
            "D": "DATE",
            "T": "TIME",
        }

        schema = []

        # TODO: Mapping other modes?
        for field in field_spec:
            if field.get("keyflag") == "X":
                mode = "REQUIRED"
            else:
                mode = "NULLABLE"

            schema.append(
                bigquery.SchemaField(
                    name=field.get("fieldname").lower(),
                    field_type=sap_type_map.get(field.get("saptype")),
                    mode=mode,
                )
            )
        return schema

    def create_table(self, meta_dataset: str, dataset: str, table: str):

        if not self.reader.table_exists(dataset, table):
            table_id = self.__get_table_id(dataset, table)
            field_spec = self.reader.read_sap_schema(dataset=meta_dataset, table=table)
            bq_schema = self.__gen_bq_schema(field_spec)
            table = bigquery.Table(table_id, schema=bq_schema)
            self.client.create_table(table)

    def create_view(self, dataset: str, view: str, sql: str):

        dataset = self.client.dataset(dataset)
        table = dataset.table(view)

        table.view_query = sql

        try:
            table.create()
            return True
        except Exception as err:
            print(err)
            return False
