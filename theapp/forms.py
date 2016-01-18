from django.forms import ModelForm
from theapp.models import User, City


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'location']

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['city'].queryset = City.objects.all()
        # assuming your Category model has user foreignkey/onetone field.
