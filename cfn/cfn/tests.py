"""Tests for the cfn."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
import factory
from posts.models import Post
import mock

RETURNED_JSON = """{
  "avatar_url": "https://avatars.githubusercontent.com/u/11498059?v=3",
  "html_url": "https://github.com/iamrobinhood12345",
  "bio": "I move fast and break my computer.",
}"""

LONG_MESSAGE = ("Lorem ipsum dolor sit amet, consectetuer adipiscing elit. " +
                "Aenean commodo ligula eget dolor. Aenean massa. Cum " +
                "sociis natoque penatibus et magnis dis parturient montes, " +
                "nascetur ridiculus mus. Donec quam felis, ultricies nec, " +
                "pellentesque eu, pretium quis,.")


class UserFactory(factory.django.DjangoModelFactory):
        """User factory for testing."""

        class Meta:
            """Model meta."""

            model = User

        username = factory.Sequence(lambda n: "User{}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
        )


class HomeViewTests(TestCase):
    """Tests for the home view with registration."""

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def setUp(self, github_api_call):
        """Set up test tool instances."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(5)]

    # Marc Mon
    def test_home_route_is_status_ok(self):
        """Funcional test."""
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)

    # Marc Mon
    def test_home_route_uses_correct_template(self):
        """Test that the home view renders the home.html template."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "cfn/home.html")

    # Marc Mon
    def test_non_user_cannot_see_logged_in(self):
        """A non user should only see the Log in and registration."""
        response = self.client.get('/')
        self.assertContains(response, 'Log In / Register via Github!')

    # Marc Mon
    def test_user_can_see_logged_in_home_page(self):
        """A logged in user sees the logged in home page."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        response = self.client.get('/')
        self.assertContains(response, '<p>Logged in as:')

    # Marc Thur
    def test_user_feed_contains_post_by_user(self):
        """A user's post show up on their own feed."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        post = Post(author=test_user, title="TestPost", content="testcontent")
        post.save()
        response = self.client.get('/')
        self.assertContains(response, 'TestPost')

    # Marc Thur
    def test_user_feed_contains_posts_by_followed_users(self):
        """A post by a followed user is on the feed."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        test_user2 = self.users[1]
        self.client.post('/profile/' + test_user2.username + '/')
        post = Post(author=test_user2, title="TestPost", content="testcontent")
        post.save()
        response = self.client.get('/')
        self.assertContains(response, 'TestPost')

    # Marc Thur
    def test_user_feed_doesnt_contains_posts_by_unfollowed_users(self):
        """A post by an unfollowed user is not on the feed."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        test_user2 = self.users[1]
        post = Post(author=test_user2, title="TestPost", content="testcontent")
        post.save()
        response = self.client.get('/')
        self.assertNotContains(response, 'TestPost')

    # Marc Thur
    def test_user_feed_with_greater_than_255_chars_is_shortened(self):
        """A post of more than 255 chars is shortened with a continue link."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        test_user2 = self.users[1]
        self.client.post('/profile/' + test_user2.username + '/')
        post = Post(author=test_user2, title="TestPost", content=LONG_MESSAGE)
        post.save()
        response = self.client.get('/')
        self.assertContains(response, '> continue</a>')

    # Marc Thur
    def test_user_feed_with_shorter_than_255_chars_is_not_shortened(self):
        """A post of less than 255 chars is not shortened."""
        test_user = self.users[0]
        self.client.force_login(test_user)
        test_user2 = self.users[1]
        self.client.post('/profile/' + test_user2.username + '/')
        post = Post(
            author=test_user2, title="TestPost", content='Short Message')
        post.save()
        response = self.client.get('/')
        self.assertNotContains(response, '> continue</a>')

    # Benny
    def test_about_page_returns_200(self):
        """Test that founder page url is correct."""
        response = self.client.get('/about/')
        self.assertTrue(response.status_code == 200)
