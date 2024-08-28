import unittest

import boto3


class MyTestCase(unittest.TestCase):
    def test_s3_client(self):
        s3_client = boto3.client("s3",
                             region_name="ap-northeast-2",
                             aws_access_key_id='AKIA6GBMEHUUKC7J7Y53',
                             aws_secret_access_key='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')
        response = s3_client.list_buckets(MaxBuckets=123)
        print(response['Buckets'][0]['Name'])

if __name__ == '__main__':
    unittest.main()
