import collections
import traceback
import json

# from loguru import logger
import boto3
from botocore.client import Config


class S3Dict(collections.UserDict):
    def __init__(
        self,
        bucket_name=None,
        access_key_id=None,
        access_secret_key=None,
        file_name=None,
        autosave=False,
        data=None,
    ):
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

        self.__loadstate()
        if data is not None:
            # initialize with data that was passed to __init__
            self.data = data
        self.__savestate()

    def save(self):
        """ force state to be saved to S3"""
        self.__savestate(True)

    def load(self):
        """ force state to be loaded from S3 """
        self.__loadstate()

    @property
    def autosave(self):
        return self.__autosave

    @autosave.setter
    def autosave(self, val):
        if isinstance(val, bool):
            self.__autosave = val
            # if autosave turned on, save now
            if self.__autosave:
                self.save()
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
        """ loads state from json file 
            if file does not exists, creates the file """
        # TODO: might be better if __loadstate only loads and does not create the file if needed
        state = {}
        objs = self.__s3.Bucket(self.__BUCKET_NAME).objects.all()
        fnames = list(map(lambda x: x.key, objs))

        if self.__fname in fnames:
            try:
                obj = self.__s3.Object(self.__BUCKET_NAME, self.__fname)
                data = obj.get()["Body"].read()
                state = json.loads(data)
            except Exception as e:
                raise Exception(
                    f"Error loading state from {self.__s3}: {e} {traceback.print_exc}",
                    file=sys.stderr,
                )
        else:
            try:
                data = json.dumps(state)
                self.__s3.Bucket(self.__BUCKET_NAME).put_object(
                    Key=self.__fname, Body=data
                )
            except Exception as e:
                raise Exception(
                    f"Error creating {self.__fname} {self.__s3}: {e} {traceback.print_exc}",
                    file=sys.stderr,
                )
        self.data = state

    def __savestate(self, savenow=False):
        # Don't save unless savenow = True
        # if autosave is True, always save

        savenow = savenow or self.__autosave
        if not savenow:
            return

        try:
            data = json.dumps(self.data)
            self.__s3.Bucket(self.__BUCKET_NAME).put_object(Key=self.__fname, Body=data)
        except:
            raise Exception(f"Error saving state to {self.__s3}")

    def fromkeys(self, *args):
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
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val
        self.__savestate()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, key):
        del (self.data[key])
        self.__savestate()
