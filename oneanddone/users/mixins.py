# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

from oneanddone.users.models import UserProfile


class BaseUserProfileRequiredMixin(object):
    """
    Require users to have a UserProfile before they can interact with
    the view.
    """
    def dispatch(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.filter(user=request.user)
        if user_profile.exists() and user_profile[0].privacy_agreement:
            return super(BaseUserProfileRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('users.profile.create')


class UserProfileRequiredMixin(LoginRequiredMixin, BaseUserProfileRequiredMixin):
    """
    Require a user to be both logged in and have a UserProfile before
    they can interact with the view.
    """
