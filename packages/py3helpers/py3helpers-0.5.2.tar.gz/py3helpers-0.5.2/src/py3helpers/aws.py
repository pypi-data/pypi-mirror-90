#!/usr/bin/env python
"""Aws s3 interaction helper functions"""
########################################################################
# File: aws.py
#  executable: aws.py
#
# Author: Andrew Bailey
# History: 03/27/19 Created
########################################################################

import math
# built in
import os
import warnings
from concurrent.futures import ProcessPoolExecutor

# boto3
import boto3
import botocore


class S3Client(object):

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, profile_name=None):
        """
        Gets an instance of boto3 s3 client. Check default env variables
        for credentials.
        """
        self.session = boto3.Session(profile_name=profile_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     aws_session_token=aws_session_token)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.profile_name = profile_name
        self.s3_resource = self.session.resource('s3')
        self.s3_client = self.session.client('s3')
        self.connected = self.setup()

    def setup(self):
        """Hide unnecessary warnings"""
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        try:
            self.s3_resource.buckets.all().__next__()
            self.s3_client.list_buckets().__next__()
        except Exception:
            return False
        return True


class AwsS3(S3Client):
    """Class to deal with getting information from aws s3"""

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None,
                 profile_name="default", time=3600):
        try:
            session = botocore.session.get_session()
            client = session.create_client("sts")
            profile = session.full_config["profiles"]
            self.mp_ok = False
            if profile_name in profile:
                if "role_arn" in profile[profile_name]:
                    self.mp_ok = True
                    role_arn = profile[profile_name]["role_arn"]
                    response = client.assume_role(
                        RoleArn=role_arn,
                        RoleSessionName='AwsS3',
                        DurationSeconds=time)
                    aws_access_key_id = response["Credentials"]["AccessKeyId"]
                    aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
                    aws_session_token = response["Credentials"]["SessionToken"]
            else:
                profile_name = None
        except (botocore.exceptions.ProfileNotFound, botocore.exceptions.ClientError):
            pass
        super().__init__(aws_access_key_id, aws_secret_access_key, aws_session_token, profile_name)

    def download_object(self, path, dest):
        """Download file from specified path
        :param path: path to file
        :param dest: path to directory or renamed file output
        """
        bucket, key = self.split_name(path)
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(key))
        assert os.path.exists(os.path.dirname(dest)), \
            "Destination directory does not exist: {}".format(os.path.dirname(dest))
        try:
            self.s3_resource.Bucket(bucket).download_file(key, dest)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "403" or \
                    e.response['Error']['Code'] == 'NoSuchKey':
                print("The object does not exist. {}".format(path))
                dest = False
            elif e.response['Error']['Code'] == 'NoSuchBucket':
                print("The Bucket not exist. {}".format(bucket))
                dest = False
            else:
                raise e
        return dest

    def multiprocess_download_files(self, paths, dest, n_workers=2):
        """Multiprocess download files

        Thanks to https://github.com/chasenicholl/boto3m for the inspiration and alot of the code for this function
        """

        n = math.ceil(len(paths) / n_workers)
        chunks = [paths[x:x + n] for x in range(0, len(paths), n)]

        futures = []
        with ProcessPoolExecutor(max_workers=len(chunks)) as executor:
            for chunk in chunks:
                resp = executor.submit(AwsS3.download_files,
                                       aws_access_key_id=self.aws_access_key_id,
                                       aws_secret_access_key=self.aws_secret_access_key,
                                       aws_session_token=self.aws_session_token,
                                       profile_name=self.profile_name,
                                       paths=chunk,
                                       dest=dest)
                futures.append(resp)

        # Collect results and return a list of file locations
        downloaded_files = []
        for future in futures:
            res = future.result()
            if isinstance(res, list):
                downloaded_files.extend(res)
        return downloaded_files

    @staticmethod
    def download_files(aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None,
                       profile_name="default", paths=None, dest=None):
        """
        Create a new Boto3 Session, and download chunk of files.
        Auto create folders along the way.
        """
        resource = S3Client(aws_access_key_id, aws_secret_access_key, aws_session_token, profile_name).s3_resource
        files = []
        assert os.path.isdir(dest), \
            "Destination directory is not a directory or does not exist: {}".format(dest)

        for path in paths:
            bucket, key = AwsS3.split_name(path)
            out_file = os.path.join(dest, os.path.basename(key))
            try:
                resource.Bucket(bucket).download_file(key, out_file)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "403" or \
                        e.response['Error']['Code'] == 'NoSuchKey':
                    print("The object does not exist. {}".format(path))
                    out_file = False
                elif e.response['Error']['Code'] == 'NoSuchBucket':
                    print("The Bucket not exist. {}".format(bucket))
                    out_file = False
                else:
                    raise e
            files.append(out_file)
        return files

    def upload_object(self, file_path, destination, use_original_name=True, ExtraArgs=None):
        """Upload a file to s3 bucket
        :param use_original_name: boolean option to use the basename of original file
        :param file_path: path to file to upload
        :param destination: location to place file
        :param ExtraArgs: dictionary of extra arguments for data object
        :return: True
        """
        assert os.path.exists(file_path), "File path does not exist {}".format(file_path)
        bucket_name, save_path = self.split_name(destination)
        if use_original_name:
            save_path = os.path.join(save_path, os.path.basename(file_path))

        self.s3_client.upload_file(file_path, bucket_name, save_path, ExtraArgs=ExtraArgs)
        return os.path.join(bucket_name, save_path)

    def create_bucket(self, bucket_name, region="us-west-2"):
        """Create a bucket
        :param bucket_name: name of bucket
        :param region: region to place bucket
        """
        self.s3_resource.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region})
        return True

    def delete_bucket(self, bucket_name):
        """Delete a bucket
        :param bucket_name: name of bucket to delete
        :return: True
        """
        bucket = self.s3_resource.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
        return True

    def bucket_exists(self, bucket_name):
        """Check if bucket exists
        :param bucket_name: name of bucket to create
        :return: True if exists False if not
        """
        self.s3_resource.Bucket(bucket_name)
        exists = True
        try:
            self.s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404' or error_code == '403':
                exists = False
        return exists

    def object_exists(self, object_path):
        """Return True if object exists
        :param object_path: path to object
        """
        bucket_name, save_path = self.split_name(object_path)
        try:
            self.s3_resource.Object(bucket_name, save_path).load()
        except botocore.exceptions.ClientError:
            return False
        return True

    def delete_object(self, object_path):
        """Delete object in s3
        :param object_path: path to object to delete
        """
        bucket_name, save_path = self.split_name(object_path)
        self.s3_client.delete_object(Bucket=bucket_name, Key=save_path)
        return True

    @staticmethod
    def split_name(name):
        """Split a name to get bucket and key path
        :param name: path to bucket or key
        """
        split_name = [x for x in name.split("/") if x != '']
        bucket_name = split_name[0]
        key_path = "/".join(split_name[1:])
        return bucket_name, key_path

    def list_objects(self, path):
        """Return a list of full paths to objects within key or bucket
        :param path: path to bucket or key
        """
        return [x for x in self.list_objects_generator(path)]

    def folder_exists(self, path):
        """Check to see if folder exists
        :param path: path to folder
        """
        bucket_name, save_path = self.split_name(path)
        if self.bucket_exists(bucket_name):
            try:
                result = self.s3_client.list_objects(Bucket=bucket_name, Prefix=save_path)
                if result["Contents"]:
                    return True
            except (botocore.exceptions.ClientError, KeyError):
                # The object does not exist.
                return False
        return False

    def list_buckets(self):
        """List all bucket names accessible by s3 client"""
        return [x["Name"] for x in self.s3_client.list_buckets()["Buckets"]]

    def list_objects_generator(self, path, ext=""):
        """
        Generate objects in an S3 bucket.
        source: https://alexwlchan.net/2019/07/listing-s3-keys/
        :param path: path to folder
        :param ext: Only fetch objects whose keys end with
            this suffix (optional).
        """
        assert self.folder_exists(path), "AWS object '{}' does not exist".format(path)
        bucket, prefix = self.split_name(path)
        paginator = self.s3_client.get_paginator("list_objects")
        # take care of weird cases when a file has same prefix as a folder
        if len(prefix) > 0:
            prefix += "/"
        kwargs = {'Bucket': bucket}

        # We can pass the prefix directly to the S3 API.  If the user has passed
        # a tuple or list of prefixes, we go through them one by one.
        if isinstance(prefix, str):
            prefixes = (prefix,)
        else:
            prefixes = prefix

        for key_prefix in prefixes:
            kwargs["Prefix"] = key_prefix

            for page in paginator.paginate(**kwargs):
                try:
                    contents = page["Contents"]
                except KeyError:
                    return

                for obj in contents:
                    key = obj["Key"]
                    if key.endswith(ext) and not key.endswith("/"):
                        yield os.path.join(bucket, key)
