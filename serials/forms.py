from django import forms

from serials.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Комментарий'}),
        }
