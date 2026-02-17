import logging

from google.cloud import storage
from google.cloud import bigquery

from src.bigquery_repository import (
    BigQueryRepository,
)
from src.cloud_storage_repository import (
    CloudStorageRepository,
)
from src.transformer import EventActualTransformer


logger = logging.getLogger(__name__)


def run_venue_performance_pipeline(project_id, blob_name: str):
    gcs_client = storage.Client(project=project_id)
    bq_client = bigquery.Client(project=project_id)

    input_repository = CloudStorageRepository(gcs_client)
    output_repository = BigQueryRepository(bq_client)
    transformer = EventActualTransformer()

    excel_file = input_repository.fetch_excel_file(
        bucket_name="docomo_event_actual", blob_name=blob_name
    )

    logger.info("Excelファイルを解析し、クレンジングを行います。")
    df = transformer.transform(excel_file)
    logger.info("クレンジング完了。")

    output_repository.save_venue_performance(df)
