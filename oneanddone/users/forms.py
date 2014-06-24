from django import forms

from oneanddone.users.models import UserProfile


class UserProfileForm(forms.ModelForm):
    privacy_policy_accepted = forms.BooleanField(required = True,)
    username = forms.RegexField(
        max_length=30, regex=r'^[a-zA-Z0-9]+$',
        help_text = "Required. 30 characters or fewer. Letters and digits only.",
        error_messages = {'invalid': "This value may contain only alphanumeric characters."})
    
    class Meta:
        model = UserProfile
        fields = ('username', 'name', 'privacy_policy_accepted')

    privacy_policy_accepted.help_text = ("I'm okay with you handling this info as you explain in <a href='https://www.mozilla.org/en-US/privacy/websites/' target='_blank'>Mozilla's Privacy Policy</a>.")
