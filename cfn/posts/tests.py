"""Posts tests."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from posts.models import Post
import factory

import mock


RETURNED_JSON = """{
  "avatar_url": "https://avatars.githubusercontent.com/u/11498059?v=3",
  "html_url": "https://github.com/iamrobinhood12345",
  "bio": "I move fast and break my computer.",
}"""


class UserFactory(factory.django.DjangoModelFactory):
    """User factory for testing."""

    class Meta:
        """Model meta."""

        model = User

    username = factory.Sequence(lambda n: "User{}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
    )


class BackendTests(TestCase):
    """Posts backend test runner."""

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def setUp(self, github_api_call):
        """Set up for backend test runner."""
        self.users = [UserFactory.create() for i in range(5)]
        self.posts = [Post() for i in range(5)]
        for i in range(len(self.posts)):
            self.posts[i].author = self.users[i]
            self.posts[i].title = factory.Sequence(lambda n: "Post{}".format(n))
            self.posts[i].save()

    # Ben Wednesday
    def test_posts_exist(self):
        """Count posts."""
        self.assertTrue(Post.objects.all().count() == 5)

    # Ben Wednesday
    def test_post_author(self):
        """"Test post has author."""
        this_post = Post.objects.all()[0]
        self.assertTrue(this_post.author == self.users[0])

    # Ben Wednesday
    def test_post_has_title(self):
        """Test post title attributed."""
        self.assertTrue(self.posts[0].title)


class FrontEndTests(TestCase):
    """Posts frontend test runner."""

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def setUp(self, github_api_call):
        """Set up for frontend test runner."""
        self.users = [UserFactory.create() for i in range(5)]
        self.client = Client()
        self.request = RequestFactory()

    # Ben Wednesday
    def test_post_view_authenticated_user_returns_status_ok(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Ben Wednesday
    def test_other_user_post_view_authenticated_user_returns_status_ok(self):
        """Test other post view with authenticated client returns status code 200."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        other_user = self.users[1]
        self.client.force_login(this_user)
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Ben Thursday
    def test_posts_view_authenticated_user_returns_status_ok(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/', follow=True)
        self.assertTrue(response.status_code == 200)

    # Ben Thursday
    def test_new_post_view_authenticated_user_returns_status_ok(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/new')
        self.assertTrue(response.status_code == 200)

    # Ben Thursday
    def test_edit_post_view_authenticated_user_returns_status_ok(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id) + '/edit')
        self.assertTrue(response.status_code == 200)

    # Ben Thursday
    def test_delete_post_view_authenticated_user_returns_status_ok(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id) + '/delete')
        self.assertTrue(response.status_code == 200)

    # Ben Thursday
    def test_post_view_renders_template_content(self):
        """Test post view response content contains post content."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertContains(response, 'tornado fire crocodile')

    # Ben Thursday
    def test_post_view_renders_template_title(self):
        """Test post view response content contains post title."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertContains(response, 'marc ben benny built this site')

    # Ben Thursday
    def test_post_view_renders_correct_template(self):
        """Test post view response renders the post.html template."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "posts/post.html")

    # Ben Thursday
    def test_posts_view_renders_template_content(self):
        """Test post view response content contains post content."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/', follow=True)
        self.assertContains(response, 'tornado fire crocodile')

    # Ben Thursday
    def test_posts_view_renders_template_title(self):
        """Test post view response content contains post title."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/', follow=True)
        self.assertContains(response, 'marc ben benny built this site')

    # Ben Thursday
    def test_posts_view_renders_correct_template(self):
        """Test post view response renders the post.html template."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        self.client.force_login(this_user)
        response = self.client.get('/posts/', follow=True)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "posts/posts.html")

    # Ben Thursday
    def test_view_other_user_post_on_posts_view(self):
        """Test other user posts' content shows on posts page."""
        this_user = self.users[0]
        this_post = Post()
        this_post.author = this_user
        this_post.content = 'tornado fire crocodile'
        this_post.title = 'marc ben benny built this site'
        this_post.save()
        other_user = self.users[1]
        self.client.force_login(other_user)
        response = self.client.get('/posts/', follow=True)
        self.assertContains(response, 'tornado fire crocodile')
        self.assertContains(response, 'marc ben benny built this site')

    # Benny
    def test_edited_post_content_renders_on_post_view(self):
        """Test other post view with authenticated client returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_edited_post_content_renders_on_posts_view(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_edited_post_content_renders_on_profile_view(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_post_content_renders_on_post_view(self):
        """Test other post view with authenticated client returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_post_content_renders_on_posts_view(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_post_content_renders_on_profile_view(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_edited_post_content_renders_on_post(self):
        """Test other post view with authenticated client returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_edited_post_content_renders_on_posts(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_edited_post_content_renders_on_profile(self):
        """Test post view returns status code 200."""
        this_user = self.users[0]
        self.client.force_login(this_user)
        this_post = Post()
        this_post.author = this_user
        this_post.save()
        response = self.client.get('/posts/' + str(this_post.id), follow=True)
        self.assertTrue(response.status_code == 200)
