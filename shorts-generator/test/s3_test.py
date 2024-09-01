import unittest

import boto3

from config import Config


class S3Test(unittest.TestCase):
    def test_s3_client(self):
        s3_client = boto3.client("s3",
                             region_name=Config.region(),
                             aws_access_key_id=Config.aws_access_key(),
                             aws_secret_access_key=Config.aws_secret_key())
        response = s3_client.list_buckets(MaxBuckets=123)
        expected: str = "video-process-test-bucket"
        bucket_name: str = response['Buckets'][0]['Name']

        self.assertEqual(expected, bucket_name)

if __name__ == '__main__':
    unittest.main()
