"""Posts tests."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from posts.models import Post
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


# class PostFactory(factory.django.DjangoModelFactory):
#     """Create test instance of Post Class."""

#     user = User(username='test')
#     user.save()

#     class Meta:
#         """Invoke post instance using Post model class."""

#         model = Post
#     author = user
#     title = factory.Sequence(lambda n: "Post{}".format(n))


class BackendTests(TestCase):
    """Posts backend test runner."""

    def setUp(self):
        """Set up for backend test runner."""
        self.users = [UserFactory.create() for i in range(5)]
        self.posts = [Post() for i in range(5)]
        for i in range(len(self.posts)):
            self.posts[i].author = self.users[i]
            self.posts[i].title = factory.Sequence(lambda n: "Post{}".format(n))
            self.posts[i].save()

    # Ben Wednesday
    def test_post_author(self):
        """"Test post has author."""
        this_post = Post.objects.all()[0]
        self.assertTrue(this_post.author == self.users[0])

    # Ben Wednesday
    def test_post_has_title(self):
        """Test post title attributed."""
        self.assertTrue(self.posts[0].title)

    # Ben Wednesday
    
