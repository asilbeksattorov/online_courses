from django import forms
from .models import Course, Module, Text, Video, Image, File, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'duration', 'price', 'subject', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Customize widgets
        self.fields['overview'].widget = forms.Textarea(attrs={'rows': 4})


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'course']


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'body']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'url']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 100}),
            'rating': forms.RadioSelect,
        }



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

