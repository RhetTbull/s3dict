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

import S3Dict


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
    state = S3Dict.S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test.json",
    )

    """ assignment like any python dictionary """
    state["foo"] = "bar"
    print(f"foo: {state['foo']}")

    state["foobar"] = 42

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
        this can be expensive in terms of run time and cost (Amazon charges for per PUT) """
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
    state3 = S3Dict.S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test.json",
        data=dict(foo=42, bar=100),
    )

    print(state3)
    state3.save()

    """ manually change test.json on S3 bucket then check to see it got re-loaded """
    input("Press enter to continue")
    state3.load()
    print(state3)

    """ access properties of the class """
    print(state3.file_name)
    print(state3.access_key_id)
    print(state3.access_secret_key)
    print(state3.bucket_name)
