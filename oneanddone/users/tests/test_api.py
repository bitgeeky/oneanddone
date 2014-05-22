# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from mock import Mock, patch
from nose.tools import eq_

from django.contrib.auth.models import User

from oneanddone.base.tests import TestCase
from oneanddone.users import views
from oneanddone.users.tests import UserFactory, UserProfileFactory

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import json

class ApiTests(APITestCase):
    def setUp(self):
        self.client_user = UserFactory.create()
        self.token = Token.objects.create(user=self.client_user)
        self.uri = '/api/v1/user/'

    def test_unauthenticated_user(self):
        response = self.client.get(reverse('api-user'))
        self.assertEqual(response.status_code, 401, "REST token-auth failed %s"%response.status_code)
        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'
        get_response = self.client.get(user_uri)
        self.assertEqual(get_response.status_code, 401, "REST get user details failed %s"%get_response.status_code)
        delete_response = self.client.delete(user_uri)
        self.assertEqual(delete_response.status_code, 401, "REST get user details failed %s"%delete_response.status_code)
    
    def test_get_user_list(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get(reverse('api-user'), {}, **header)
        self.assertEqual(response.status_code, 200, "REST token-auth failed")

    def test_get_user_details(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'
        response = self.client.get(user_uri)
        self.assertEqual(response.status_code, 200, "REST get user details failed")

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'
        delete_response = self.client.delete(user_uri)
        self.assertEqual(delete_response.status_code, 204, "REST get user details failed %s"%delete_response.status_code)
        get_response = self.client.get(user_uri)
        self.assertEqual(get_response.status_code, 404, "REST get user details failed %s"%get_response.status_code)
