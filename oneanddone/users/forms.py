from django import forms

from oneanddone.users.models import UserProfile


class UserProfileForm(forms.ModelForm):
    privacy_agreement = forms.BooleanField(required = True,)

    class Meta:
        model = UserProfile
        fields = ('name', 'privacy_agreement')

    privacy_agreement.help_text = ("I'm okay with you handling this info as you explain in <a href='https://www.mozilla.org/en-US/privacy/websites/' target='_blank'>Mozilla's Privacy Policy</a>.")
