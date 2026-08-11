from google.cloud import storage
from datetime import datetime, timezone
import os


SOURCE_BUCKET = "ccit-source-bucket" #os.environ["SOURCE_BUCKET"]
REPORT_BUCKET = "ccit-reports-bucket" #os.environ["REPORT_BUCKET"]


def main():

    print("==========================================")
    print("Cloud Run Bucket Statistics Job")
    print("==========================================")

    print(f"Source Bucket : {SOURCE_BUCKET}")
    print(f"Report Bucket : {REPORT_BUCKET}")

    client = storage.Client()

    source_bucket = client.bucket(SOURCE_BUCKET)
    report_bucket = client.bucket(REPORT_BUCKET)

    # Get all objects
    blobs = list(client.list_blobs(SOURCE_BUCKET))

    object_count = len(blobs)

    total_size = sum(blob.size or 0 for blob in blobs)

    total_size_mb = total_size / (1024 * 1024)

    print()
    print("Bucket Statistics")
    print("-----------------")

    print(f"Number of objects : {object_count}")
    print(f"Total size        : {total_size_mb:.2f} MB")

    # Generate report
    timestamp = datetime.now(timezone.utc)

    report = []

    report.append("Bucket Statistics")
    report.append("=================")
    report.append("")

    report.append(f"Bucket: {SOURCE_BUCKET}")
    report.append(
        f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    report.append("")

    report.append(f"Number of objects: {object_count}")
    report.append(f"Total size: {total_size_mb:.2f} MB")

    report.append("")
    report.append("Objects")
    report.append("--------------------------------")

    for blob in blobs:

        size_mb = (blob.size or 0) / (1024 * 1024)

        report.append(
            f"{blob.name}    {size_mb:.2f} MB"
        )

    report_content = "\n".join(report)

    # Generate filename
    filename = (
        f"bucket_stats_"
        f"{timestamp.strftime('%Y-%m-%d_%H%M%S')}.txt"
    )

    # Upload report
    report_blob = report_bucket.blob(filename)

    report_blob.upload_from_string(
        report_content,
        content_type="text/plain"
    )

    print()
    print("Report uploaded successfully!")
    print(f"gs://{REPORT_BUCKET}/{filename}")

    print()
    print("Job completed successfully.")


if __name__ == "__main__":
    main()
