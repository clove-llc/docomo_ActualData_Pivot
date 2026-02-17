import logging


import pandas as pd
from google.cloud import bigquery

logger = logging.getLogger(__name__)


class BigQueryRepository:
    DATA_SET = "docomo_eventActual"

    TABLE_SCHEMA = [
        bigquery.SchemaField("datasource", "STRING"),
        bigquery.SchemaField("no", "INTEGER"),
        bigquery.SchemaField("event_month", "STRING"),
        bigquery.SchemaField("regional_office_name", "STRING"),
        bigquery.SchemaField("branch_name", "STRING"),
        bigquery.SchemaField("facility_name", "STRING"),
        bigquery.SchemaField("floor_label", "STRING"),
        bigquery.SchemaField("floor_number", "INTEGER"),
        bigquery.SchemaField("floor_number_above_ground", "INTEGER"),
        bigquery.SchemaField("is_basement_floor", "BOOLEAN"),
        bigquery.SchemaField("floor_category", "STRING"),
        bigquery.SchemaField("space_name", "STRING"),
        bigquery.SchemaField("area_raw", "STRING"),
        bigquery.SchemaField("area_sqm", "INTEGER"),
        bigquery.SchemaField("area_group", "STRING"),
        bigquery.SchemaField("is_area_unconfirmed", "BOOLEAN"),
        bigquery.SchemaField("is_daily_venue", "BOOLEAN"),
        bigquery.SchemaField("helper_company_name", "STRING"),
        bigquery.SchemaField("staff_count", "STRING"),
        bigquery.SchemaField("staff_count_numeric", "INTEGER"),
        bigquery.SchemaField("start_date", "DATE"),
        bigquery.SchemaField("end_date", "DATE"),
        bigquery.SchemaField("actual_days_raw", "STRING"),
        bigquery.SchemaField("actual_days", "INTEGER"),
        bigquery.SchemaField("date", "DATE"),
        bigquery.SchemaField("daily_result_raw", "STRING"),
        bigquery.SchemaField("daily_result", "INTEGER"),
        bigquery.SchemaField("is_missing_input", "BOOLEAN"),
        bigquery.SchemaField("is_event_cancelled", "BOOLEAN"),
    ]

    def __init__(self, client: bigquery.Client):
        self._client = client

    def _get_full_table_id(self, table_id: str) -> str:
        return f"{self._client.project}.{self.DATA_SET}.{table_id}"

    def _add_missing_columns(self, df: pd.DataFrame) -> None:
        for field in self.TABLE_SCHEMA:
            if field.name not in df.columns:
                df[field.name] = None

    def _align_dataframe_types(self, df: pd.DataFrame) -> pd.DataFrame:
        schema_map = {field.name: field.field_type for field in self.TABLE_SCHEMA}

        for field_name, field_type in schema_map.items():
            if field_name not in df.columns:
                continue

            if field_type == "STRING":
                df[field_name] = df[field_name].astype("string")

            elif field_type == "INTEGER":
                df[field_name] = pd.to_numeric(df[field_name], errors="coerce").astype(
                    "Int64"
                )

            elif field_type == "BOOLEAN":
                df[field_name] = df[field_name].astype("boolean")

            elif field_type == "DATE":
                df[field_name] = pd.to_datetime(df[field_name], errors="coerce").dt.date

        return df

    def save_venue_performance(self, df: pd.DataFrame) -> None:
        full_table_id = self._get_full_table_id("venue_performance")

        logger.info("BigQueryへデータロードを開始します: %s", full_table_id)

        self._add_missing_columns(df)

        df = self._align_dataframe_types(df)

        # テーブルの列順を整える
        df = df[[field.name for field in self.TABLE_SCHEMA]]

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=self.TABLE_SCHEMA,
            autodetect=False,
        )

        job = self._client.load_table_from_dataframe(
            df,
            full_table_id,
            job_config=job_config,
        )

        job.result()

        logger.info("BigQueryへのデータロード完了: %s", full_table_id)
