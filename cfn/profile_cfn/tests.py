"""ProfileCfn Tests."""

# from django.test import TestCase, Client, RequestFactory
# from django.contrib.auth.models import User
# from profile_cfn.models import ProfileCfn
# from profile_cfn.forms import EditProfileForm
# from django.core.files.uploadedfile import SimpleUploadedFile
# from bs4 import BeautifulSoup as Soup
# import factory

# import mock


# class UserFactory(factory.django.DjangoModelFactory):
#     """User factory for testing."""

#     class Meta:
#         """Model meta."""

#         model = User

#     username = factory.Sequence(lambda n: "User{}".format(n))
#     email = factory.LazyAttribute(
#         lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
#     )

# RETURNED_JSON = """{
#   "login": "iamrobinhood12345",
#   "id": 11498059,
#   "avatar_url": "https://avatars.githubusercontent.com/u/11498059?v=3",
#   "gravatar_id": "",
#   "url": "https://api.github.com/users/iamrobinhood12345",
#   "html_url": "https://github.com/iamrobinhood12345",
#   "followers_url": "https://api.github.com/users/iamrobinhood12345/followers",
#   "following_url": "https://api.github.com/users/iamrobinhood12345/following{/other_user}",
#   "gists_url": "https://api.github.com/users/iamrobinhood12345/gists{/gist_id}",
#   "starred_url": "https://api.github.com/users/iamrobinhood12345/starred{/owner}{/repo}",
#   "subscriptions_url": "https://api.github.com/users/iamrobinhood12345/subscriptions",
#   "organizations_url": "https://api.github.com/users/iamrobinhood12345/orgs",
#   "repos_url": "https://api.github.com/users/iamrobinhood12345/repos",
#   "events_url": "https://api.github.com/users/iamrobinhood12345/events{/privacy}",
#   "received_events_url": "https://api.github.com/users/iamrobinhood12345/received_events",
#   "type": "User",
#   "site_admin": false,
#   "name": "William Benjamin Shields",
#   "company": null,
#   "blog": "https://github.com/iamrobinhood12345",
#   "location": "World",
#   "email": "bshields23@gmail.com",
#   "hireable": true,
#   "bio": "I move fast and break my computer.",
#   "public_repos": 43,
#   "public_gists": 7,
#   "followers": 3,
#   "following": 17,
#   "created_at": "2015-03-16T07:34:21Z",
#   "updated_at": "2017-02-16T04:28:57Z"
# }"""


# class BackendTests(TestCase):
#     """User/profile backend test runner."""

#     @mock.patch(
#         "profile_cfn.models.github_api_call",
#         return_value=RETURNED_JSON
#     )
#     def setUp(self, github_api_call):
#         """Set up for backend test runner."""
#         self.users = [UserFactory.create() for i in range(5)]

#     # Ben Monday
#     def test_profile_is_made_when_user_is_saved(self):
#         """Test profile created when user is registered."""
#         self.assertTrue(ProfileCfn.objects.count() == 5)

#     # Ben Monday
#     def test_profile_is_associated_with_users(self):
#         """Test profile has correct user instance."""
#         profile = ProfileCfn.objects.first()
#         username = self.users[0].username
#         self.assertTrue(profile.user.username == username)

#     def test_profile_model_returns_string(self):
#         """Test that user model returns string for Py2 compatibility."""
#         assert type(str(self.users[0])) == str

#     def test_profile_model_returns_string_part_2(self):
#         """Test that user model returns string for Py2 compatibility."""
#         assert type(str(self.users[0])) == str

#     def test_profile_model_returns_is_active(self):
#         """Test that user model returns bool on is_active."""
#         assert type((ProfileCfn.objects.first().is_active)) == bool

#     def test_inactive_profile_model_user_is_inactive(self):
#         """Test that user profile model is inactive by default."""
#         assert type((ProfileCfn.objects.first().is_active)) == bool


# class FrontendTests(TestCase):
#     """User/profile frontend test runner."""

#     @mock.patch(
#         "profile_cfn.models.github_api_call",
#         return_value=RETURNED_JSON
#     )
#     def setUp(self, github_api_call):
#         """Set up for frontend fest runner."""
#         self.client = Client()
#         self.request = RequestFactory()
#         self.photo = SimpleUploadedFile('test.jpg', open('cfn/static/images/cf_logo.png', 'rb').read())
#         self.users = [UserFactory.create() for i in range(5)]
#         for each in self.users:
#             each.password = 'testpassword'
#             each.save()

#     def log_in_test_user(self):
#         """Log in the test user."""
#         self.client.login(username=self.users[0].username, password='testpassword')

#     # Ben Monday
#     def test_profile_view_authenticated_returns_status_ok(self):
#         """Test profile view returns status code 200."""
#         self.log_in_test_user()
#         response = self.client.get('/profile', follow=True)
#         self.assertTrue(response.status_code == 200)

#     # Ben Monday
#     def test_profile_view_unauthenticated_returns_status_redirect(self):
#         """Test profile view with unauthenticated client returns status code 302."""
#         response = self.client.get("/profile/")
#         self.assertTrue(response.status_code == 302)

#     # Ben Monday
#     def test_other_profile_view_authenticated_returns_status_ok(self):
#         """Test other profile view with authenticated client returns status code 200."""
#         self.log_in_test_user()
#         new_user = self.users[1]
#         response = self.client.get(
#             '/profile/' + new_user.username, follow=True)
#         self.assertTrue(response.status_code == 200)

#     # Ben Monday
#     def test_other_profile_view_unauthenticated_returns_status_redirect(self):
#         """Test other profile view with unauthenticated client returns status code 301."""
#         response = self.client.get("/profile/test_user")
#         self.assertTrue(response.status_code == 301)

#     # Ben Monday
#     def test_no_profile_authenticated_returns_status_not_found(self):
#         """Test non-existing profile view with unauthenticated client returns status code 302."""
#         self.log_in_test_user()
#         response = self.client.get("/profile/abcdefg")
#         self.assertTrue(response.status_code == 301)

#     # Ben Monday
#     def test_no_profile_unauthenticated_returns_status_redirect(self):
#         """Test non-existing profile view with unauthenticated client returns status code 302."""
#         response = self.client.get("/profile/abcdefg")
#         self.assertTrue(response.status_code == 301)

#     # Ben Monday
#     def test_profile_route_uses_correct_template(self):
#         """Test that the profile view renders the profile.html template."""
#         self.log_in_test_user()
#         response = self.client.get("/profile/")
#         self.assertTemplateUsed(response, "base.html")
#         self.assertTemplateUsed(response, "profile_cfn/profile.html")

#     # Marc Tues
#     def test_user_does_not_have_option_to_follow_themselves(self):
#         """A user should not see follow or unfollow on their own profile."""
#         self.log_in_test_user()
#         response = self.client.get("/profile/", follow=True)
#         self.assertNotContains(response, '<button type="submit" name="unfollow">Unfollow</button>')

#     # Marc Tues
#     def test_user_does_not_have_option_to_unfollow_themselves(self):
#         """A user should not see unfollow on their own profile."""
#         self.log_in_test_user()
#         response = self.client.get("/profile/", follow=True)
#         self.assertNotContains(response, '<button type="submit" name="follow">Follow</button>')

#     # Marc Tues
#     def test_user_can_view_profile_button_on_their_profile(self):
#         """A user should not see follow or unfollow on their own profile."""
#         self.log_in_test_user()
#         response = self.client.get("/profile/", follow=True)
#         self.assertContains(response, '<button>Update Profile</button>')

