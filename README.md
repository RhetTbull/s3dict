S3Dict [Homepage](https://github.com/RhetTbull/s3dict)
========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


What is S3Dict?
-----------------

Implements a python dictionary class (inherited from collections.UserDict) that saves its state as
a json file in Amazon AWS S3 buckets.  I built this as an experiment for saving state in a script
run inside a Docker container.  

Installation instructions
-------------------------

	python setup.py install


Example uses of the module
--------------------------

```python
import S3Dict

if __name__ == "__main__":

    """ create an instance of S3Dict """
    state = S3Dict.S3Dict(
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

Usage Notes
-----------

To use S3Dict, you must first create an Amazon S3 bucket and a user with permissions to access the bucket.
I highly recommend [Keith Weaver's](https://github.com/keithweaver) excellent [tutorial](https://github.com/keithweaver/python-aws-s3) on using AWS S3 with python and setting up buckets and users.

Be careful with ```autosave``` as it could cost you money--if your underlying dict changes a lot, autosave will
cause S3Dict to pound your S3 account with frequent PUT commands which will rack up charges.


