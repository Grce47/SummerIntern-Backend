from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import pythonCode

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


class EditStatusForm(forms.ModelForm):
    class Meta:
        model = pythonCode
        fields = ['Done','Feedback']
    
    def __init__(self, *args, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)
        self.fields['Feedback'].required = False