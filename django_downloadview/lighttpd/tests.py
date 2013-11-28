import django_downloadview.apache.tests
from django_downloadview.lighttpd.response import XSendfileResponse


class XSendfileValidator(django_downloadview.apache.tests.XSendfileValidator):
    """Utility class to validate XSendfileResponse instances.

    See also :py:func:`assert_x_sendfile` shortcut function.

    """
    def assert_x_sendfile_response(self, test_case, response):
        test_case.assertTrue(isinstance(response, XSendfileResponse))


def assert_x_sendfile(test_case, response, **assertions):
    """Make ``test_case`` assert that ``response`` is a XSendfileResponse.

    Optional ``assertions`` dictionary can be used to check additional items:

    * ``basename``: the basename of the file in the response.

    * ``content_type``: the value of "Content-Type" header.

    * ``file_path``: the value of "X-Sendfile" header.

    """
    validator = XSendfileValidator()
    return validator(test_case, response, **assertions)
