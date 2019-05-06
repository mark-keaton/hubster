from django.db import models


class GithubUser(models.Model):
    id = models.IntegerField(primary_key=True)

    avatar_url = models.URLField()
    bio = models.TextField(blank=True)
    blog = models.URLField(blank=True)
    company = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(null=True)
    email = models.EmailField(blank=True)
    events_url = models.URLField()
    followers = models.IntegerField(default=0)
    followers_url = models.URLField()
    following = models.IntegerField(default=0)
    following_url = models.URLField()
    gists_url = models.URLField()
    gravatar_id = models.CharField(max_length=50, blank=True)
    hireable = models.BooleanField(default=False)
    html_url = models.URLField()
    location = models.CharField(max_length=50, blank=True)
    login = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True)
    node_id = models.CharField(max_length=32)
    organizations_url = models.URLField()
    public_gists = models.IntegerField(default=0)
    public_repos = models.IntegerField(default=0)
    received_events_url = models.URLField()
    repos_url = models.URLField()
    site_admin = models.BooleanField(default=False)
    starred_url = models.URLField()
    subscriptions_url = models.URLField()
    type = models.CharField(max_length=32)
    updated_at = models.DateTimeField(null=True)
    url = models.URLField()


class License(models.Model):
    id = models.IntegerField(primary_key=True)

    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    node_id = models.CharField(max_length=32)
    spdx_id = models.CharField(max_length=32)
    url = models.CharField(max_length=200)


class Topic(models.Model):
    name = models.CharField(max_length=60)


class GithubRepo(models.Model):
    id = models.IntegerField(primary_key=True)

    archive_url = models.URLField()
    archived = models.BooleanField(default=False)
    assignees_url = models.URLField()
    blobs_url = models.URLField()
    branches_url = models.URLField()
    clone_url = models.URLField()
    collaborators_url = models.URLField()
    comments_url = models.URLField()
    commits_url = models.URLField()
    compare_url = models.URLField()
    contents_url = models.URLField()
    contributors_url = models.URLField()
    created_at = models.DateTimeField(null=True)
    default_branch = models.CharField(max_length=50)
    deployments_url = models.URLField()
    description = models.TextField(null=True)
    disabled = models.BooleanField(default=False)
    downloads_url = models.URLField()
    events_url = models.URLField()
    fork = models.BooleanField(default=False)
    forks_count = models.IntegerField()
    forks_url = models.URLField()
    full_name = models.CharField(max_length=60)
    git_commits_url = models.URLField()
    git_refs_url = models.URLField()
    git_tags_url = models.URLField()
    git_url = models.CharField(max_length=200)
    has_downloads = models.BooleanField(default=False)
    has_issues = models.BooleanField(default=False)
    has_pages = models.BooleanField(default=False)
    has_projects = models.BooleanField(default=False)
    has_wiki = models.BooleanField(default=False)
    homepage = models.URLField(blank=True, null=True)
    hooks_url = models.URLField()
    html_url = models.URLField()
    issue_comment_url = models.URLField()
    issue_events_url = models.URLField()
    issues_url = models.URLField()
    keys_url = models.URLField()
    labels_url = models.URLField()
    language = models.CharField(max_length=50, null=True)
    languages_url = models.URLField()
    license = models.ForeignKey(
        License, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    merges_url = models.URLField()
    milestones_url = models.URLField()
    mirror_url = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50)
    network_count = models.IntegerField(default=0)
    node_id = models.CharField(max_length=32)
    notifications_url = models.URLField()
    open_issues_count = models.IntegerField()
    owner = models.ForeignKey(GithubUser, null=False, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    pulls_url = models.URLField()
    pushed_at = models.DateTimeField(null=True)
    releases_url = models.URLField()
    size = models.IntegerField()
    ssh_url = models.CharField(max_length=200)
    stargazers_count = models.IntegerField(default=0)
    stargazers_url = models.URLField()
    statuses_url = models.URLField()
    subscribers_count = models.IntegerField(default=0)
    subscribers_url = models.URLField()
    subscription_url = models.URLField()
    svn_url = models.URLField()
    tags_url = models.URLField()
    teams_url = models.URLField()
    topics = models.ManyToManyField(Topic)
    trees_url = models.URLField()
    updated_at = models.DateTimeField(null=True)
    url = models.URLField()
    watchers_count = models.IntegerField(default=0)
