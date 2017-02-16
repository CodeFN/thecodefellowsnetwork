"""Posts tests."""

# from django.test import TestCase, Client, RequestFactory
# from django.contrib.auth.models import User
# from posts.models import Post
# import factory


# class UserFactory(factory.django.DjangoModelFactory):
#     """User factory for testing."""

#     class Meta:
#         """Model meta."""

#         model = User

#     username = factory.Sequence(lambda n: "User{}".format(n))
#     email = factory.LazyAttribute(
#         lambda x: "{}@imager.com".format(x.username.replace(" ", ""))
#     )


# class BackendTests(TestCase):
#     """Posts backend test runner."""

#     def setUp(self):
#         """Set up for backend test runner."""
#         self.users = [UserFactory.create() for i in range(5)]
#         self.posts = [Post() for i in range(5)]
#         for i in range(len(self.posts)):
#             self.posts[i].author = self.users[i]
#             self.posts[i].title = factory.Sequence(lambda n: "Post{}".format(n))
#             self.posts[i].save()

#     # Ben Wednesday
#     def test_posts_exist(self):
#         """Count posts."""
#         self.assertTrue(Post.objects.all().count() == 5)

#     # Ben Wednesday
#     def test_post_author(self):
#         """"Test post has author."""
#         this_post = Post.objects.all()[0]
#         self.assertTrue(this_post.author == self.users[0])

#     # Ben Wednesday
#     def test_post_has_title(self):
#         """Test post title attributed."""
#         self.assertTrue(self.posts[0].title)


# class FrontEndTests(TestCase):
#     """Posts frontend test runner."""

#     def setUp(self):
#         """Set up for frontend test runner."""
#         self.client = Client()
#         self.request = RequestFactory()

#     def add_user(self, username='test_user'):
#         """Make a user and return his profile."""
#         user = UserFactory.create()
#         user.username = username
#         user.set_password('testpassword')
#         user.save()
#         return user

#     def log_in_test_user(self, username='test_user'):
#         """Log in the test user."""
#         self.client.login(username=username, password='testpassword')

#     # Ben Wednesday
#     def test_post_view_authenticated_user_returns_status_ok(self):
#         """Test post view returns status code 200."""
#         this_user = self.add_user()
#         self.log_in_test_user()
#         this_post = Post()
#         this_post.author = this_user
#         this_post.save()
#         response = self.client.get('/posts/' + str(this_post.id), follow=True)
#         self.assertTrue(response.status_code == 200)

#     # Ben Wednesday
#     def test_other_user_post_view_authenticated_user_returns_status_ok(self):
#         """Test other post view with authenticated client returns status code 200."""
#         this_user = self.add_user()
#         this_post = Post()
#         this_post.author = this_user
#         this_post.save()
#         other_user = self.add_user(username='other_user')
#         self.log_in_test_user(username='other_user')
#         response = self.client.get('/posts/' + str(this_post.id), follow=True)
#         self.assertTrue(response.status_code == 200)