#     # Marc Tues
#     def test_other_user_can_be_followed_by_user(self):
#         """Test that a user can be follow by user."""
#         test_user = self.users[0]
#         self.log_in_test_user()
#         test_user2 = self.users[1]
#         self.client.post('/profile/' + test_user2.username + '/')
#         self.assertTrue(test_user2.followed_by.first() == test_user.profile)
#         self.client.post('/profile/' + test_user2.username + '/')
#         self.assertTrue(test_user.profile not in test_user2.followed_by.all())

#     # Marc Tues
#     def test_user_can_follow_another_user(self):
#         """Test that a user can follow another user."""
#         test_user = self.users[0]
#         self.log_in_test_user()
#         test_user2 = self.users[1]
#         self.client.post('/profile/' + test_user2.username + '/')
#         self.assertTrue(test_user.profile.follows.first() == test_user2)
#         self.client.post('/profile/' + test_user2.username + '/')
#         self.assertTrue(test_user2 not in test_user.profile.follows.all())

#     # Marc Tues
#     def test_other_user_can_be_unfollowed_by_user(self):
#         """Test that a user can be unfollow by user."""
#         test_user = self.users[0]
#         self.log_in_test_user()
#         test_user2 = self.add_user('test_user2')
#         self.client.post('/profile/test_user2/')  # <-- Follow
#         self.client.post('/profile/test_user2/')  # <-- Unfollow
#         self.assertTrue(test_user.profile not in test_user2.followed_by.all())

#     # Marc Tues
#     def test_user_can_unfollow_another_user(self):
#         """Test that a user can unfollow another user."""
#         test_user = self.users[0]
#         self.log_in_test_user()
#         test_user2 = self.users[1]
#         self.client.post('/profile/test_user2/')  # <-- Follow
#         self.client.post('/profile/test_user2/')  # <-- Unfollow
#         self.assertTrue(test_user2 not in test_user.profile.follows.all())

#     # Marc Tues
#     def test_multiple_followed_users_show_up_on_profile(self):
#         """Test that a user can be follow by user."""
#         self.add_user('test_user2')
#         self.log_in_test_user('test_user2')
#         self.client.post('/profile/test_user/')
#         self.add_user('test_user3')
#         self.log_in_test_user('test_user3')
#         self.client.post('/profile/test_user/')
#         self.add_user('test_user4')
#         self.log_in_test_user('test_user4')
#         self.client.post('/profile/test_user/')
#         self.log_in_test_user()
#         response = self.client.get("/profile/")
#         soup = Soup(response.content, 'html.parser')
#         following_divs = soup.findAll("div", {"class": "followed_by_list"})
#         self.assertTrue(len(following_divs) == 3)

#     # Marc Tues
#     def test_multiple_users_following_show_up_on_profile(self):
#         """Test that a user can be follow by user."""
#         self.log_in_test_user()
#         self.add_user('test_user2')
#         self.add_user('test_user3')
#         self.add_user('test_user4')
#         self.client.post('/profile/test_user2/')
#         self.client.post('/profile/test_user3/')
#         self.client.post('/profile/test_user4/')
#         response = self.client.get("/profile/")
#         soup = Soup(response.content, 'html.parser')
#         following_divs = soup.findAll("div", {"class": "following_list"})
#         self.assertTrue(len(following_divs) == 3)

#     # Marc Tues
#     def test_edit_profile_form_valid(self):
#         """Test that the form for editing a profile is valid."""
#         test_user = self.users[0]
#         form = EditProfileForm(instance=test_user.profile, data={
#             'First Name': 'Test',
#             'Last Name': 'User',
#             'about': 'this is just a test',
#             'profile_picture': [self.photo],
#         })
#         self.assertTrue(form.is_valid())

#     # Marc Tues
#     def test_edit_profile_changes_profile(self):
#         """Test that edit profile changes profile."""
#         self.log_in_test_user()
#         self.client.post("/profile/edit/", {
#             'First Name': 'Test',
#             'Last Name': 'User',
#             'about': 'Descriptor',
#             'profile_picture': [self.photo],
#         })
#         user = User.objects.first()
#         self.assertTrue(user.profile.about == 'Descriptor')
