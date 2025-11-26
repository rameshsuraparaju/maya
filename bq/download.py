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

"""Provides class for BigQuery download."""
from google.cloud import bigquery
from bq import query


class Download:
    """Download data from a BigQuery table to a dataframe."""

    client = bigquery.Client()

    def __init__(self, project_id: str):
        """Initialize self.

        Args:
            project_id (str): Google Cloud project ID.
        """
        self.project_id = project_id
        self.query = query.Query(self.project_id)

    def download(self, dataset: str, table: str):
        """Download data from BigQuery table.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            pandas.Dataframe: Table data in a Dataframe.
        """

        sql = self.query.read_table_all(dataset, table)
        return __class__.client.query(sql).result().to_dataframe()



