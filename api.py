"""
Class for accessing to Tilda API.
Tilda API documentation: https://help-ru.tilda.cc/api
"""
import json
import typing as t
import configparser

from urllib.request import urlopen
from urllib.parse import urlencode

from exceptions import TildaException


class TildaApi:

    TILDA_API_DOMEN = 'https://api.tildacdn.info/v1/'
    TIMEOUT = 5
    GET_PROJECTS_LIST = 'getprojectslist'
    GET_PROJECT_INFO = 'getprojectinfo'
    GET_PAGES_LIST = 'getpageslist'
    GET_PAGE = 'getpage'
    GET_PAGE_FULL = 'getpagefull'
    GET_PAGE_EXPORT = 'getpageexport'
    GET_PAGE_FULL_EXPORT = 'getpagefullexport'

    def __init__(self):
        """
        Read config and define values for tilda public key and tilda secret key
        """
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.TILDA_PUBLICKEY = config['tilda']['publickey']
        self.TILDA_SECRETKEY = config['tilda']['secretkey']
        self.TILDA_API_NAMES = [
                                    self.GET_PROJECTS_LIST,
                                    self.GET_PROJECT_INFO,
                                    self.GET_PAGES_LIST,
                                    self.GET_PAGE,
                                    self.GET_PAGE_FULL,
                                    self.GET_PAGE_EXPORT,
                                    self.GET_PAGE_FULL_EXPORT
                            ]

    def _api_call(self, api_name: str, api_params: t.Dict = None):
        """
        Call any API-function of tilda.
        :param api_name: string - name of API function
        :param api_params: Dict - GET-parameters. Example: {'projectid': 11111}
        :return: Dict or List - result of request to Tilda API
        """
        # check api name
        if api_name not in self.TILDA_API_NAMES:
            raise ValueError('Wrong API function name')

        # make api url
        param_str = '' if not api_params else '&' + urlencode(api_params)
        url = '{domen}{api_name}/?publickey={public_key}&secretkey={secret_key}{params}'.format(
            domen=self.TILDA_API_DOMEN,
            api_name=api_name,
            public_key=self.TILDA_PUBLICKEY,
            secret_key=self.TILDA_SECRETKEY,
            params=param_str
        )

        with urlopen(url=url, timeout=self.TIMEOUT) as resp:
            result = json.loads(resp.read())

        # handling data
        status = result.get('status')
        if status == 'FOUND':
            return result['result']
        elif status == 'ERROR':
            raise TildaException(result['message'])
        else:
            raise TildaException('Unknown error')

    def get_projects_list(self) -> t.List:
        """
        Return list of tilda account.

        :return: List
        Example:
           [
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
        """
        return self._api_call(self.GET_PROJECTS_LIST)

    def get_project_info(self, project_id: int) -> t.Dict:
        """
        Return info of tilda project

        :param project_id: int, id of tilda project
        :return: Dict
        Example:
            {
                "id": "0",
                "title": "Project title",
                "descr": "",
                "customdomain": "project.ru",
                "export_csspath": "",
                "export_jspath": "",
                "export_imgpath": "",
                "indexpageid": "0",
                "customcsstext": "y",
                "favicon": "",
                "page404id": "0",
                "images": [
                  {
                    "from": "",
                    "to": ""
                  }
                  ...
                ]
              }
        """
        return self._api_call(api_name=self.GET_PROJECT_INFO, api_params={'projectid': project_id})

    def get_pages_list(self, project_id: int) -> t.List:
        """
        Return pages list of tilda project
        :param project_id: int
        :return: List
        Example:
            [
                {
                  "id": "1001",
                  "projectid": "0",
                  "title": "Page title first",
                  "descr": "",
                  "img": "",
                  "featureimg": "",
                  "alias": "",
                  "date": "2014-05-16 14:45:53",
                  "sort": "80",
                  "published": "1419702868",
                  "filename": "page1001.html"
                },
                {
                  "id": "1002",
                  "projectid": "0",
                  "title": "Page title second",
                  "descr": "",
                  "img": "",
                  "featureimg": "",
                  "alias": "",
                  "date": "2014-05-17 10:50:00",
                  "sort": "90",
                  "published": "1419702277",
                  "filename": "page1002.html"
                },
                ...
              ]
        """
        return self._api_call(api_name='getpageslist', api_params={'projectid': project_id})

    def get_page(self, page_id: int) -> t.Dict:
        """
        Return tilda page info + body-html code of the page
        :param page_id: int
        :return: Dict
        Example:
            {
                "id": "1001",
                "projectid": "0",
                "title": "Page title",
                "descr": "",
                "img": "",
                "featureimg": "",
                "alias": "",
                "date": "2014-05-16 14:45:53",
                "sort": "80",
                "published": "1419702868",
                "html": "some html page code",
                "filename": "page1001.html",
                "js": [
                  ...
                ],
                "css": [
                  ...
                ]
            }
        """
        return self._api_call(api_name=self.GET_PAGE, api_params={'pageid': page_id})

    def get_page_full(self, page_id: int) -> t.Dict:
        """
        Return full tilda page info + full html-code of the page
        :param page_id: int
        :return: Dict
        Example:
            {
                "id": "1001",
                "projectid": "0",
                "title": "Page title",
                "descr": "",
                "img": "",
                "featureimg": "",
                "alias": "",
                "date": "2014-05-16 14:45:53",
                "sort": "80",
                "published": "1419702868",
                "html": "some html page code",
                "filename": "page1001.html"
            }
        """
        return self._api_call(api_name=self.GET_PAGE_FULL, api_params={'pageid': page_id})

    def get_page_export(self, page_id: int) -> t.Dict:
        """
        Return tilda page info for export + body-html code of the page
        :param page_id: int
        :return: Dict
        Example:
            {
                "id": "1001",
                "projectid": "0",
                "title": "Page title",
                "descr": "",
                "img": "",
                "featureimg": "",
                "alias": "",
                "date": "2014-05-16 14:45:53",
                "sort": "80",
                "published": "1419702868",
                "images": [
                  {
                    "from": "",
                    "to": ""
                  },
                  {
                    "from": "",
                    "to": ""
                  },
                  {
                    "from": "",
                    "to": ""
                  }
                ],
                "html": "body page html-code with local links to files",
                "filename": "page1001.html"
            }
        """
        return self._api_call(api_name=self.GET_PAGE_EXPORT, api_params={'pageid': page_id})

    def get_page_full_export(self, page_id: int) -> t.Dict:
        """
        Return full tilda page info + full page html-code
        :param page_id: int
        :return: Dict
        Example:
            {
                "id": "1001",
                "projectid": "0",
                "title": "Page title",
                "descr": "",
                "img": "",
                "featureimg": "",
                "alias": "",
                "date": "2014-05-16 14:45:53",
                "sort": "80",
                "published": "1419702868",
                "images": [
                  {
                    "from": "",
                    "to": ""
                  },
                  {
                    "from": "",
                    "to": ""
                  },
                  {
                    "from": "",
                    "to": ""
                  }
                ],
                "html": "full page html-code with local links to files",
                "filename": "page1001.html"
            }
        """
        return self._api_call(api_name=self.GET_PAGE_FULL_EXPORT, api_params={'pageid': page_id})

