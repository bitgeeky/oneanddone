# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls.defaults import patterns, url

from oneanddone.users import views


urlpatterns = patterns('',
    url(r'^login/$', views.LoginView.as_view(), name='users.login'),
    url(r'^profile/new/$', views.CreateProfileView.as_view(), name='users.profile.create'),
    url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='users.profile.update'),

    # API URL's for interacting with User objects
    url(r'^api/v1/users/$', views.UserListAPI.as_view(), name='api-users'),
    url(r'^api/v1/users/(?P<email>([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+))/$', views.UserDetailAPI.as_view(), name='api-users-detail'),
)
