from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        #fields = '__all__'
        fields = ['title', 'featured_image', 'description', 'tags', 'source_link', 'demo_link' ]
        widgets = {
            'tags' : forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        #fields = '__all__'
        fields = ['value', 'body' ]
        labels = {
            'value': 'Place your vote up or down',
            'body': 'Add a text for you vote'
        } 
        

    def __init__(self, *args, **kwargs) -> None:
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})