# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from nose.tools import eq_

from oneanddone.users.tests import UserFactory

from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

import random


class APITests(APITestCase):
    """
    Test Cases For User REST API
    """
    def setUp(self):
        self.client_user = UserFactory.create()

        #Add delete user permission for client
        delete_permission = Permission.objects.get(codename='delete_user')
        self.client_user.user_permissions.add(delete_permission)

        self.token = Token.objects.create(user=self.client_user)
        self.uri = '/api/v1/user/'

    def test_unauthenticated_client(self):
        """
        Test user list, user details, user deletion for unauthenticated user
        """
        response = self.client.get(reverse('api-user'))
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % response.status_code)

        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'

        get_response = self.client.get(user_uri)
        eq_(get_response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % get_response.status_code)

        delete_response = self.client.delete(user_uri)
        eq_(delete_response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % delete_response.status_code)

    def test_client_with_false_token(self):
        """
        Test user list, user details, user deletion for user with false token
        """
        invalid_key = 'd81e33c57b2d9471f4d6849bab3cb233b3b30468'
        false_token = ''.join(random.sample(invalid_key, len(invalid_key)))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + false_token)

        response = self.client.get(reverse('api-user'))
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % response.status_code)

        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'

        get_response = self.client.get(user_uri)
        eq_(get_response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % get_response.status_code)

        delete_response = self.client.delete(user_uri)
        eq_(delete_response.status_code, status.HTTP_401_UNAUTHORIZED,
            "Failed with status code %s" % delete_response.status_code)

    def test_forbidden_client(self):
        """
        Test user deletion by an authenticated but forbidden client
        """
        forbidden_user = UserFactory.create()
        forbidden_token = Token.objects.create(user=forbidden_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + forbidden_token.key)

        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'

        #Make a DELETE request
        delete_response = self.client.delete(user_uri)
        eq_(delete_response.status_code, status.HTTP_403_FORBIDDEN,
            "Failed with status code %s" % delete_response.status_code)

    def test_get_user_list(self):
        """
        Test GET user list for authenticated user
        """
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get(reverse('api-user'), {}, **header)
        eq_(response.status_code, status.HTTP_200_OK,
            "Failed with status code %s" % response.status_code)

    def test_get_user_details(self):
        """
        Test GET details of a user with particular email for authenticated user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'
        response = self.client.get(user_uri)
        eq_(response.status_code, status.HTTP_200_OK,
            "Failed with status code %s" % response.status_code)

    def test_delete_user(self):
        """
        Test DELETE user with particular email for authenticated user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        test_user = UserFactory.create()
        user_uri = self.uri + test_user.email + '/'

        #Make a DELETE request
        delete_response = self.client.delete(user_uri)
        eq_(delete_response.status_code, status.HTTP_204_NO_CONTENT,
            "Failed with status code %s" % delete_response.status_code)

        #Verify that the user has been deleted
        get_response = self.client.get(user_uri)
        eq_(get_response.status_code, status.HTTP_404_NOT_FOUND,
            "Failed with status code %s" % get_response.status_code)
