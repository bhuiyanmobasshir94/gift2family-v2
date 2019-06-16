from .models import AgentProfile
from django import forms

class AgentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True
        if 'name' in self.fields:
            self.fields['name'].required = True
        if 'phone_number' in self.fields:
            self.fields['phone_number'].required = True
        if 'nationality' in self.fields:
            self.fields['nationality'].required = True
        if 'country' in self.fields:
            self.fields['country'].required = True
        if 'passport_copy' in self.fields:
            self.fields['passport_copy'].required = True

    class Meta:
        model = AgentProfile
        exclude = ('user', 'date_created')
