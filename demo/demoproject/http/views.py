from django_downloadview import HTTPDownloadView


class SimpleURLDownloadView(HTTPDownloadView):
    def get_url(self):
        """Return URL of hello-world.txt file on GitHub."""
        return 'https://raw.githubusercontent.com' \
               '/benoitbryon/django-downloadview' \
               '/b7f660c5e3f37d918b106b02c5af7a887acc0111' \
               '/demo/demoproject/download/fixtures/hello-world.txt'


simple_url = SimpleURLDownloadView.as_view()
