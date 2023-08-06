#!/usr/bin/env python

"""
Download a customer's upload files.

Try GCS, and if files are not there try S3.

"""
import binascii
import json
import os
import re
import sys

import boto3
from botocore.errorfactory import ClientError
from google.cloud import datastore, storage


def green(rhs):
    return "\033[92m{}\033[0m".format(rhs)


def red(rhs):
    return "\033[91m{}\033[0m".format(rhs)


DATASTORE_CLIENT = datastore.Client()
STORAGE_CLIENT = storage.Client()
S3_RESOURCE = boto3.resource('s3')
S3_CLIENT = boto3.client('s3')
PROJECT_NAME = "atomic-light-001"
GCS_BUCKET = "atomic-light-001"
AWS_BUCKET = "672025612811-prod-us-west-2-render-data"


def main():
    """
    Wizard to collect information required to download.

    Asks for Account: (name or account_id).
    Asks for Job ID (jid).
    Asks to confirm or change download directory.

    Then try GCS download. If it fails, try AWS download.
    """
    creds_warning()

    account_id, account_name = get_account()
    job_id, jid, upload_key = get_job(account_id)

    slug = os.path.join(account_name, jid)

    directory = get_destination(slug)

    if attempt_gcs_download(upload_key, account_id, job_id, directory):
        sys.exit(0)

    if attempt_aws_download(account_id, job_id, directory):
        sys.exit(0)

    print("""The script failed.
        One possible reason is that you have legacy Conductor installed.
        Legacy Conductor includes an old version of the requests library
        and inserts it into the PYTHONPATH. This interferes with the 
        version requred by the Google storage package. 
        Simply unset the PYTHONPATH or remove Conductor and try again.
        """)

    sys.exit(1)


def creds_warning():
    google_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not google_creds:
        print(red("Couldn't find your GOOGLE_APPLICATION_CREDENTIALS. See here: https://cloud.google.com/datastore/docs/reference/libraries"))
        get_option("Do you want to continue?", ["Abort", "Continue"])

    aws_creds_path = os.path.join(os.environ['HOME'], ".aws",  "credentials")
    if not os.path.exists(aws_creds_path):
        print(red("Couldn't find your AWS Credentials. See here: https://console.aws.amazon.com/iam/home?#/home"))
        get_option("Do you want to continue?", ["Abort", "Continue"])


def get_account():
    account = input(green("Enter the account name or number: "))
    query = DATASTORE_CLIENT.query(kind='Account')

    query.namespace = "accounts_service"
    field = "name"
    if account.isdigit():
        query.ancestor = datastore.key.Key("Account",  int(
            account), project=PROJECT_NAME, namespace="accounts_service")
        field = "ID"
    else:
        query.add_filter('name', '=', account)
    results = list(query.fetch())
    if not results:
        print(red("Couldn't find account by {}: {}. Exiting".format(field, account)))
        sys.exit(1)
    print("Found account. Name:{}, ID:{}".format(
        results[0]["name"], results[0].id))
    return results[0].id, results[0]["name"]


def get_job(account_id):
    jid = input(green("Enter the job ID:"))

    query = DATASTORE_CLIENT.query(kind='Job')
    query.add_filter('account_id', '=', str(account_id))
    query.add_filter('jid', '=', jid)
    results = list(query.fetch())

    if not results:
        print(red("Couldn't find job with jobID:{} and accountID:{}. Exiting".format(
            jid, account_id)))
        sys.exit(1)

    print("Found job. with jid:{}, ID:{}".format(
        results[0]["jid"], results[0].id))
    return results[0].id, results[0]["jid"], results[0]["upload"]


def attempt_gcs_download(upload_key, account_id, job_id, directory):
    gcs_files = get_gcs_files_blob(upload_key)
    if not gcs_files:
        print(red("There was a problem reading Google files blob for account/job: {}/{}, Checking Amazon...".format(account_id, job_id)))
        return False

    gcs_ok = gcs_files_exist(gcs_files, account_id)
    if not gcs_ok:
        print(red("Couldn't fetch files from Google for account/job: {}/{}, Checking Amazon...".format(account_id, job_id)))
        return False

    download_gcs_files(gcs_files, account_id, directory)
    return True


def attempt_aws_download(account_id, job_id, directory):

    aws_files = get_aws_files_blob(account_id, job_id)
    if not aws_files:
        print(red("Couldn't find Amazon files blob for account/job: {}/{}. Exiting".format(account_id, job_id)))
        return False

    aws_ok = aws_files_exist(aws_files)
    if not aws_ok:
        print(red("Upload files don't exist in Amazon account/job: {}/{}. Exiting".format(account_id, job_id)))
        return False

    download_aws_files(aws_files, directory)
    return True


def get_gcs_files_blob(upload_key):

    query = DATASTORE_CLIENT.query(kind='Upload')
    query.ancestor = upload_key
    results = list(query.fetch())
    if not results:
        return None

    blob_path = results[0]["files_blob"]
    print("Found GCS Files Blob:{}. Extracting files list JSON".format(blob_path))
    bucket = STORAGE_CLIENT.bucket(GCS_BUCKET)

    blob_name = blob_path.replace(GCS_BUCKET, "").strip("/")
    blob = bucket.blob(blob_name)
    result = json.loads(blob.download_as_string())
    try:
        result = json.loads(blob.download_as_string())
    except BaseException:
        return
    return result


def gcs_files_exist(gcs_files, account_id):
    if not len(gcs_files):
        return False

    # Just try the first entry from the blob and assume it represents all.
    blob_name = to_blob_name(gcs_files[0], account_id)

    if not blob_name:
        return False
    return gcs_file_exists(blob_name)


