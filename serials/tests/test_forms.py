from django.test import SimpleTestCase
from serials.forms import CommentForm


class TestForms(SimpleTestCase):

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'text': 'test comment'
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
