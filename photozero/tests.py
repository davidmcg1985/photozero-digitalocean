from django.test import TestCase
from timeline.models import Photo, Comment


class TestCalls(TestCase):

    def test_call_view_denies_anonymous(self):
        response = self.client.get('http://127.0.0.1:8000/timeline/create/', follow=True)
        self.assertRedirects(response, 'http://127.0.0.1:8000/timeline/')
        response = self.client.post('http://127.0.0.1:8000/timeline/create/', follow=True)
        self.assertRedirects(response, 'http://127.0.0.1:8000/timeline/')

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')
        response = self.client.get('http://127.0.0.1:8000/timeline/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photo_list.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('http://127.0.0.1:8000/timeline/', {})
        self.assertFormError(response, 'form', 'some_field', 'This field is required.')