from django_downloadview import HTTPDownloadView


class SimpleURLDownloadView(HTTPDownloadView):
    def get_url(self):
        """Return URL of hello-world.txt file on GitHub."""
        return (
            "https://raw.githubusercontent.com"
            "/jazzband/django-downloadview"
            "/b7f660c5e3f37d918b106b02c5af7a887acc0111"
            "/demo/demoproject/download/fixtures/hello-world.txt"
        )


class GithubAvatarDownloadView(HTTPDownloadView):
    def get_url(self):
        return "https://avatars0.githubusercontent.com/u/235204"


simple_url = SimpleURLDownloadView.as_view()
avatar_url = GithubAvatarDownloadView.as_view()
