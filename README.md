S3Dictionary [Homepage](https://github.com/RhetTbull/s3dict)
========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


What is S3Dictionary?
-----------------

Implements a persistent python dictionary class (inherited from collections.UserDict) that serializes its state as a json file in an Amazon AWS S3 bucket.  This works well for simple persistence if all you need is to save some key/value pairs.   

S3Dictionary should be a drop-in replacement for a standard python dict.

If you think you need this module, you probably need something else. S3Dictionary is simple and easy to use though if all you need is a persitent dictionary. With lazy saving (autosave=False), it's also reasonably fast.


Installation instructions
-------------------------

	python setup.py install


Example uses of the module
--------------------------

```python
from s3dictionary import S3Dict

if __name__ == "__main__":

    """ create an instance of S3Dict """
    state = S3Dict(
        bucket_name=AWS_BUCKET_NAME,
        access_key_id=AWS_ACCESS_KEY_ID,
        access_secret_key=AWS_ACCESS_SECRET_KEY,
        file_name="test.json",
    )

    """ assignment like any python dictionary """
    state["foo"] = "bar"

    """ save back to S3 bucket """
    state.save()

```

See example.py for additional usage examples.

Module Interface
----------------
```python
S3Dict(bucket_name=AWS_BUCKET_NAME,
       access_key_id=AWS_ACCESS_KEY_ID,
       access_secret_key=AWS_ACCESS_SECRET_KEY,
       file_name="filename.json",
       [autosave=False],
       [data=None]),
       [default=None],
```

Construct a new S3Dict object.  If `file_name` exists, restores state from file.  If file_name does not exist, initialize a new dictionary.  In the case the file does not already exist, it will not be created in the S3 bucket until you call `save()` unless `autosave=True`.    

If a dictionary is passed in `data` the dictionary will be initialized with what was passed in `data`.  This will overwrite any data that was loaded from file. If a dictionary is passed in `default` and the file does not exist, the dictionary will be initialized with what was passed in `default`.  Unlike the `data` argument, `default` will not overwrite any existing data.
    
*Required arguments*
   - `bucket_name`: name of S3 bucket
   - `acess_key_id`: AWS access key id
   - `access_secret_key`: AWS secret key
   - `file_name`: file name of the serialized dictionary to be stored in S3 bucket
    
*Optional arguments*
   - `autosave`: must be `bool`, default is False -- setting this to True causes every update to the underlying dictionary to be immediately serialized to S3
   - `data`: python dictionary used to initialize data
   - `default`: python dictionary used to initialize data if the file does not already exist in the S3 bucket

```python
S3Dict.save()
```

Force state to be serialized to S3 bucket

```python
S3Dict.load()
```

Force state to be immediately loaded from S3 bucket.  In normal circumstances, you won't need to do this.  It might be useful if an external processes updates the state information and you want to force a reload. 

```python
S3Dict.autosave = True|False
S3Dict.autosave
```

Turn autosave on (True) or off (False). Also a property to read autosave value.  If `autosave` is `True`, every update to the dictionary will immediately be serialized back to the S3 bucket.  Please be sure you understand what this means before turning `autosave` on!

```python
S3Dict.file_name
S3Dict.access_key_id
S3Dict.access_secret_key
S3Dict.bucket_name
```

Read only properties

```python
S3Dict.delete()
```

Clear the stored data and deletes the json file from S3.  The user must have S3 DeleteObject permissions.  This does not delete the actual S3Dict object instance.  To do that, follow call S3Dict.delete() with del. 

```python
from s3dictionary import S3Dict

mys3dict = S3Dict(...)
...
mys3dict.delete() # deletes the data and the file
del mys3dict # deletes the object
```

Usage Notes
-----------

To use S3Dict, you must first create an Amazon S3 bucket and a user with permissions to access the bucket.

I highly recommend [Keith Weaver's](https://github.com/keithweaver) excellent [tutorial](https://github.com/keithweaver/python-aws-s3) on using AWS S3 with python and setting up buckets and users.

Be careful with ```autosave``` as it could cost you money--if your underlying dict changes a lot, autosave will cause S3Dict to pound your S3 account with frequent PUT commands which could result in charges.  It is also costly in terms of execution speed as every change to the underlying dictionary forces an interaction with the S3 server.