def gcs_file_exists(blob_name):
    bucket = STORAGE_CLIENT.bucket(GCS_BUCKET)
    return bucket.blob(blob_name).exists()


def get_aws_files_blob(account_id, job_id):
    key = "{}/jobs/{}/files.json".format(account_id, job_id)
    if not aws_file_exists(key):
        return
    obj = S3_RESOURCE.Object(AWS_BUCKET, key)
    body = obj.get()['Body'].read()
    return json.loads(body)["files"]


def aws_files_exist(aws_files):
    for url in aws_files.keys():
        # Just try the first entry from the blob and assume it represents all.
        key = url.replace("s3://", "").replace(AWS_BUCKET, "").strip("/")
        return aws_file_exists(key)


def aws_file_exists(key):
    try:
        S3_CLIENT.head_object(Bucket=AWS_BUCKET, Key=key)
        return True
    except ClientError:
        pass
    return False


def download_gcs_files(gcs_files, account_id, directory):
    print("Downloading files from GCP...")
    bucket = STORAGE_CLIENT.bucket(GCS_BUCKET)
    num_files = len(gcs_files)
    total_bytes = sum(b["st_size"] for b in gcs_files)
    dl_bytes = 0

    for i, entry in enumerate(gcs_files):
        ptg = ptg_fmt(dl_bytes, total_bytes)
        size = sizeof_fmt(entry["st_size"])
        fraction = "{}/{}".format(i+1, num_files).rjust(12)
        blob_name = to_blob_name(entry, account_id)
        dest_name = full_destination_path(directory, entry["destination"])
        ensure_directory_for(dest_name)

        print("{} {} {} {} -> {}".format(ptg, fraction, size, blob_name, dest_name))
        dl_bytes += entry["st_size"]
        try:
            bucket.blob(blob_name).download_to_filename(dest_name)
        except KeyboardInterrupt:
            print(red("Killed by user"))
            sys.exit(0)
        except (AttributeError, TypeError):
            print(red("Failed to download {} from Google. Skipping".format(dest_name)))
            continue
    print(green("Done downloading {} files from Google".format(num_files)))


def download_aws_files(aws_files, directory):
    print("Downloading files from AWS...")
    num_files = len(list(aws_files.keys()))
    total_bytes = sum(aws_files[k]["size"] for k in aws_files.keys())
    dl_bytes = 0
    for i, url in enumerate(aws_files.keys()):
        ptg = ptg_fmt(dl_bytes, total_bytes)
        size = sizeof_fmt(aws_files[url]["size"])
        fraction = "{}/{}".format(i+1, num_files).rjust(12)
        key = url.replace("s3://", "").replace(AWS_BUCKET, "").strip("/")
        dest_name = full_destination_path(
            directory, aws_files[url]["filename"])
        ensure_directory_for(dest_name)
        print("{} {} {} {} -> {}".format(ptg, fraction, size, key, dest_name))
        dl_bytes += aws_files[url]["size"]
        try:
            S3_CLIENT.download_file(AWS_BUCKET, key, dest_name)
        except KeyboardInterrupt:
            print(red("Killed by user"))
            sys.exit(0)
        except ClientError:
            print(red("Failed to download {} from Amazon. Skipping".format(dest_name)))
            continue
    print(green("Done downloading {} files from Amazon".format(num_files)))


def full_destination_path(directory, orig_filename):
    dest_name = re.sub("[a-zA-Z]:/", "", orig_filename).strip("/")
    return os.path.join(directory, dest_name)


def get_destination(slug):
    prefix = os.path.join(os.getcwd(), slug)

    print(green("Hit return to use the default destination directory : {}".format(prefix)))
    print(green("Enter a relative path to add subdirectories. For example: Enter my_sub_dir to use {}".format(
        os.path.join(prefix, "my_sub_dir"))))
    print(green("Enter an absolute path if you want to ignore the default altogether. For example: /path/to/downloads/my_project."))

    directory = input(green(": "))
    if not os.path.isabs(directory):
        directory = os.path.join(prefix, directory)
    ensure_directory(directory)
    return directory


def ensure_directory_for(filename):
    directory = os.path.dirname(filename)
    ensure_directory(directory)


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise


def get_option(message, options):

    try:
        abort_index = [o.lower() for o in options].index("abort")
    except ValueError:
        abort_index = -1
    num_opts = len(options)
    while True:
        print(green(message))
        for i, opt in enumerate(options):
            print("{}:{}".format(i, opt))
        result = input(green("Enter a number: "))
        if not result.isdigit():
            print(red("Not a valid input, try again"))
            continue
        inp = int(result)

        if inp in range(num_opts):
            if inp == abort_index:
                sys.stderr.write("Aborted!\n")
                sys.exit(1)
            return inp


def to_blob_name(entry, account_id):
    bucket_name = PROJECT_NAME
    if "gcs_url" in entry:
        return entry["gcs_url"].replace(bucket_name, "").strip("/")
    elif "md5" in entry:
        object_md5 = binascii.b2a_hex(
            binascii.a2b_base64(entry["md5"])).decode()
        return "accounts/{}/hashstore/{}".format(account_id, object_md5)
    else:
        return False


def ptg_fmt(n, d):
    return "{0:5.1f}%".format((n * 100.0) / d)


def sizeof_fmt(num):
    for unit in ['b ', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb']:
        if abs(num) < 1024.0:
            return "{:.1f} {}".format(num, unit).rjust(10)
        num /= 1024.0
    return "{:.1f} {}".format(num, "Yb").rjust(10)


if __name__ == '__main__':
    main()
