def upload_blob(bucket_name, source_file_name, destination_blob_name, storage_client):
    """Uploads a file to the bucket."""
    print("[LOG]: START UPLOADING ({}) at bucket: {}".format(source_file_name, bucket_name))
    bucket_ = storage_client.bucket(bucket_name)
    blob = bucket_.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "[LOG]: File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

    