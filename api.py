"""
Class for accessing to Tilda API.
Tilda API documentation: https://help-ru.tilda.cc/api
"""
import json
import configparser

from urllib.request import urlopen

from exceptions import TildaException


class TildaApi:

    TILDA_API_DOMEN = 'https://api.tildacdn.info/v1/'
    TIMEOUT = 5

    def __init__(self):
        config = configparser.ConfigParser()
        self.TILDA_PUBLICKEY = config['Tilda']['publickey']
        self.TILDA_SECRETKEY = config['Tilda']['secretkey']
        self.error = ''

    def _api_call(self, api_name, api_params=None):
        """
        Call any API-function of tilda.
        :param api_name: string - name of API function
        :param api_params: Dict - GET-parameters. Example: {'projectid': 11111}
        :return:
        """
        param_str = '&'.join('{}={}'.format(k, v) for k, v in api_params.items())
        url = '{domen}{api_name}/?publickey={public_key}&secretkey={secret_key}&{params}'.format(
            domen=self.TILDA_API_DOMEN,
            api_name=api_name,
            public_key=self.TILDA_PUBLICKEY,
            secret_key=self.TILDA_SECRETKEY,
            params=param_str
        )

        resp = urlopen(
            url=url,
            timeout=self.TIMEOUT
        )

        # handling data
        result = json.loads(resp.read())
        status = result.get('STATUS')
        if status == 'FOUND':
            return result['result']
        elif status == 'ERROR':
            raise TildaException(result['message'])
        else:
            raise TildaException('Unknown error')

    def get_projects_list(self):
        """
        Get projects list of tilda.
        :return: Dict
        Example:
            {
              "status": "FOUND",
              "result": [
                {
                  "id": "0",
                  "title": "First Project",
                  "descr": "Some info"
                },
                {
                  "id": "1",
                  "title": "Second Project",
                  "descr": ""
                },
                ...
              ]
            }
        """
        return self._api_call('getprojectslist')

    def get_project_info(self, project_id):
        return self._api_call(api_name='getprojectinfo', api_params={'projectid': project_id})

    def get_pages_list(self, project_id):
        return self._api_call(api_name='getpageslist', api_params={'projectid': project_id})

    def get_page(self, page_id):
        return self._api_call(api_name='getpage', api_params={'pageid': page_id})

    def get_page_full(self, page_id):
        return self._api_call(api_name='getpagefull', api_params={'pageid': page_id})

    def get_page_export(self, page_id):
        return self._api_call(api_name='getpageexport', api_params={'pageid': page_id})

    def get_page_full_export(self, page_id):
        return self._api_call(api_name='getpagefullexport', api_params={'pageid': page_id})

