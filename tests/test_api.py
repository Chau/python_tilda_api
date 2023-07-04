import pytest

from api import TildaApi

@pytest.fixture
def get_project_list_request_success():
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


def test_get_project_list(mocker, get_project_list_request_success):
    # Creates a fake requests response object
    fake_resp = mocker.Mock()
    # Mock the json method to return the project list data
    fake_resp.read = mocker.Mock(return_value=get_project_list_request_success)

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
