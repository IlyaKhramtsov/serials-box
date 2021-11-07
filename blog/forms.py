from django import forms

from blog.models import Article


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'photo', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
