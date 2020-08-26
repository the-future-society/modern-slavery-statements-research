
import boto3
import os
import argparse
import logging

logger = logging.getLogger()


def get_arguments():
    """
    Parses CLI argumenst
    Returns: parsed arguments
    """

    parser = argparse.ArgumentParser(description="Dowloads the modern slavery corpus from AWS S3 ")
    # parser.add_argument('--csv', store=True, help="Provides the aws access key id", required=False)
    parser.add_argument('--json', action='store_true', help="Provides the aws secret access key")
    args = parser.parse_args("--json".split())
    # args = parser.parse_args("")

    return args


def download_from_s3():

    args = get_arguments()

    s3_bucket = 'modern-slavery-dataset'

    s3_client = boto3.client('s3')

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

    logger.info("Fetching data ...")
    if args.json:
        s3_client.download_file(Bucket=s3_bucket, Key='modern_slavery_dataset.json',
                                Filename='data/modern_slavery_dataset.json')
        logger.info("Saved data/modern_slavery_dataset.json")
    else:
        s3_client.download_file(Bucket=s3_bucket, Key='modern_slavery_dataset.csv',
                                Filename='data/modern_slavery_dataset.csv')
        logger.info("Saved data/modern_slavery_dataset.csv")

if __name__ == '__main__':

    download_from_s3()
