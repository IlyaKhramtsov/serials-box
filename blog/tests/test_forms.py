import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from blog.forms import AddPostForm


class TestForms(TestCase):

    def test_add_post_form_valid_data(self):
        image_file = open('static/serials/images/avatar.png', 'rb')
        photo = {
            'photo': SimpleUploadedFile(
                image_file.name,
                image_file.read()
            )
        }
        data = {
            'title': 'Test article',
            'slug': 'test-article',
            'content': 'test article content',
        }
        form = AddPostForm(data, photo)

        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = AddPostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
