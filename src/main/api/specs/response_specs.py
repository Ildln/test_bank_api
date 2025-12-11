import requests

from http import HTTPStatus

class ResponseSpecs:

    @staticmethod
    def status_ok():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def status_created():
        def conform(response: requests.Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return conform

    @staticmethod
    def status_bad():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def status_unprocessable():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT, response.text
        return confirm

    @staticmethod
    def status_forbidden():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
        return confirm

    @staticmethod
    def status_conflict():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm

    @staticmethod
    def status_not_found():
        def confirm(response: requests.Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm