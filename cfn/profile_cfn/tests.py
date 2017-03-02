"""ProfileCfn Tests."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from profile_cfn.models import ProfileCfn
from profile_cfn.forms import EditProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from bs4 import BeautifulSoup as Soup
import factory

import mock


class UserFactory(factory.django.DjangoModelFactory):
    """User factory for testing."""

    class Meta:
        """Model meta."""

        model = User

    username = factory.Sequence(lambda n: "User{}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
    )

RETURNED_JSON = """{
  "avatar_url": "https://avatars.githubusercontent.com/u/11498059?v=3",
  "html_url": "https://github.com/iamrobinhood12345",
  "bio": "I move fast and break my computer.",
}"""


class BackendTests(TestCase):
    """User/profile backend test runner."""

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def setUp(self, github_api_call):
        """Set up for backend test runner."""
        self.users = [UserFactory.create() for i in range(5)]

    # Ben Monday
    def test_profile_is_made_when_user_is_saved(self):
        """Test profile created when user is registered."""
        self.assertTrue(ProfileCfn.objects.count() == 5)

    # Ben Monday
    def test_profile_is_associated_with_users(self):
        """Test profile has correct user instance."""
        profile = ProfileCfn.objects.first()
        username = self.users[0].username
        self.assertTrue(profile.user.username == username)

    # Benny
    def test_profile_model_returns_string(self):
        """Test that user model returns string for Py2 compatibility."""
        assert type(str(self.users[0])) == str

    # Benny
    def test_profile_model_returns_string_part_2(self):
        """Test that user model returns string for Py2 compatibility."""
        assert type(str(self.users[0])) == str

    # Benny
    def test_profile_model_returns_is_active(self):
        """Test that user model returns bool on is_active."""
        assert type((ProfileCfn.objects.first().is_active)) == bool

    # Benny
    def test_inactive_profile_model_user_is_inactive(self):
        """Test that user profile model is inactive by default."""
        assert type((ProfileCfn.objects.first().is_active)) == bool


class FrontendTests(TestCase):
    """User/profile frontend test runner."""

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def setUp(self, github_api_call):
        """Set up for frontend fest runner."""
        self.client = Client()
        self.request = RequestFactory()
        self.photo = SimpleUploadedFile('test.jpg', open(
            'cfn/static/images/cf_logo.png', 'rb').read())
        self.users = [UserFactory.create() for i in range(5)]

    def log_in_test_user(self):
        """Log in the test user."""
        self.client.force_login(self.users[0])

    @mock.patch(
        "profile_cfn.models.github_api_call",
        return_value=RETURNED_JSON
    )
    def make_more_users(self, github_api_call):
        """Need 13 users for paginations tests."""
        self.users = [UserFactory.create() for i in range(14)]

    # Ben Monday
    def test_profile_view_authenticated_returns_status_ok(self):
        """Test profile view returns status code 200."""
        self.log_in_test_user()
        response = self.client.get('/profile', follow=True)
        self.assertTrue(response.status_code == 200)

    # Ben Monday
    def test_profile_view_unauthenticated_returns_status_redirect(self):
        """Test profile view with unauthenticated client...

        ...returns status code 302.
        """
        response = self.client.get("/profile/")
        self.assertTrue(response.status_code == 302)

    # Ben Monday
    def test_other_profile_view_authenticated_returns_status_ok(self):
        """Test other profile view with authenticated client...

        ...returns status code 200.
        """
        self.log_in_test_user()
        new_user = self.users[1]
        response = self.client.get(
            '/profile/' + new_user.username, follow=True)
        self.assertTrue(response.status_code == 200)

    # Ben Monday
    def test_other_profile_view_unauthenticated_returns_status_redirect(self):
        """Test other profile view with unauthenticated client...

        ...returns status code 301.
        """
        response = self.client.get("/profile/test_user")
        self.assertTrue(response.status_code == 301)

    # Ben Monday
    def test_no_profile_authenticated_returns_status_not_found(self):
        """Test non-existing profile view with unauthenticated client...

        ...returns status code 302.
        """
        self.log_in_test_user()
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    # Ben Monday
    def test_no_profile_unauthenticated_returns_status_redirect(self):
        """Test non-existing profile view with unauthenticated client...

        ...returns status code 302.
        """
        response = self.client.get("/profile/abcdefg")
        self.assertTrue(response.status_code == 301)

    # Ben Monday
    def test_profile_route_uses_correct_template(self):
        """Test that the profile view renders the profile.html template."""
        self.log_in_test_user()
        response = self.client.get("/profile/")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "profile_cfn/profile.html")

    # Marc Tues
    def test_user_does_not_have_option_to_follow_themselves(self):
        """A user should not see follow or unfollow on their own profile."""
        self.log_in_test_user()
        response = self.client.get("/profile/", follow=True)
        self.assertNotContains(
            response,
            '<button type="submit" name="unfollow">Unfollow</button>')

    # Marc Tues
    def test_user_does_not_have_option_to_unfollow_themselves(self):
        """A user should not see unfollow on their own profile."""
        self.log_in_test_user()
        response = self.client.get("/profile/", follow=True)
        self.assertNotContains(
            response,
            '<button type="submit" name="follow">Follow</button>')

    # Marc Tues
    def test_user_can_view_profile_button_on_their_profile(self):
        """A user should not see follow or unfollow on their own profile."""
        self.log_in_test_user()
        response = self.client.get("/profile/", follow=True)
        self.assertContains(response, 'Update Profile')

    # Marc Tues
    def test_other_user_can_be_followed_by_user(self):
        """Test that a user can be follow by user."""
        test_user = self.users[0]
        self.log_in_test_user()
        test_user2 = self.users[1]
        url = '/profile/' + test_user2.username + '/'
        self.client.post(url, follow=True)
        self.assertTrue(test_user2.followed_by.first() == test_user.profile)
        self.client.post('/profile/' + test_user2.username + '/')
        self.assertTrue(test_user.profile not in test_user2.followed_by.all())

    # Marc Tues
    def test_user_can_follow_another_user(self):
        """Test that a user can follow another user."""
        test_user = self.users[0]
        self.log_in_test_user()
        test_user2 = self.users[1]
        self.client.post('/profile/' + test_user2.username + '/')
        self.assertTrue(test_user.profile.follows.first() == test_user2)
        self.client.post('/profile/' + test_user2.username + '/')
        self.assertTrue(test_user2 not in test_user.profile.follows.all())

    # Marc Tues
    def test_other_user_can_be_unfollowed_by_user(self):
        """Test that a user can be unfollow by user."""
        test_user = self.users[0]
        self.log_in_test_user()
        test_user2 = self.users[1]
        self.client.post(
            '/profile/' + test_user2.username + '/')  # <-- Follow
        self.client.post(
            '/profile/' + test_user2.username + '/')  # <-- Unfollow
        self.assertTrue(test_user.profile not in test_user2.followed_by.all())

    # Marc Tues
    def test_user_can_unfollow_another_user(self):
        """Test that a user can unfollow another user."""
        test_user = self.users[0]
        self.log_in_test_user()
        test_user2 = self.users[1]
        self.client.post(
            '/profile/' + test_user2.username + '/')  # <-- Follow
        self.client.post(
            '/profile/' + test_user2.username + '/')  # <-- Unfollow
        self.assertTrue(test_user2 not in test_user.profile.follows.all())

    # Marc Tues
    def test_multiple_followed_users_show_up_on_profile(self):
        """Test that a user can be follow by user."""
        test_user = self.users[0]
        url = '/profile/' + test_user.username + '/'
        self.client.force_login(self.users[1])
        self.client.post(url)
        self.client.force_login(self.users[2])
        self.client.post(url)
        self.client.force_login(self.users[3])
        self.client.post(url)
        self.log_in_test_user()
        response = self.client.get("/profile/")
        soup = Soup(response.content, 'html.parser')
        following_divs = soup.findAll("div", {"class": "followed_by_list"})
        self.assertTrue(len(following_divs) == 3)

    # Marc Tues
    def test_multiple_users_following_show_up_on_profile(self):
        """Test that a user can be follow by user."""
        self.log_in_test_user()
        self.client.post('/profile/' + self.users[1].username + '/')
        self.client.post('/profile/' + self.users[2].username + '/')
        self.client.post('/profile/' + self.users[3].username + '/')
        response = self.client.get("/profile/")
        soup = Soup(response.content, 'html.parser')
        following_divs = soup.findAll("div", {"class": "following_list"})
        self.assertTrue(len(following_divs) == 3)

    # Marc Tues
    def test_edit_profile_form_valid(self):
        """Test that the form for editing a profile is valid."""
        test_user = self.users[0]
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
        self.log_in_test_user()
        self.client.post("/profile/edit/", {
            'First Name': 'Test',
            'Last Name': 'User',
            'about': 'Descriptor',
            'profile_picture': [self.photo],
        })
        user = User.objects.first()
        self.assertTrue(user.profile.about == 'Descriptor')

    # Marc Thur
    def test_profile_redirects_home_for_non_user(self):
        """If you are not logged in you get redirected to home from profile."""
        response = self.client.get("/profile/", follow=True)
        self.assertContains(response, 'Log In / Register via Github!')

    # Marc Thur
    def test_other_profile_redirects_home_for_non_user(self):
        """If you are not logged in...

        ...you get redirected to home from other profile.
        """
        response = self.client.get(
            "/profile/" + self.users[0].username + "/", follow=True)
        self.assertContains(response, 'Log In / Register via Github!')

    def test_pagination_on_other_user_profile_works_and_handles_errors(self):
        """Pagination works on followers...

        ...and handles bad input for both the profile page
        and other profile page, 12 users are required for pagination.
        """
        self.make_more_users()
        self.log_in_test_user()
        self.client.post('/profile/' + self.users[1].username + '/')
        self.client.post('/profile/' + self.users[2].username + '/')
        self.client.post('/profile/' + self.users[3].username + '/')
        self.client.post('/profile/' + self.users[4].username + '/')
        self.client.post('/profile/' + self.users[5].username + '/')
        self.client.post('/profile/' + self.users[6].username + '/')
        self.client.post('/profile/' + self.users[7].username + '/')
        self.client.post('/profile/' + self.users[8].username + '/')
        self.client.post('/profile/' + self.users[9].username + '/')
        self.client.post('/profile/' + self.users[10].username + '/')
        self.client.post('/profile/' + self.users[11].username + '/')
        self.client.post('/profile/' + self.users[12].username + '/')
        self.client.post('/profile/' + self.users[13].username + '/')
        response = self.client.get("/profile/?followed_page=1&follows_page=2")
        self.assertTrue(response.status_code == 200)
        response = self.client.get("/profile/?followed_page=B&follows_page=A")
        self.assertTrue(response.status_code == 200)
        response = self.client.get("/profile/?followed_page=4&follows_page=4")
        self.assertTrue(response.status_code == 200)
        self.client.get("/logout")
        self.client.force_login(self.users[1])
        response = self.client.get(
            '/profile/' + self.users[0].username +
            '?followed_page=1&follows_page=2', follow=True)
        self.assertTrue(response.status_code == 200)
        response = self.client.get(
            '/profile/' + self.users[0].username +
            '?followed_page=B&follows_page=A', follow=True)
        self.assertTrue(response.status_code == 200)
        response = self.client.get(
            '/profile/' + self.users[0].username +
            '?followed_page=4&follows_page=4', follow=True)
        self.assertTrue(response.status_code == 200)

    # Benny
    def test_find_users_shows_correct_count_minus_admin(self):
        """Test find users tally subtracts 1 for admin."""
        response = self.client.get(
            '/find/users/', follow=True)
        self.assertContains(response, 'Total Users: 4')
