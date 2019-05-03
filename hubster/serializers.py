from rest_framework import serializers

from hubster.models import GithubUser, GithubRepo, License


class GithubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubUser
        fields = "__all__"


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = "__all__"


class GithubRepoSerializer(serializers.ModelSerializer):
    """
    GithubRepo serializer/deserializer for working with
    nested objects for License and Owner
    """

    license = LicenseSerializer()
    owner = GithubUserSerializer()

    class Meta:
        model = GithubRepo
        fields = "__all__"
        depth = 1


class GithubRepoSerializerWithId(GithubRepoSerializer):
    """
    GithubRepo serializer/deserializer for working with
    integer values representing foreign keys to License and Owner.
    """

    license = serializers.PrimaryKeyRelatedField(queryset=License.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=GithubUser.objects.all())
