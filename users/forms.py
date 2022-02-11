from dataclasses import fields
from django.forms import ModelForm, models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2' ]
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs) -> None:
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})


class ProfileForm(models.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'short_intro', 'bio', 'email', 'location', 'username', 
        'profile_image', 'social_github', 'social_linkedin', 
        'social_stackoverflow', 'social_twitter', 'social_website' ]

    def __init__(self, *args, **kwargs) -> None:
        super(ModelForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})

class SkillForm(models.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description' ]

    def __init__(self, *args, **kwargs) -> None:
        super(ModelForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})


class MessageForm(models.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body' ]

    def __init__(self, *args, **kwargs) -> None:
        super(ModelForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})
        