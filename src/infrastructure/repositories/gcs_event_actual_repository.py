from io import BytesIO
import logging
import pandas as pd

from src.infrastructure.clients.cloud_storage_client import CloudStorageClient

logger = logging.getLogger(__name__)


class GcsEventActualRepository:
    def __init__(self, cloud_storage_client: CloudStorageClient):
        self._client = cloud_storage_client

    def fetch_excel_file(self, blob_name: str) -> pd.ExcelFile:
        logger.info("Cloud Storage からイベント実績 Excel をダウンロード開始: %s", blob_name)

        blob = self._client.bucket.blob(blob_name)
        file_bytes = blob.download_as_bytes()

        logger.info("ダウンロード完了。ExcelFile オブジェクトを生成します。")

        return pd.ExcelFile(BytesIO(file_bytes))
