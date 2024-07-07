# MinIO Bucket Downloader

This Python script allows you to download an entire bucket from a MinIO server. It provides a command-line interface and interactive prompts for easy use.

## Prerequisites

- Python 3.6 or higher
- `minio` Python package
- `tqdm` Python package
  
```
pip install minio tqdm
```

## Usage

You can run the script in two ways:

```
python minio_bucket_downloader.py --endpoint <endpoint> --access_key <access_key> --secret_key <secret_key> --bucket <bucket_name> --directory <local_directory>
```

Replace the placeholders with your actual MinIO server details and desired local directory.

Simply run the script without any arguments:

```
python minio_bucket_downloader.py
```

The script will prompt you for the necessary information:

- MinIO endpoint
- Access key
- Secret key
- Bucket name
- Local directory for download

## Parameters

- `endpoint`: The MinIO server endpoint (e.g., "play.min.io:9000")
- `access_key`: Your MinIO access key
- `secret_key`: Your MinIO secret key
- `bucket`: The name of the bucket you want to download
- `directory`: The local directory where files will be downloaded

## Notes

- The script uses HTTP by default. If your MinIO server requires HTTPS, you'll need to modify the `create_minio_client` function in the script.
- Make sure you have sufficient permissions to access the specified bucket and to write to the local directory.
- Large buckets may take a significant amount of time to download. The progress bars will keep you informed of the download progress.

