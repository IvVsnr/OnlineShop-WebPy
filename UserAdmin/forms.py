from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class MySignUpForm(UserCreationForm):

    class Meta:

        model = MyUser

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_image',
            'some_file'
            # password field is required to be specified explicitly as it is provided by UserCreationForm
        )