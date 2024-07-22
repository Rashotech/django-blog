from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.messages import get_messages
from blog_posts.models import BlogPost

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.blog_post = BlogPost.objects.create(
            title="A blog post",
            content="Content of the blog post",
            author=self.user
        )
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.profile_url = reverse('users:profile')
        self.profile_update_url = reverse('users:profile_update')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_register_view_post(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_logout_view_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_profile_view_get_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_profile_view_get_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')

    def test_profile_update_post_success(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.profile_update_url, {
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your profile has been updated successfully!')