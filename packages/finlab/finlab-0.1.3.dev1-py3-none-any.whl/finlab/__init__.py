import os

__version__ = '0.1.3.dev1'

class Token:
    def __init__(self, interaction=True):

        if interaction and 'finlab_id_token' not in os.environ:
            id_token = input('Please login to finlab and copy id token here: \n')
            os.environ['finlab_id_token'] = id_token
        pass

    def set(self, token):
        os.environ['finlab_id_token'] = token

    def get(self):
        if 'finlab_id_token' in os.environ:
            return os.environ['finlab_id_token']
        else:
            return None
