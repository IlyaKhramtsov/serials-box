from django import forms

from blog.models import Article


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "photo"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
