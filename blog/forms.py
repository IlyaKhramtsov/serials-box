from django import forms

from blog.models import Article


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название'}),
        }
