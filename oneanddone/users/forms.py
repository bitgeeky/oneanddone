from django import forms

from oneanddone.users.models import UserProfile


class UserProfileForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(required = True,)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'name', 'privacy_policy_accepted')

    privacy_policy_accepted.help_text = ("I'm okay with you handling this info as you explain in <a href='https://www.mozilla.org/en-US/privacy/websites/' target='_blank'>Mozilla's Privacy Policy</a>.")
