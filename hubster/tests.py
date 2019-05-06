import json

from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.test import APIRequestFactory

from hubster.models import GithubRepo, GithubUser, License
from hubster.serializers import GithubUserSerializer, GithubRepoSerializerWithId
from scraper import build_license_dict

# factory = APIRequestFactory()
# request = factory.get("/repos/")

repo_json = """
{
    "id": 1413492,
    "license": 10,
    "owner": 2,
    "archive_url": "https://api.github.com/repos/defunkt/jquery-pjax/{archive_format}{/ref}",
    "archived": false,
    "assignees_url": "https://api.github.com/repos/defunkt/jquery-pjax/assignees{/user}",
    "blobs_url": "https://api.github.com/repos/defunkt/jquery-pjax/git/blobs{/sha}",
    "branches_url": "https://api.github.com/repos/defunkt/jquery-pjax/branches{/branch}",
    "clone_url": "https://github.com/defunkt/jquery-pjax.git",
    "collaborators_url": "https://api.github.com/repos/defunkt/jquery-pjax/collaborators{/collaborator}",
    "comments_url": "https://api.github.com/repos/defunkt/jquery-pjax/comments{/number}",
    "commits_url": "https://api.github.com/repos/defunkt/jquery-pjax/commits{/sha}",
    "compare_url": "https://api.github.com/repos/defunkt/jquery-pjax/compare/{base}...{head}",
    "contents_url": "https://api.github.com/repos/defunkt/jquery-pjax/contents/{+path}",
    "contributors_url": "https://api.github.com/repos/defunkt/jquery-pjax/contributors",
    "created_at": "2011-02-26T02:44:18Z",
    "default_branch": "master",
    "deployments_url": "https://api.github.com/repos/defunkt/jquery-pjax/deployments",
    "description": "pushState + ajax = pjax",
    "disabled": false,
    "downloads_url": "https://api.github.com/repos/defunkt/jquery-pjax/downloads",
    "events_url": "https://api.github.com/repos/defunkt/jquery-pjax/events",
    "fork": false,
    "forks_count": 2082,
    "forks_url": "https://api.github.com/repos/defunkt/jquery-pjax/forks",
    "full_name": "defunkt/jquery-pjax",
    "git_commits_url": "https://api.github.com/repos/defunkt/jquery-pjax/git/commits{/sha}",
    "git_refs_url": "https://api.github.com/repos/defunkt/jquery-pjax/git/refs{/sha}",
    "git_tags_url": "https://api.github.com/repos/defunkt/jquery-pjax/git/tags{/sha}",
    "git_url": "git://github.com/defunkt/jquery-pjax.git",
    "has_downloads": true,
    "has_issues": true,
    "has_pages": false,
    "has_projects": true,
    "has_wiki": false,
    "homepage": "https://pjax.herokuapp.com",
    "hooks_url": "https://api.github.com/repos/defunkt/jquery-pjax/hooks",
    "html_url": "https://github.com/defunkt/jquery-pjax",
    "issue_comment_url": "https://api.github.com/repos/defunkt/jquery-pjax/issues/comments{/number}",
    "issue_events_url": "https://api.github.com/repos/defunkt/jquery-pjax/issues/events{/number}",
    "issues_url": "https://api.github.com/repos/defunkt/jquery-pjax/issues{/number}",
    "keys_url": "https://api.github.com/repos/defunkt/jquery-pjax/keys{/key_id}",
    "labels_url": "https://api.github.com/repos/defunkt/jquery-pjax/labels{/name}",
    "language": "JavaScript",
    "languages_url": "https://api.github.com/repos/defunkt/jquery-pjax/languages",
    "merges_url": "https://api.github.com/repos/defunkt/jquery-pjax/merges",
    "milestones_url": "https://api.github.com/repos/defunkt/jquery-pjax/milestones{/number}",
    "mirror_url": null,
    "name": "jquery-pjax",
    "network_count": 0,
    "node_id": "MDEwOlJlcG9zaXRvcnkxNDEzNDky",
    "notifications_url": "https://api.github.com/repos/defunkt/jquery-pjax/notifications{?since,all,participating}",
    "open_issues_count": 84,
    "private": false,
    "pulls_url": "https://api.github.com/repos/defunkt/jquery-pjax/pulls{/number}",
    "pushed_at": "2018-11-27T06:24:23Z",
    "releases_url": "https://api.github.com/repos/defunkt/jquery-pjax/releases{/id}",
    "size": 911,
    "ssh_url": "git@github.com:defunkt/jquery-pjax.git",
    "stargazers_count": 16365,
    "stargazers_url": "https://api.github.com/repos/defunkt/jquery-pjax/stargazers",
    "statuses_url": "https://api.github.com/repos/defunkt/jquery-pjax/statuses/{sha}",
    "subscribers_count": 0,
    "subscribers_url": "https://api.github.com/repos/defunkt/jquery-pjax/subscribers",
    "subscription_url": "https://api.github.com/repos/defunkt/jquery-pjax/subscription",
    "svn_url": "https://github.com/defunkt/jquery-pjax",
    "tags_url": "https://api.github.com/repos/defunkt/jquery-pjax/tags",
    "teams_url": "https://api.github.com/repos/defunkt/jquery-pjax/teams",
    "trees_url": "https://api.github.com/repos/defunkt/jquery-pjax/git/trees{/sha}",
    "updated_at": "2019-05-03T13:18:09Z",
    "url": "https://api.github.com/repos/defunkt/jquery-pjax",
    "watchers_count": 16365,
    "topics": []
}
"""


class GithubRepoDeserializerWithIdTestCase(TestCase):
    def setUp(self):
        build_license_dict()
        GithubUser.objects.create(id=2)

    def test_deserializer(self):
        repo_dict = json.loads(repo_json)
        serializer = GithubRepoSerializerWithId(data=repo_dict)
        repo = None
        if serializer.is_valid():
            repo = serializer.save()
        else:
            print(serializer.errors)
        self.assertIsNotNone(repo)
        self.assertEqual(repo.id, 1413492)

    def tearDown(self):
        License.objects.all().delete()
        GithubRepo.objects.get(id=1413492).delete()
        GithubUser.objects.get(id=2).delete()


class GithubRepoSerializerWithIdTestCase(TestCase):
    def setUp(self):
        build_license_dict()
        GithubUser.objects.create(id=2)
        repo_dict = json.loads(repo_json)
        serializer = GithubRepoSerializerWithId(data=repo_dict)
        repo = None
        if serializer.is_valid():
            repo = serializer.save()

    def test_serializer(self):
        repo_dict = json.loads(repo_json)
        repo = GithubRepo.objects.get(id=1413492)
        serializer = GithubRepoSerializerWithId(repo)
        self.assertEqual(serializer.data, repo_dict)
