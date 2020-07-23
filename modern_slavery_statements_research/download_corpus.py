import argparse
import boto3
from collections import defaultdict
import pandas as pd
from os import path, makedirs, scandir, path
from tqdm import tqdm
import re
import logging
from itertools import chain


logger = logging.getLogger(__name__)

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# noinspection PyArgumentList
logging.basicConfig(level=logging.INFO,
                    format=log_fmt
                    )

def get_arguments():
    """
    Parses CLI argumenst
    Returns: parsed arguments
    """

    parser = argparse.ArgumentParser(description="Dowloads the latest documents from AWS S3 ")
    parser.add_argument('-i', type=str, help="Provides the aws access key id", required=False)
    parser.add_argument('-a', type=str, help="Provides the aws secret access key", required=False)
    parser.add_argument('-b', type=str, help="Provide filename to bucket name file,"
                                             "default = modern-slavery-dataset-txt",
                        default="modern-slavery-dataset-txt", required=False)
    parser.add_argument('-m', type=str, help="Provides metadata for each file outputed",
                        default="./metadatas.csv", required=False)
    parser.add_argument('--only_m', type=bool, help="Whether of not we want to output only metadatas" 
                                                    "and not all files, default=false",
                        default=False)
    args = parser.parse_args()

    return args


def get_aws_creds_from_session():
    """
    Gets AWS access credentials from the session to avoid having to print them in the console.
    :return: str aws_access_aws_access_key_id, aws_secret_access_key
    """

    session = boto3.Session()
    credentials = session.get_credentials()

    # Credentials are refreshable, so accessing your access key / secret key
    # separately can lead to a race condition. Use this to get an actual matched
    # set.
    credentials = credentials.get_frozen_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    return aws_access_key_id, aws_secret_access_key


def get_bucket_client(aws_access_key_id, aws_secret_access_key):
    client = boto3.client('s3',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)
    return client

def get_bucket_from_resource(bucket_name, aws_access_key_id, aws_secret_access_key):
    resource = boto3.resource('s3',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)
    return resource.Bucket(bucket_name)

def get_first_folder_name(objects):
    return f"{objects[0].split('/')[0]}/"

def get_latest_folder_name(bucket_name, aws_access_key_id, aws_secret_access_key):
    """
    Gets all objects in the given bucket 
    Finds the latest ones
    Returns the folder name of the latests objects

    Args:
        bucket_name (str): bucket name in which to download files

    Returns:
        str: latest modified folder name 
    """
    # client = get_bucket_client(aws_access_key_id, aws_secret_access_key)
    # objects = client.list_objects_v2(Bucket=bucket_name)['Contents']
    # get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    #
    # sorted_objects = [obj['Key'] for obj in sorted(objects, key=get_last_modified, reverse=True)]
    # folder_name = get_first_folder_name(sorted_objects)


    s3r = boto3.resource('s3',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)
    bucket = s3r.Bucket(bucket_name)
    logger.info("Identifying the most recent data folder...")
    files_in_bucket = list(bucket.objects.all())
    sorted_folder_names = sorted([re.sub(r'/.+', '', file.key) for file in files_in_bucket], reverse=True)
    folder_name = get_first_folder_name(sorted_folder_names)
    # latest_folder_name = sorted_folder_names[0]

    logger.info(f"Storing local data in {folder_name}")
    if not path.exists(path.dirname(folder_name)):
        makedirs(path.dirname(folder_name))
        # logger.info(f"Storing local data in {folder_name}")
    return folder_name

def get_metadatas(obj):
    """Searches for all metadatas given for one object

    Args:
        obj (ObjectSummary): one S3 object

    Returns:
       defaultdict : each metadata info is stored in this defaultdict
    """
    metadatas = defaultdict(str)
    metadatas["bucket_name"] = obj.bucket_name
    metadatas["filename"] = obj.key
    metadatas["size"] = str(obj.size)
    metadatas["last_modified"] = str(obj.last_modified)
    metadatas["owner_name"] = str(obj.owner["DisplayName"])
    metadatas["owner_id"] = str(obj.owner["ID"])
    metadatas["storage_class"] = str(obj.storage_class)
    return metadatas

def download(bucket_name='modern-slavery-dataset-txt', metadata_path='./metadatas.csv', only_metadata=False, aws_access_key_id=None, aws_secret_access_key=None):
    """The main function of this file
    Downloads the latest files modified in the given bucket
    Writes a csv file containing all info from each downloaded file
    Args: command line arguments
    """

    if (not aws_access_key_id or not aws_secret_access_key):
        aws_access_key_id, aws_secret_access_key = get_aws_creds_from_session()

    remote_directory = get_latest_folder_name(bucket_name, aws_access_key_id, aws_secret_access_key)
    bucket = get_bucket_from_resource(bucket_name, aws_access_key_id, aws_secret_access_key)
    metadatas = []
    for obj in tqdm(bucket.objects.filter(Prefix = remote_directory)):
        if only_metadata == False:
            bucket.download_file(obj.key, obj.key)
        metadatas.append(get_metadatas(obj))

    df = pd.DataFrame(metadatas)
    df.to_csv(metadata_path)

    logger.info("Download finished.")


def transform(path_to_scraper_run_dir, output_format='pandas_dataframe'):
    """
    Takes a path to a directory of modern slavery statements in .txt format,
    transforms them to a pandas dataframe then pickles and saves the dataframe
    as 'ms_statements_pd.pkl'.
    The pickled dataframe can be read in Python as follows:
    df = pd.read_pickle('ms_statements_pd.pkl')
        
    Args:
        path_to_scraper_run_dir (str): absolute or relative path to the
            directory containing modern slavery statements as .txt files,
            obtained by calling download()
        format (str): format for saving the transformed statements.
            Currrently, the default 'pandas_dataframe' is the only option.
    """
    assert path.isdir(path_to_scraper_run_dir), \
        "{} is not a valid path to the directory scraper_run!".format(
            path_to_scraper_run_dir
        )
    assert output_format == 'pandas_dataframe', \
        "pandas_dataframe is currently the only supported output format"

    data = []
    with scandir(path_to_scraper_run_dir) as iterator:
        for txt_file in tqdm(iterator):
            assert txt_file.is_file()
            assert txt_file.name.endswith(".txt")
            with open(txt_file.path, encoding="utf8") as f:
                words = list(chain.from_iterable(map(str.split, f)))
                datum = {
                    'url_id': txt_file.name.strip('.txt'),
                    'word_count': int(len(words)),
                    'contents': ' '.join(words) # remove commas from python list
                }
                data.append(datum)

    df = pd.DataFrame(data)
    df.to_pickle('ms_statements_pd.pkl')


def main():
    args = get_arguments()
    download(args.b, args.m, args.only_m, args.i, args.a)


if __name__ == '__main__':
    main()

