import configparser
import traceback

from loguru import logger

import S3Dict


def load_config(configfile):
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
    config = load_config("example.ini")
    state = S3Dict.S3Dict(
        bucket_name=config["AWS_BUCKET_NAME"],
        access_key_id=config["AWS_ACCESS_KEY_ID"],
        access_secret_key=config["AWS_ACCESS_SECRET_KEY"],
        file_name="test.json",
        autosave=False,
    )
    state["foo"] = "bar"
    print(f"foo: {state['foo']}")

    if "foobar" in state:
        print("Yep")
    else:
        print("Nope")

    state["foobar"] = 42
    for k in state:
        print(f"k = {k}, {state[k]}")

    for k in state.keys():
        print(f"k = {k}, {state[k]}")

    del (state["foobar"])

    for k, v in state.items():
        print(k, v)

    state["foo"] = "bar"
    state["answer"] = 42

    print(len(state))
    state.clear()
    
    state.autosave = True 
    state = state.fromkeys([1, 2, 3])

    print(state.pop(1))
    print(state.popitem())
    print(state.setdefault("42"))
    state.update({"a": "1", "b": 2, "c": 3})
    state["foobar"] = "BAR"
    print(state.values())
    print(f"keys = {state.keys()}")
    state.save()

    # test properties
    print(state.file_name)
    print(state.access_key_id)
    print(state.access_secret_key)
    print(state.bucket_name)