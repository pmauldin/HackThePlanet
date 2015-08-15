"""
Base model subsequent models inherit from
"""


class Model(object):

    def __init__(self, **kwargs):
        # attach to self
        self.data = kwargs

    def save(self):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
