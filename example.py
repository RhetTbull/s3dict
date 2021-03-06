"""
    Example script to demonstrate use of S3Dict
    To use this: you'll need to rename example.ini-sample to example.ini
    and add your Amazon AWS user key and secret key along with bucket name
    The load_config function will read example.ini to load your AWS credentials

    Alternatively, you can pass the AWS credentials directly to the S3Dict constructor

"""

import configparser
import traceback

from loguru import logger

from s3dictionary import S3Dict


def load_config(configfile):
    """ Read config file in ini format to load AWS credentials and bucket name """

    config = configparser.ConfigParser()
    config.read(configfile)

    if "aws" not in config:
        quit(f"Error parsing {configfile}: missing [aws] section")

    c = {}
    try:
        c["AWS_ACCESS_KEY_ID"] = config["aws"]["ACCESS_KEY_ID"]
        c["AWS_ACCESS_SECRET_KEY"] = config["aws"]["ACCESS_SECRET_KEY"]
        c["AWS_BUCKET_NAME"] = config["aws"]["BUCKET_NAME"]
    except Exception as e:
        traceback.print_exc()
        quit(f"Error parsing {configfile}: {e}")

    return c


if __name__ == "__main__":

    """ load credentials """
    config = load_config("example.ini")

    """ create an instance of S3Dict """
    state = S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test.json",
    )

    """ assignment like any python dictionary """
    state["foo"] = "bar"
    print(f"foo: {state['foo']}")

    state["foobar"] = 42
    print(f"foobar: {state['foobar']}")

    """  iteration """
    for k in state:
        print(f"k = {k}, {state[k]}")

    for k in state.keys():
        print(f"k = {k}, {state[k]}")

    for k, v in state.items():
        print(k, v)

    """ remove a key """
    del (state["foobar"])

    print(len(state))

    """ clear all items """
    state.clear()

    """ set a value and save """
    state["foo"] = "bar"
    state.save()

    """ create a new instance fromkeys 
        inherits settings from state """
    state2 = state.fromkeys([1, 2, 3])

    """ turn on autosave -- be sure you know what this will do!
        autosave causes every update to the dict to be saved to S3 
        this can be expensive in terms of run time and cost (Amazon charges per PUT) """
    state2.autosave = True

    """ pop and popitem """
    print(state2.pop(1))
    print(state2.popitem())

    """ setdefault """
    print(state2.setdefault("42"))

    """ update """
    state2.update({"a": "1", "b": 2, "c": 3})
    print(state2.values())

    """ create an instance of S3Dict """
    """ initialize with dict() """
    state3 = S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test3.json",
        data=dict(foo=42, bar=100),
    )

    print(state3)
    state3.save()

    """ manually change test3.json on S3 bucket then check to see it got re-loaded """
    input("Press enter to continue")
    state3.load()
    print(state3)

    """ create an instance of S3Dict """
    """ initialize with default if file not found """
    state4 = S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test4.json",
        default={"a": 1, "b": 2, "c": 3},
    )

    print(state4)
    state4.save()
    state4.load()
    print(state4)

    """ create an instance of S3Dict """
    """ initialize with default if file not found """
    """ set autosave=True to force immediate write """
    """ store the file in a folder in the bucket """
    state5 = S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test/test5.json",
        autosave=True,
        default={"x": 1, "y": 2, "z": 3},
    )

    state5.load()
    print(state5)

    """ access properties of the class """
    print(state5.file_name)
    print(state5.access_key_id)
    print(state5.access_secret_key)
    print(state5.bucket_name)

    """ delete the dictionary """
    """ policy for user and bucket must be set so user has S3:DeleteObject permissions or this raises an exception """
    state5.delete()
    del state5
    try:
        print(state5["x"])
    except Exception as e:
        print(f"Error accessing state5: {e}")
