import logging
import os
import requests

from .exceptions import WordsapyException
from .dict_obj import DictObj

logger = logging.getLogger(__name__)

class WordsapyClient():

    def __init__(self, api_key=None):
        if api_key is not None:
            self.api_key = api_key
        self._base_url = 'https://wordsapiv1.p.rapidapi.com/words/'
        self._headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com'
        }

    @property
    def api_key(self):
        return os.environ.get('WORDS_API_KEY')

    @api_key.setter
    def api_key(self, api_key):
        os.environ['WORDS_API_KEY'] = str(api_key)

    def _get(self, action, word='', results_key='', params=''):
        '''
        '''
        if self.api_key is None or self.api_key == '':
            raise WordsapyException('API key not found.')

        url = '{}{}{}'.format(self._base_url, word, '/' + action if action else '')
        response = requests.request("GET", url, params=params, headers=self._headers)
        json = response.json()

        if ('success' in json and json['success'] == False) or 'message' in json:
            raise WordsapyException(json['message'] if 'message' in json else 'Unknown error')

        if results_key:
            if isinstance(json[results_key], list):
                return [DictObj(item) if isinstance(item, dict) else item for item in json[results_key]]
            else:
                return DictObj(json[results_key])

        return DictObj(json)

