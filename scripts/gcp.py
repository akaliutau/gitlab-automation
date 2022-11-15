import os
from collections import Sequence

from google.cloud import bigquery
from google.cloud.bigquery import QueryJob

from constants import HOST_PROJECT


class BigQuery:
    os.environ.setdefault("GCLOUD_PROJECT", HOST_PROJECT)

    def __init__(self, project_id: str):
        self._project_id = project_id
        self._client = bigquery.Client()

    @staticmethod
    def _to_json(query_job: QueryJob) -> any:
        return [dict(row) for row in query_job] if query_job else []

    @staticmethod
    def normalize(sql: str) -> str:
        return ' '.join(sql.split())

    @staticmethod
    def get_full_name(dataset: str, table: str) -> str:
        return f"{dataset}.{table}"

    @staticmethod
    def process_errors(results: Sequence[dict]) -> None:
        errors_count = 0
        first_error_msg = ''
        for result in results:
            if 'errors' in result:
                errors_count += 1
                first_error_msg = first_error_msg or result['errors']
        print(f'errors: {errors_count}')
        if first_error_msg:
            raise Exception(first_error_msg)

    def query_to_json(self, sql) -> any:
        print(self.normalize(sql))
        return self._to_json(self._client.query(query=sql, project=self._project_id))

    def insert_all(self, table: str, records: list) -> None:
        if records:
            self.process_errors(self._client.insert_rows_json(table, records))
        else:
            print('no records to insert')

    def update_all(self, table: str, key_field: str, update_field: str, records: list) -> any:
        if records:
            for r in records:
                self.update(table, key_field, r[key_field], update_field, r[update_field])
        else:
            print('no records to update')

    def update(self, table: str, key_field: str, key_value: str, update_field: str, value: str) -> any:
        sql = f"""
          UPDATE `{self._project_id}.{table}`
          SET {update_field} = {value}
          WHERE {key_field} = "{key_value}";
        """
        print(self.normalize(sql))
        return self._client.query(query=sql, project=self._project_id)


