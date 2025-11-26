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
import logging
import pandas as pd

from typing import List
from google.cloud import bigquery

from bq import query
from gcs import hoarder

class Upload:
    """ Upload data to a BigQuery table from a dataframe."""

    client = bigquery.Client()

    def __init__(self, project_id: str):
        """Initialize self.

        Args:
            project_id (str): Google Cloud Project ID.
        """
        self.logger = logging.getLogger(__name__)
        self.project_id = project_id
        self.hoarder = hoarder.Hoarder(project_id)

    def __get_table_id(self, dataset: str, table: str):
        """concatenates input to fully qualified BigQuery table name.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.

        Returns:
            str: Fully qualified BigQuery table name.
        """
        return self.project_id + '.' + dataset + '.' + table

    def __truncate_table(self, dataset: str, table: str):
        """Truncates specified table in BigQuery.

        Args:
            dataset (str): Dataset name.
            table (str): Table name.
        """
        sql = query.Query(self.project_id).truncate_table(dataset, table)
        __class__.client.query(sql)

    def upload(
            self,
            dataframe: pd.DataFrame,
            schema: List[bigquery.SchemaField],
            dataset: str,
            table: str,
            write: str,
            bucket_name: str = ""
        ):

        if any(s["type"] == "JSON" for s in schema):
            self.__upload_with_json_columns(
                dataframe,
                schema,
                dataset,
                table,
                write,
                bucket_name
            )

        else:

            write_disposition = 'WRITE_APPEND'
            if write == 'TRUNCATE':
                # JobConfig's WRITE_TRUNCATE does NOT work!!
                self.__truncate_table(dataset, table)
                write_disposition = 'WRITE_APPEND'

            job_config = bigquery.LoadJobConfig(
                write_disposition=write_disposition,
                schema=schema
            )

            job = __class__.client.load_table_from_dataframe(
                dataframe,
                self.__get_table_id(
                    dataset, table),
                job_config=job_config
            )

            # Wait for the result
            _ = job.result()


    def __upload_with_json_columns(
            self,
            dataframe: pd.DataFrame,
            schema: List[bigquery.SchemaField],
            dataset: str,
            table: str,
            write: str,
            bucket_name: str
        ):

        try:
            uri = self.hoarder.write_frame_as_json_file(
                source_df=dataframe,
                target_bucket_name=bucket_name,
                target_table_id=table
            ).get("uri")
        except Exception as e:
            self.logger.error("Cannot get file URI")
            raise ValueError

        write_disposition = 'WRITE_APPEND'
        if write == 'TRUNCATE':
            # JobConfig's WRITE_TRUNCATE does NOT work!!
            self.__truncate_table(dataset, table)
            write_disposition = 'WRITE_APPEND'

        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            schema=schema,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )

        job = __class__.client.load_table_from_uri(
            uri,
            self.__get_table_id(dataset, table),
            job_config=job_config)

        # Wait for the result
        _ = job.result()
        table = __class__.client.get_table(self.__get_table_id(dataset, table))
        self.logger.info('Loaded %s rows to %s', table.num_rows, table)

    def upload_chunks(self,
                      chunk_size: int,
                      dataframe: pd.DataFrame,
                      schema: List[bigquery.SchemaField],
                      dataset: str,
                      table: str,
                      write: str):

        for i in range(0, len(dataframe), chunk_size):

            chunk = dataframe[i:i+chunk_size]

            # Convert the chunk to a list of dictionaries for insertion
            rows_to_insert = chunk.to_dict(orient='records')

            # Create a job configuration
            job_config = bigquery.LoadJobConfig(
                            schema=schema,
                            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                            )

            # Start the job
            try:
                table_ref = __class__.client.dataset(dataset).table(table)
                table = __class__.client.get_table(table_ref)
                errors = __class__.client.insert_rows(table, rows_to_insert)
                if not errors:
                    print(f"Batch {i//chunk_size + 1} inserted successfully.")
                else:
                    print(f"Encountered errors while inserting batch {i//chunk_size + 1}:")
                    print(errors)
            except Exception as e:
                print(f"Error: {e}")

