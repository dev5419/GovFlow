import os
import uuid
import datetime
import io
from minio import Minio

class ReportStorageService:
    @staticmethod
    def store_report(tender_id: str, bidder_id: str, pdf_bytes: bytes) -> str:
        """
        Stores the generated PDF report in MinIO.
        Returns the object key.
        Per PRD 8.7 / 20.4, ensures immutability by generating a new key every time.
        """
        # Ensure a new UUID or timestamp so past reports are never overwritten
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        object_key = f"reports/{tender_id}/{bidder_id}/compliance_report_{timestamp}_{unique_id}.pdf"
        
        minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        minio_access_key = os.getenv("MINIO_ACCESS_KEY", "govflow_admin")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY", "govflow_secret")
        
        client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False
        )
        
        bucket_name = "govflow-documents"
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        client.put_object(
            bucket_name,
            object_key,
            io.BytesIO(pdf_bytes),
            length=len(pdf_bytes),
            content_type="application/pdf"
        )
        
        return object_key
