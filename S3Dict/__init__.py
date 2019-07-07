import collections
import traceback
import json

import time

from loguru import logger
import boto3
from botocore.client import Config


class S3Dict(collections.UserDict):
    def __init__(
        self,
        bucket_name=None,
        access_key_id=None,
        access_secret_key=None,
        file_name=None,
        autosave = False,
        data={},
    ):
        logger.debug(
            f"__init__: {bucket_name} {access_key_id} {access_secret_key} {file_name} {autosave} {data}"
        )
        if (
            bucket_name == None
            or access_key_id == None
            or access_secret_key == None
            or file_name == None
        ):
            raise ValueError(
                f"bucket_name ({bucket_name}), access_key_id ({access_key_id}),"
                + f" access_secret_key ({access_secret_key}), and file_name ({file_name}) must be specified"
            )

        self.__autosave = autosave
        self.__fname = file_name
        self.__BUCKET_NAME = bucket_name
        self.__AWS_ACCESS_KEY_ID = access_key_id
        self.__AWS_SECRET_ACCESS_KEY = access_secret_key
        self.__s3 = boto3.resource(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_secret_key,
            config=Config(signature_version="s3v4"),
        )

        # TODO: logic to either load state or preserve state depending on data
        self.__loadstate()
        self.data = data
        self.__savestate()

    def save(self):
        self.__savestate(True)

    @property
    def autosave(self):
        return self.__autosave
    
    @autosave.setter
    def autosave(self,val):
        if isinstance(val,bool):
            self.__autosave = val
        else:
            raise ValueError("autosave must be type bool")

    @property
    def file_name(self):
        return self.__fname

    @property
    def access_key_id(self):
        return self.__AWS_ACCESS_KEY_ID
    
    @property
    def access_secret_key(self):
        return self.__AWS_SECRET_ACCESS_KEY

    @property
    def bucket_name(self):
        return self.__BUCKET_NAME

    def __loadstate(self):
        state = {}
        objs = self.__s3.Bucket(self.__BUCKET_NAME).objects.all()
        fnames = list(map(lambda x: x.key, objs))
        logger.debug(f"fnames: {fnames}")

        if self.__fname in fnames:
            try:
                obj = self.__s3.Object(self.__BUCKET_NAME, self.__fname)
                data = obj.get()["Body"].read()
                state = json.loads(data)
                logger.debug(f"data: {data}, state: {state}")
            except Exception as e:
                logger.debug(
                    f"Error loading state from {self.__s3}: {e} {traceback.print_exc}"
                )
                # couldn't find the state file on s3 bucket so initialize state
        else:
            try:
                logger.debug(f"{self.__fname} not in bucket, creating it")
                data = json.dumps(state)
                self.__s3.Bucket(self.__BUCKET_NAME).put_object(
                    Key=self.__fname, Body=data
                )
            except Exception as e:
                logger.debug(
                    f"Error creating {self.__fname} {self.__s3}: {e} {traceback.print_exc}"
                )

        self.data = state

    def __savestate(self, savenow = False):
        # Don't save unless savenow = True
        # if autosave is True, always save
        
        savenow = savenow or self.__autosave
        if not savenow:
            logger.debug("skipping saving")
            return 

        logger.debug("savestate")
        start = time.clock()
        try:
            data = json.dumps(self.data)
            self.__s3.Bucket(self.__BUCKET_NAME).put_object(Key=self.__fname, Body=data)
        except:
            quit(f"Error saving state to {self.__s3}")
        stop = time.clock()
        elapsed = stop - start
        logger.debug(f"elapsed: {elapsed}")

    def fromkeys(self, *args):
        logger.debug(f"fromkeys: {args}")
        newdict = S3Dict(
            bucket_name=self.__BUCKET_NAME,
            access_key_id=self.__AWS_ACCESS_KEY_ID,
            access_secret_key=self.__AWS_SECRET_ACCESS_KEY,
            file_name=self.__fname,
            autosave=self.__autosave,
            data=dict.fromkeys(*args),
        )
        return newdict

    def __getitem__(self, key):
        logger.debug(f"__getitem__: {key}")
        return self.data[key]

    def __setitem__(self, key, val):
        logger.debug(f"__setitem__: {key} {val}")
        self.data[key] = val
        self.__savestate()

    def __iter__(self):
        logger.debug(f"__iter__:")
        return iter(self.data)

    def __len__(self):
        logger.debug(f"__len__:")
        return len(self.data)

    def __delitem__(self, key):
        logger.debug(f"__delitem__: {key}")
        del (self.data[key])
        self.__savestate()
