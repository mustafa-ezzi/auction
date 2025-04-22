import boto3
import uuid
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Read environment variables from .env
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)


def parse_s3_url(image_url):
    parsed_url = urlparse(image_url)
    object_key = parsed_url.path.lstrip("/")
    return object_key


def upload_player_to_s3(image_path, project_id, is_path):

    try:
        if is_path:
            id = str(uuid.uuid4()) + "." + image_path.split(".")[-1]
            s3_object_key = f"projects/{project_id}/players/{id}"
            s3_client.upload_file(image_path, BUCKET_NAME, s3_object_key)
        else:
            id = str(uuid.uuid4()) + "." + image_path.name.split(".")[-1]
            s3_object_key = f"projects/{project_id}/players/{id}"
            s3_client.upload_fileobj(image_path, BUCKET_NAME, s3_object_key)

        s3_image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_object_key}"

        return s3_image_url

    except Exception as e:
        print(e)
        return None


def upload_team_to_s3(image_file, project_id, team_id):

    id = str(uuid.uuid4()) + "." + image_file.name.split(".")[-1]

    s3_object_key = f"projects/{project_id}/teams/{team_id}/{id}"

    try:
        s3_client.upload_fileobj(image_file, BUCKET_NAME, s3_object_key)

        s3_image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_object_key}"
        return s3_image_url

    except Exception as e:
        print(e)
        return None


def upload_settings_to_s3(image_file, project_id):

    id = str(uuid.uuid4()) + "." + image_file.name.split(".")[-1]

    s3_object_key = f"projects/{project_id}/settings/{id}"

    try:
        s3_client.upload_fileobj(image_file, BUCKET_NAME, s3_object_key)

        s3_image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_object_key}"
        return s3_image_url

    except Exception as e:
        print(e)
        return None


def delete_project_from_s3(project_id):

    s3_folder_prefix = f"projects/{project_id}/"

    try:

        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=s3_folder_prefix
        )

        if "Contents" in response:
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_folder_prefix)

        return True

    except Exception as e:
        print(e)
        return False


def delete_team_from_s3(project_id, team_id):

    s3_folder_prefix = f"projects/{project_id}/teams/{team_id}"

    try:

        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=s3_folder_prefix
        )

        if "Contents" in response:
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_folder_prefix)

        return True

    except Exception as e:
        print(e)
        return False


def delete_player_from_s3(project_id, filename):

    s3_folder_prefix = f"projects/{project_id}/players/{filename}"

    try:

        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix=s3_folder_prefix
        )

        if "Contents" in response:
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_folder_prefix)

        return True

    except Exception as e:
        print(e)
        return False


def delete_key_from_s3(s3_path):

    try:
        object_key = parse_s3_url(s3_path)
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_key)

        return True

    except Exception as e:
        print(e)
        return False
