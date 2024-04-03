# import boto3
# from botocore.exceptions import ClientError
#
# from exceptions import Forbidden, NoSuchBucket
#
#
# class AwesomeS3Client:
#     def __init__(self, s3_api_url: str, access_key: str, secret_key: str, bucket: str):
#         self._s3_api_url = s3_api_url
#         self._access_key = access_key
#         self._secret_key = secret_key
#         self._bucket = bucket
#         self._setup_client()
#
#     def _setup_client(self):
#         self._client = boto3.client(
#             "s3",
#             endpoint_url=self._s3_api_url,
#             aws_access_key_id=self._access_key,
#             aws_secret_access_key=self._secret_key,
#         )
#         try:
#             self._client.head_bucket(Bucket=self._bucket)
#         except ClientError as error:
#             if error.response["Error"]["Code"] == "403":
#                 raise Forbidden
#             if error.response["Error"]["Code"] == "NoSuchBucket":
#                 raise NoSuchBucket
#
#     def list_objects(self):
#         return self._client.list_objects_v2(Bucket=self._bucket)["Contents"]
#
#     def get_object(self, key):
#         return self._client.get_object(Bucket=self._bucket, Key=key)["Body"]
import asyncio
from asyncio.exceptions import TimeoutError as ddd
from time import time
s = time()
async def delay(n):
    print('sleep start', time() - s)
    await asyncio.sleep(n)
    print('sleep end', time() - s)
    return n
async def main():
    task = asyncio.create_task(delay(10))
    try:
        await asyncio.wait_for(asyncio.shield(task), 5)
    except ddd:
        print('задача более 5', time() - s)
        result = await task
        print(result, time() - s)
asyncio.run(main())

asyncio.run(main())
