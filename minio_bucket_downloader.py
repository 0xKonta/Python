import os
import argparse
from minio import Minio
from tqdm import tqdm
import urllib3

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download a MinIO bucket")
    parser.add_argument("--endpoint", help="MinIO endpoint")
    parser.add_argument("--access_key", help="MinIO access key")
    parser.add_argument("--secret_key", help="MinIO secret key")
    parser.add_argument("--bucket", help="Bucket name")
    parser.add_argument("--directory", help="Local directory for download")
    return parser.parse_args()

def get_user_input(prompt):
    return input(f"{prompt}: ").strip()

def create_minio_client(endpoint, access_key, secret_key):
    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

def download_object(client, bucket_name, obj, local_directory, file_pbar, size_pbar):
    object_name = obj.object_name
    object_size = obj.size
    local_file_path = os.path.join(local_directory, object_name)
    
    ensure_directory_exists(os.path.dirname(local_file_path))
    
    client.fget_object(bucket_name, object_name, local_file_path)
    file_pbar.update(1)
    size_pbar.update(object_size)

def download_bucket(endpoint, access_key, secret_key, bucket_name, local_directory):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = create_minio_client(endpoint, access_key, secret_key)

    try:
        if not client.bucket_exists(bucket_name):
            print(f"Error: Bucket '{bucket_name}' does not exist.")
            return

        objects = list(client.list_objects(bucket_name, recursive=True))
        total_objects = len(objects)
        total_size = sum(obj.size for obj in objects)

        with tqdm(total=total_objects, unit="file", desc="Files") as file_pbar, \
             tqdm(total=total_size, unit="B", unit_scale=True, desc="Total Size", miniters=1) as size_pbar:
            for obj in objects:
                download_object(client, bucket_name, obj, local_directory, file_pbar, size_pbar)

        print("\nDownload completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    args = parse_arguments()

    endpoint = args.endpoint or get_user_input("Enter MinIO endpoint")
    access_key = args.access_key or get_user_input("Enter access key")
    secret_key = args.secret_key or get_user_input("Enter secret key")
    bucket_name = args.bucket or get_user_input("Enter bucket name")
    local_directory = args.directory or get_user_input("Enter local directory for download")

    print("\nStarting MinIO Bucket Download...")
    download_bucket(endpoint, access_key, secret_key, bucket_name, local_directory)

if __name__ == "__main__":
    main()
