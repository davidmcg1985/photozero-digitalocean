from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Photo, Comment


# class LoginTestCase(TestCase):

#     def test_call_view_denies_anonymous(self):
#         response = self.client.get('http://localhost:8000/timeline/create/', follow=True)
#         self.assertRedirects(response, 'http://localhost:8000/timeline/')
#         response = self.client.post('http://localhost:8000/timeline/create/', follow=True)
#         self.assertRedirects(response, 'http://localhost:8000/timeline/')

#     def test_call_view_loads(self):
#         self.client.login(username='user', password='test')
#         response = self.client.get('http://localhost:8000/timeline/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'photo_list.html')

#     def test_call_view_fails_blank(self):
#         self.client.login(username='user', password='test')
#         response = self.client.post('http://127.0.0.1:8000/timeline/', {})
#         self.assertFormError(response, 'form', 'some_field', 'This field is required.')


class PhotoTestCase(TestCase):

    def setUp(self):
        Photo.objects.create(username="user", title="Test", 
            description="This is a test Upload")