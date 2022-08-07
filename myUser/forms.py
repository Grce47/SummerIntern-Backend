from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import pythonCode

class UserSignUpForm(UserCreationForm): #we use the USerCreationForm from Django (username and password fields are created in that only)
    first_name = forms.CharField()  #first name field
    last_name = forms.CharField()   #last name field
    email = forms.EmailField()      #email field

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


class EditStatusForm(forms.ModelForm):  #the code status form (Done check and feedback button)
    class Meta:
        model = pythonCode
        fields = ['Done','Feedback']    #fields are added in here
    
    def __init__(self, *args, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)
        self.fields['Feedback'].required = False