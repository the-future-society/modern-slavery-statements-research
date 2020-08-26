
import boto3
import os
import argparse
import logging
import sys


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

    parser = argparse.ArgumentParser(description="Downloads the modern slavery corpus from AWS S3. Defaults to downloading a CSV.")
    # parser.add_argument('--csv', store=True, help="Provides the aws access key id", required=False)
    parser.add_argument('--json', action='store_true', help="Specify if you'd like to download the data in a JSON format instead")
    parser.add_argument('-i', type=str, help="Provide the aws access key id, without quotes", required=False)
    parser.add_argument('-a', type=str, help="Provide the aws secret access key, without quotes", required=False)
    # args = parser.parse_args("--json".split())
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


def download_from_s3():

    args = get_arguments()

    aws_access_key_id = args.i
    aws_secret_access_key = args.a
    json = args.json

    try:
        if (not aws_access_key_id or not aws_secret_access_key):
            aws_access_key_id, aws_secret_access_key = get_aws_creds_from_session()
    except:
        print("You need to provide credetials as command line arguments. Check download-corpus --help")
        sys.exit()


    s3_bucket = 'modern-slavery-dataset'

    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

    # response = s3_client.list_objects_v2(Bucket=s3_bucket)

    # print("Modern Slavery Text Corpus is available in the following formats: \n")
    #
    # contents = response.get('Contents')
    # for file in contents:
    #     print(file['Key'])

    # Create a /data/ directory if it doesn't exist already
    if not os.path.exists('data'):
        os.makedirs('data')
        print('Created a directory "/data/" in your current directory.')

    logger.info("Fetching data ... Gather patience as the file size is ~130MB.")
    if json:
        try:
            s3_client.download_file(Bucket=s3_bucket, Key='modern_slavery_dataset.json',
                                    Filename='data/modern_slavery_dataset.json')
            logger.info("Saved data/modern_slavery_dataset.json")

        except:
            logger.info("No data downloaded due to incorrect credentials. Check download-corpus --help")
    else:
        try:

            s3_client.download_file(Bucket=s3_bucket, Key='modern_slavery_dataset.csv',
                                    Filename='data/modern_slavery_dataset.csv')
            logger.info("Saved data/modern_slavery_dataset.csv")

        except:
            logger.info("No data downloaded due to incorrect credentials. Check download-corpus --help")

if __name__ == '__main__':
    args = get_arguments()
    download_from_s3(args.i, args.a, args.json)
