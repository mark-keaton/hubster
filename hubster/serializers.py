from rest_framework import serializers

from hubster.models import GithubUser


class GithubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubUser
        fields = "__all__"

