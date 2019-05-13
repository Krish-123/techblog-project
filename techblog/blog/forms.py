from django import forms
from . models import PostModel,CommentModel

class PostForm(forms.ModelForm):

    class Meta():
        model = PostModel
        fields = ['author','title','post']

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'post':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = CommentModel
        fields = ['author','comment']

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'comment':forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }