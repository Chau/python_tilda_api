import pytest

from api import TildaApi

@pytest.fixture
def project_list_request_success():
    return {
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
            }

@pytest.fixture
def project_info_request_success():
    return {
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
            }


def test_get_project_list(mocker, project_list_request_success):
    # Creates a fake requests response object
    fake_resp = mocker.Mock()
    # Mock method to return the project list data
    fake_resp.read = mocker.Mock(return_value=project_list_request_success)
    mocker.patch('api.urlopen', return_value=fake_resp)

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


def test_get_project_info(mocker, project_info_request_success):
    fake_resp = mocker.Mock()
    fake_resp.read = mocker.Mock(return_value=project_info_request_success)
    mocker.patch('api.urlopen', return_value=fake_resp)

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
