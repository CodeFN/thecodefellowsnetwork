"""Tests for the cfn."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
import factory
from cfn.views import HomeView


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

    def setUp(self):
        """Set up test tool instances."""
        self.client = Client()
        self.request = RequestFactory()

    def add_user(self):
        """Make a user and return his profile."""
        user = UserFactory.create()
        user.username = 'test_user'
        user.set_password('testpassword')
        user.save()
        return user

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
        self.assertContains(response, 'Log in or sign up with Github!')

    # Marc Mon
    def test_user_can_see_logged_in_home_page(self):
        """A logged in user sees the logged in home page."""
        test_user = self.add_user()
        self.client.force_login(test_user)
        response = self.client.get('/')
        self.assertContains(response, '<p>Logged in as:')
