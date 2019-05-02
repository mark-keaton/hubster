from rest_framework import viewsets

from hubster.models import GithubUser
from hubster.serializers import GithubUserSerializer


class GithubUserViewSet(viewsets.ModelViewSet):
    """
    View Github users.
    """

    queryset = GithubUser.objects.all()
    serializer_class = GithubUserSerializer
