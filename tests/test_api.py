import json
import pytest

from api import TildaApi
from exceptions import TildaException

@pytest.fixture
def project_list_request_success():
    return json.dumps({
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
              ]
            })

@pytest.fixture
def project_info_request_success():
    return json.dumps({
              "status": "FOUND",
              "result": {
                "id": "1",
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
                ]
              }
            })

@pytest.fixture
def pages_list_success():
    return json.dumps({
              "status": "FOUND",
              "result": [
                {
                  "id": "1001",
                  "projectid": "1",
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
                  "projectid": "1",
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
              ]
            })

@pytest.fixture
def api_calling_fail():
    return json.dumps(
        {
            "status": "ERROR",
            "message": "error"
        }
    )


def test_get_projects_list_success(mocker, project_list_request_success):
    # Creates a fake requests response object
    mocker.patch('api.urlopen').return_value.__enter__.return_value.read = mocker.Mock(
        return_value=project_list_request_success
    )
    # calls api function
    tilda_api = TildaApi()
    projects_list = tilda_api.get_projects_list()
    assert projects_list == [
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
                              ]


def test_get_project_list_fail(mocker, api_calling_fail):
    mocker.patch('api.urlopen').return_value.__enter__.return_value.read = mocker.Mock(
        return_value=api_calling_fail
    )
    # calls api function
    tilda_api = TildaApi()
    with pytest.raises(TildaException):
        tilda_api.get_projects_list()


def test_get_project_info(mocker, project_info_request_success):
    # Creates a fake requests response object
    mocker.patch('api.urlopen').return_value.__enter__.return_value.read = mocker.Mock(
        return_value=project_info_request_success
    )
    # calls api function
    tilda_api = TildaApi()
    project_info = tilda_api.get_project_info(project_id=1)
    assert project_info == {
                                "id": "1",
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
                                ]
                              }


def test_get_pages_list(mocker, pages_list_success):
    # Creates a fake requests response object
    mocker.patch('api.urlopen').return_value.__enter__.return_value.read = mocker.Mock(
        return_value=pages_list_success
    )
    # calls api function
    tilda_api = TildaApi()
    pages_list = tilda_api.get_pages_list(project_id=1)
    assert pages_list == [
                            {
                              "id": "1001",
                              "projectid": "1",
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
                              "projectid": "1",
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
                          ]
