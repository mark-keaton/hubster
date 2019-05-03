from rest_framework import viewsets

from hubster.models import GithubRepo, GithubUser
from hubster.serializers import GithubRepoSerializer, GithubUserSerializer


class GithubUserViewSet(viewsets.ModelViewSet):
    """
    View Github users.
    """

    queryset = GithubUser.objects.all()
    serializer_class = GithubUserSerializer


class GithubRepoViewSet(viewsets.ModelViewSet):
    """
    View Github repos.
    """

    queryset = GithubRepo.objects.all()
    serializer_class = GithubRepoSerializer

