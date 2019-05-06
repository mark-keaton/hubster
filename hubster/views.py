from rest_framework import viewsets

from hubster.models import GithubRepo, GithubUser
from hubster.serializers import GithubRepoSerializer, GithubUserSerializer


class QuerysetFilterMixin:
    """
    Simple default queryset overriding to utilize
    Django's built-in filtering functionality.

    Assumes 'model' is declared on the class.
    """

    def get_queryset(self):
        Model = self.model
        fields = set([f.name for f in Model._meta.get_fields()])

        filters = {
            key: value
            for key, value in self.request.query_params.items()
            if any(key.startswith(field) for field in fields)
        }

        queryset = self.queryset
        for key, value in filters.items():
            if value is not None:
                queryset = queryset.filter(**{key: value})
        return queryset


class GithubUserViewSet(QuerysetFilterMixin, viewsets.ModelViewSet):
    """
    View Github users.
    """

    model = GithubUser
    serializer_class = GithubUserSerializer
    queryset = GithubUser.objects.all()


class GithubRepoViewSet(QuerysetFilterMixin, viewsets.ModelViewSet):
    """
    View Github repos.
    """

    model = GithubRepo
    queryset = GithubRepo.objects.all()
    serializer_class = GithubRepoSerializer

