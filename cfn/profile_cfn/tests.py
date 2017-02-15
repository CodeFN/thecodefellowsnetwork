"""CFN Tests."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from profile_cfn.models import ProfileCfn
from profile_cfn.forms import EditProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from bs4 import BeautifulSoup as Soup
import factory


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
    """User/profile backend test runner."""

    def setUp(self):
        """Set up for backend test runner."""
        self.users = [UserFactory.create() for i in range(5)]

    def test_profile_is_made_when_user_is_saved(self):
        """Test profile created when user is registered."""
        self.assertTrue(ProfileCfn.objects.count() == 5)

    def test_profile_is_associated_with_users(self):
        """Test profile has correct user instance."""
        profile = ProfileCfn.objects.first()
        username = self.users[0].username
        self.assertTrue(profile.user.username == username)

    def test_profile_model_returns_string(self):
        """Test that user model returns string for Py2 compatibility."""
        assert type(str(UserFactory.create())) == str

    def test_profile_model_returns_string_part_2(self):
        """Test that user model returns string for Py2 compatibility."""
        assert type(str(ProfileCfn.objects.first())) == str

    def test_profile_model_returns_is_active(self):
        """Test that user model returns bool on is_active."""
        assert type((ProfileCfn.objects.first().is_active)) == bool

    def test_inactive_profile_model_user_is_inactive(self):
        """Test that user profile model is inactive by default."""
        assert type((ProfileCfn.objects.first().is_active)) == bool


class FrontendTests(TestCase):
    """User/profile frontend test runner."""

    def setUp(self):
        """Set up for frontend fest runner."""
        self.client = Client()
        self.request = RequestFactory()
        self.photo = SimpleUploadedFile('test.jpg', open('cfn/static/images/cf_logo.png', 'rb').read())

    def add_user(self, username='test_user'):
        """Make a user and return his profile."""
        user = UserFactory.create()
        user.username = username
        user.set_password('testpassword')
        user.save()
        return user

    def log_in_test_user(self, username='test_user'):
        """Log in the test user."""
        self.client.login(username=username, password='testpassword')

    def test_profile_view_authenticated_returns_status_ok(self):
        """Test profile view returns status code 200."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get('/profile', follow=True)
        self.assertTrue(response.status_code == 200)

    def test_profile_view_unauthenticated_returns_status_redirect(self):
        """Test profile view with unauthenticated client returns status code 302."""
        response = self.client.get("/profile/")
        self.assertTrue(response.status_code == 302)

    def test_other_profile_view_authenticated_returns_status_ok(self):
        """Test other profile view with authenticated client returns status code 200."""
        self.add_user()
        self.log_in_test_user()
        new_user = UserFactory.create()
        response = self.client.get(
            '/profile/' + new_user.username, follow=True)
        self.assertTrue(response.status_code == 200)

    def test_other_profile_view_unauthenticated_returns_status_redirect(self):
        """Test other profile view with unauthenticated client returns status code 301."""
        self.add_user()
        response = self.client.get("/profile/test_user")
        self.assertTrue(response.status_code == 301)

    def test_no_profile_authenticated_returns_status_not_found(self):
        """Test non-existing profile view with unauthenticated client returns status code 302."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    def test_no_profile_unauthenticated_returns_status_redirect(self):
        """Test non-existing profile view with unauthenticated client returns status code 302."""
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    def test_profile_route_uses_correct_template(self):
        """Test that the profile view renders the profile.html template."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get("/profile/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "profile_cfn/profile.html")

    # Marc Tues
    def test_user_does_not_have_option_to_follow_themselves(self):
        """A user should not see follow or unfollow on their own profile."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get("/profile/")
        self.assertNotContains(response, '<button type="submit" name="unfollow">Unfollow</button>')

    # Marc Tues
    def test_user_does_not_have_option_to_unfollow_themselves(self):
        """A user should not see unfollow on their own profile."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get("/profile/")
        self.assertNotContains(response, '<button type="submit" name="follow">Follow</button>')

    # Marc Tues
    def test_user_can_view_profile_button_on_their_profile(self):
        """A user should not see follow or unfollow on their own profile."""
        self.add_user()
        self.log_in_test_user()
        response = self.client.get("/profile/")
        self.assertContains(response, '<button>Update Profile</button>')

    # Marc Tues
    def test_other_user_can_be_followed_by_user(self):
        """Test that a user can be follow by user."""
        test_user = self.add_user()
        self.log_in_test_user()
        test_user2 = self.add_user('test_user2')
        self.client.post('/profile/test_user2/')
        self.assertTrue(test_user2.followed_by.first() == test_user.profile)
        self.client.post('/profile/test_user2/')
        self.assertTrue(test_user.profile not in test_user2.followed_by.all())

    # Marc Tues
    def test_user_can_follow_another_user(self):
        """Test that a user can follow another user."""
        test_user = self.add_user()
        self.log_in_test_user()
        test_user2 = self.add_user('test_user2')
        self.client.post('/profile/test_user2/')
        self.assertTrue(test_user.profile.follows.first() == test_user2)
        self.client.post('/profile/test_user2/')
        self.assertTrue(test_user2 not in test_user.profile.follows.all())

    # Marc Tues
    def test_other_user_can_be_unfollowed_by_user(self):
        """Test that a user can be unfollow by user."""
        test_user = self.add_user()
        self.log_in_test_user()
        test_user2 = self.add_user('test_user2')
        self.client.post('/profile/test_user2/')  # <-- Follow
        self.client.post('/profile/test_user2/')  # <-- Unfollow
        self.assertTrue(test_user.profile not in test_user2.followed_by.all())

    # Marc Tues
    def test_user_can_unfollow_another_user(self):
        """Test that a user can unfollow another user."""
        test_user = self.add_user()
        self.log_in_test_user()
        test_user2 = self.add_user('test_user2')
        self.client.post('/profile/test_user2/')  # <-- Follow
        self.client.post('/profile/test_user2/')  # <-- Unfollow
        self.assertTrue(test_user2 not in test_user.profile.follows.all())

    # Marc Tues
    def test_multiple_followed_users_show_up_on_profile(self):
        """Test that a user can be follow by user."""
        self.add_user()
        self.add_user('test_user2')
        self.log_in_test_user('test_user2')
        self.client.post('/profile/test_user/')
        self.add_user('test_user3')
        self.log_in_test_user('test_user3')
        self.client.post('/profile/test_user/')
        self.add_user('test_user4')
        self.log_in_test_user('test_user4')
        self.client.post('/profile/test_user/')
        self.log_in_test_user()
        response = self.client.get("/profile/")
        soup = Soup(response.rendered_content, 'html.parser')
        following_divs = soup.findAll("div", {"class": "followed_by_list"})
        self.assertTrue(len(following_divs) == 3)

    # Marc Tues
    def test_multiple_users_following_show_up_on_profile(self):
        """Test that a user can be follow by user."""
        self.add_user()
        self.log_in_test_user()
        self.add_user('test_user2')
        self.add_user('test_user3')
        self.add_user('test_user4')
        self.client.post('/profile/test_user2/')
        self.client.post('/profile/test_user3/')
        self.client.post('/profile/test_user4/')
        response = self.client.get("/profile/")
        soup = Soup(response.rendered_content, 'html.parser')
        following_divs = soup.findAll("div", {"class": "following_list"})
        self.assertTrue(len(following_divs) == 3)

    # Marc Tues
    def test_edit_profile_form_valid(self):
        """Test that the form for editing a profile is valid."""
        test_user = self.add_user()
        form = EditProfileForm(instance=test_user.profile, data={
            'First Name': 'Test',
            'Last Name': 'User',
            'about': 'this is just a test',
            'profile_picture': [self.photo],
        })
        self.assertTrue(form.is_valid())

    # Marc Tues
    def test_edit_profile_changes_profile(self):
        """Test that edit profile changes profile."""
        self.add_user()
        self.log_in_test_user()
        self.client.post("/profile/edit/", {
            'First Name': 'Test',
            'Last Name': 'User',
            'about': 'Descriptor',
            'profile_picture': [self.photo],
        })
        user = User.objects.first()
        self.assertTrue(user.profile.about == 'Descriptor')
