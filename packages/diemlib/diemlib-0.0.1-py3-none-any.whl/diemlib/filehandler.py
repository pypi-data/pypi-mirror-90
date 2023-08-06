#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...
"""

import ibm_boto3
import io
from ibm_botocore.client import Config, ClientError
import pandas as pd
from pathlib import Path
from diemlib.main import *


class filehandler(object):
    def __init__(self, cos):
        self.ibm_api_key_id = cos["__ibm_api_key_id"]
        self.ibm_service_instance_id = cos["__ibm_service_instance_id"]
        self.ibm_auth_endpoint = "https://iam.cloud.ibm.com/identity/token"
        self.endpoint_url = cos["__endpoint_url"]
        self.Bucket = cos["__Bucket"]

    def connect(self):

        try:

            s3c = ibm_boto3.client(
                "s3",
                ibm_api_key_id=self.ibm_api_key_id,
                ibm_service_instance_id=self.ibm_service_instance_id,
                ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
                config=Config(signature_version="oauth"),
                endpoint_url=self.endpoint_url,
            )
            return s3c

        except Exception as e:
            error(e)
            raise

    def saveLocal(self, file_name, file_body):
        with open("%s" % file_name, "w") as fout:
            fout.write(file_body)

    def saveFile(self, file_name, file_body, **kwargs):

        file_path = file_name

        if "file" in kwargs:
            file_path = kwargs.get("file")
            print(f"Using custom directory {file_path} to disk")

        if file_body:
            print(f"Saving local file {file_name} to disk")

            self.saveLocal(file_name, file_body)

        s3c = self.connect()

        print(f"Starting large file upload for {file_name} to bucket: {self.Bucket}")
        # set the chunk size to 5 MB
        part_size = 1024 * 1024 * 5

        # set threadhold to 5 MB
        file_threshold = 1024 * 1024 * 5

        # set the transfer threshold and chunk size in config settings
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold, multipart_chunksize=part_size
        )

        # create transfer manager
        transfer_mgr = ibm_boto3.s3.transfer.TransferManager(
            s3c, config=transfer_config
        )

        try:
            # initiate file upload
            future = transfer_mgr.upload(file_path, self.Bucket, file_name)

            # wait for upload to complete
            future.result()

            print("Large file upload complete!")
        except Exception as e:
            error(e)
        finally:
            transfer_mgr.shutdown()

    def getFile(self, file, **kwargs):

        try:

            s3c = self.connect()
            obj = s3c.get_object(Bucket=self.Bucket, Key=file)
            type = Path(file).suffix

            if type == ".pickle":
                df = pd.read_pickle(io.BytesIO(obj["Body"].read()))
                return df
            elif type == ".parquet":
                df = pd.read_parquet(io.BytesIO(obj["Body"].read()), **kwargs)
                return df
            else:
                df = pd.read_csv(
                    io.BytesIO(obj["Body"].read()), encoding="utf8", **kwargs
                )
            return df

        except Exception as e:
            error(e)
            raise
