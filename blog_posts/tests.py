from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, BlogPost, Comment

class BlogPostViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='TestCategory')
        self.post = BlogPost.objects.create(title='Test Post', content='Test Content', author=self.user, category=self.category)

    def test_category_filter(self):
        url = reverse('posts:category_filter', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_author_filter(self):
        url = reverse('posts:author_filter', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_single_post(self):
        url = reverse('posts:single_post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_posts/single_post.html')

    def test_search(self):
        url = reverse('posts:search') + '?q=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_create_blog_post_get(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:create_blog_post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_posts/new_post.html')

    def test_create_blog_post_post_valid(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:create_blog_post')
        data = {
            'title': 'New Test Post',
            'content': 'Test Content',
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.count(), 2) 

    def test_create_blog_post_post_invalid(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:create_blog_post')
        data = {
            'title': '',
            'content': 'Test Content',
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_edit_blog_post_get(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:edit_blog_post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_posts/edit_post.html')

    def test_edit_blog_post_post_valid(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:edit_blog_post', args=[self.post.id])
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated Content',
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')

    def test_edit_blog_post_post_invalid(self):
        self.client.login(username='testuser', password='password')
        url = reverse('posts:edit_blog_post', args=[self.post.id])
        data = {
            'title': '',
            'content': 'Updated Content',
            'category': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.content, 'Updated Content')

    def test_create_comment_valid(self):
        url = reverse('posts:create_comment', args=[self.post.id])
        data = {
            'content': 'Test Comment',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.comments.count(), 1)

    def test_create_comment_invalid(self):
        url = reverse('posts:create_comment', args=[self.post.id])
        data = {
            'content': '', 
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.comments.count(), 0)

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Technology",
            description="All about technology"
        )

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.name, "Technology")
        self.assertEqual(self.category.description, "All about technology")
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)

    def test_category_str(self):
        self.assertEqual(str(self.category), self.category.name)


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Technology")
        self.blog_post = BlogPost.objects.create(
            title="A blog post",
            content="Content of the blog post",
            author=self.user,
            category=self.category
        )

    def test_blog_post_creation(self):
        self.assertIsInstance(self.blog_post, BlogPost)
        self.assertEqual(self.blog_post.title, "A blog post")
        self.assertEqual(self.blog_post.content, "Content of the blog post")
        self.assertEqual(self.blog_post.author, self.user)
        self.assertEqual(self.blog_post.category, self.category)
        self.assertIsNotNone(self.blog_post.created_at)
        self.assertIsNotNone(self.blog_post.updated_at)

    def test_blog_post_str(self):
        self.assertEqual(str(self.blog_post), self.blog_post.title)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Technology")
        self.blog_post = BlogPost.objects.create(
            title="A blog post",
            content="Content of the blog post",
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.blog_post,
            content="This is a comment"
        )

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.content, "This is a comment")
        self.assertEqual(self.comment.post, self.blog_post)
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), self.comment.content)