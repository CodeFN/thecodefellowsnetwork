"""Views for CFN."""
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User


class HomeView(TemplateView):
    """Home View."""

    template_name = 'cfn/home.html'


class FindUserView(ListView):
    """Class-based view for my list of user profiles."""

    model = User
    template_name = "cfn/find_user.html"
    context_object_name = "fellows"
    paginate_by = 72
    queryset = User.objects.all().order_by('username')

