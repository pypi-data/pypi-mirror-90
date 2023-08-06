import json
import os
import pickle
import shutil
from pathlib import Path
from typing import Union

import s3fs


class Serializer:
    """
    Seriealizer that can serialize/deserialize to/from local filesystem or S3
    """

    def __init__(self, s3_config: Union[dict, None]):
        """
        Create a seriealizer object.

        Depending on `s3_config`, the object will work with the local filesystem or S3


        :param s3_config:
            If `None`, use the local filesystem.
            Otherwise, use the provided credentials to connect to S3. The config dictionary
            has to contain the following keys: `"defaultBucket", "accessKey", "accessSecret"`
            If other keys exist, they are ignored
        """
        if s3_config is not None:
            if isinstance(s3_config, s3fs.S3FileSystem):
                s3 = s3_config
            else:
                key = s3_config['accessKey']
                secret = s3_config['accessSecret']
                s3 = s3fs.S3FileSystem(key=key, secret=secret)
        else:
            s3 = None
        self.s3 = s3

    def path_exists(self, path):
        if self.s3 is None:
            return os.path.exists(path)
        else:
            return self.s3.exists(path)

    def ls(self, path):
        if self.s3 is None:
            if not path:
                path = './'
            return os.listdir(path)
        else:
            ls = self.s3.ls(path)
            # Emulate the behaviour of os.listdir
            ls = [l.split('/', maxsplit=1)[-1] for l in ls]
            return ls

    def touch(self, path):
        if self.s3 is None:
            Path(path).touch()
        else:
            self.s3.touch(path)

    def makedirs(self, dirs, exist_ok=True):
        if self.s3 is None:
            return os.makedirs(dirs, exist_ok=exist_ok)
        else:
            return self.s3.mkdir(dirs, exist_ok=exist_ok)

    def rmtree(self, tree):
        if self.s3 is None:
            return shutil.rmtree(tree)
        else:
            return self.s3.rm(tree, recursive=True)

    def rm(self, path):
        if self.s3 is None:
            return os.remove(path)
        else:
            return self.s3.rm(path)

    def open(self, what, mode='r'):
        if self.s3 is None:
            return open(what, mode)
        else:
            return self.s3.open(what, mode)

    def json_dump(self, what, where):
        return json.dump(what, self.open(where, 'w'))

    def json_load(self, where):
        return json.load(self.open(where, 'r'))

    def pickle_dump(self, what, where):
        return pickle.dump(what, self.open(where, 'wb'))

    def pickle_load(self, where):
        return pickle.load(self.open(where, 'rb'))


if __name__ == '__main__':
    this_dir = os.path.split(__file__)[0]
    config = json.load(open(os.path.join(this_dir, 'secret/config.json')))
    sr = Serializer(config['s3'])
