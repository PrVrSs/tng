from urllib.request import urlopen
from flask import Flask, url_for
import unittest
from flask_testing import LiveServerTestCase, TestCase
from TsqlParser import Parser
from RestApiTsqlParser import create_app
import json
import pytest


class TestRestApiTsqlParser(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 5
        return app

    def test_server_is_up_and_running(self):
        response = urlopen(self.get_server_url())
        self.assertTrue(b'Server is working' in response.read())
        self.assertEqual(response.code, 200)

    def test_server_urls(self):
        get_urls = ['/tasks', '/tasks/1', '/tasks/1/id', '/tasks/1/json',
                    '/tasks/1/string', '/tasks/1/correct', '/tasks/1/request',
                    '/tasks/1/time', '/tasks/1/tokens']
        for rest_ip in get_urls:
            response = urlopen(self.get_server_url()+rest_ip)
            self.assertEqual(response.code, 200)


class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()

    def test_get_json(self):
        response = self.client.get("/tasks/1")
        req = 'SELECT c1,c2 FROM tab1'
        p = Parser(input_data=req, type=2)
        self.assertEqual(response.json['string'], p.to_string())

    def test_not_found(self):
        self.assert404(self.client.get("/taskss"))

    def test_create_task(self):
        response = self.client.post('/tasks', data=json.dumps({"request": "SELECT c1,c2 FROM tab2"}),
                                    content_type='application/json')
        self.assertEquals(response.status, "201 CREATED")

    def test_delete_task(self):
        response = self.client.delete("/tasks/1")
        self.assertEquals(response.status, "200 OK")

    def test_put_task(self):
        response = self.client.put('/tasks/1', data=json.dumps({"request": "SELECT c1,c2 FROM tab2"}),
                                   content_type='application/json')
        self.assertEquals(response.status, "200 OK")

if __name__ == '__main__':
    unittest.main()


# Переписал под pytest

'''@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    @pytest.fixture
    def app(self):
        app = create_app()
        return app

    def test_server_is_up_and_running(self, live_server):

        res = urlopen(url_for('server_is_working', _external=True))
        assert res.code == 200
        assert b'Server is working' in res.read()


@pytest.mark.usefixtures('client_class')
class TestSuite:

    @pytest.fixture
    def app(self):
        app = create_app()
        return app

    def test_get_json(self):
        response = self.client.get("/tasks/1")
        req = 'SELECT c1,c2 FROM tab1'
        p = Parser(input_data=req, type=2)
        assert response.json['string'] == p.to_string()

    def test_not_found(self):
        assert self.client.get("/taskss").status_code == 404

    def test_create_task(self):
        response = self.client.post('/tasks', data=json.dumps({"request": "SELECT c1,c2 FROM tab2"}),
                                    content_type='application/json')
        assert response.status == "201 CREATED"

    def test_delete_task(self):
        response = self.client.delete("/tasks/1")
        assert response.status == "200 OK"

    def test_put_task(self):
        response = self.client.put('/tasks/1', data=json.dumps({"request": "SELECT c1,c2 FROM tab2"}),
                                   content_type='application/json')
        assert response.status == "200 OK"
'''
