from google.cloud import storage

class GoogleCloudStorageClient:
    def __init__(
        self,
        gcp_project_id: str,
        bucket_name: str,
    ):
        self.client = storage.Client(project=gcp_project_id)
        self.bucket = self.client.bucket(bucket_name)