import logging
from google.cloud import bigquery
import pandas as pd


logger = logging.getLogger(__name__)


class BqVenuePerformanceRepository:
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

    def __init__(self, client: bigquery.Client, table_id: str):
        self._client = client
        self._table_id = table_id

    def save(
        self,
        df: pd.DataFrame,
        write_disposition: str = bigquery.WriteDisposition.WRITE_TRUNCATE,
    ) -> None:

        logger.info("BigQueryへデータロード開始: %s", self._table_id)

        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            schema=self.TABLE_SCHEMA,
            autodetect=False,
        )

        job = self._client.load_table_from_dataframe(
            df,
            self._table_id,
            job_config=job_config,
        )

        job.result()

        logger.info("BigQueryロード完了: %s", self._table_id)
