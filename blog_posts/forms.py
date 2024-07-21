from django import forms 
from . import models 

class CreatePost(forms.ModelForm): 
    class Meta: 
        model = models.BlogPost
        fields = ['title','content','category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']