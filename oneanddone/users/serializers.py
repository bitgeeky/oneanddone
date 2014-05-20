# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from rest_framework import serializers
from django.contrib.auth.models import User

from oneanddone.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name','user')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required = False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'profile')
