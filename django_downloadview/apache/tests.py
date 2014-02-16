from six import iteritems
from django_downloadview.apache.response import XSendfileResponse


class XSendfileValidator(object):
    """Utility class to validate XSendfileResponse instances.

    See also :py:func:`assert_x_sendfile` shortcut function.

    """
    def __call__(self, test_case, response, **assertions):
        """Assert that ``response`` is a valid X-Sendfile response.

        Optional ``assertions`` dictionary can be used to check additional
        items:

        * ``basename``: the basename of the file in the response.

        * ``content_type``: the value of "Content-Type" header.

        * ``file_path``: the value of "X-Sendfile" header.

        """
        self.assert_x_sendfile_response(test_case, response)
        for key, value in iteritems(assertions):
            assert_func = getattr(self, 'assert_%s' % key)
            assert_func(test_case, response, value)

    def assert_x_sendfile_response(self, test_case, response):
        test_case.assertTrue(isinstance(response, XSendfileResponse))

    def assert_basename(self, test_case, response, value):
        test_case.assertEqual(response.basename, value)

    def assert_content_type(self, test_case, response, value):
        test_case.assertEqual(response['Content-Type'], value)

    def assert_file_path(self, test_case, response, value):
        test_case.assertEqual(response['X-Sendfile'], value)

    def assert_attachment(self, test_case, response, value):
        header = 'Content-Disposition'
        if value:
            test_case.assertTrue(response[header].startswith('attachment'))
        else:
            test_case.assertFalse(header in response)


def assert_x_sendfile(test_case, response, **assertions):
    """Make ``test_case`` assert that ``response`` is a XSendfileResponse.

    Optional ``assertions`` dictionary can be used to check additional items:

    * ``basename``: the basename of the file in the response.

    * ``content_type``: the value of "Content-Type" header.

    * ``file_path``: the value of "X-Sendfile" header.

    """
    validator = XSendfileValidator()
    return validator(test_case, response, **assertions)
