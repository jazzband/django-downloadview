from six import iteritems
from django_downloadview.nginx.response import XAccelRedirectResponse


class XAccelRedirectValidator(object):
    """Utility class to validate XAccelRedirectResponse instances.

    See also :py:func:`assert_x_accel_redirect` shortcut function.

    """
    def __call__(self, test_case, response, **assertions):
        """Assert that ``response`` is a valid X-Accel-Redirect response.

        Optional ``assertions`` dictionary can be used to check additional
        items:

        * ``basename``: the basename of the file in the response.

        * ``content_type``: the value of "Content-Type" header.

        * ``redirect_url``: the value of "X-Accel-Redirect" header.

        * ``charset``: the value of ``X-Accel-Charset`` header.

        * ``with_buffering``: the value of ``X-Accel-Buffering`` header.
          If ``False``, then makes sure that the header disables buffering.
          If ``None``, then makes sure that the header is not set.

        * ``expires``: the value of ``X-Accel-Expires`` header.
          If ``False``, then makes sure that the header disables expiration.
          If ``None``, then makes sure that the header is not set.

        * ``limit_rate``: the value of ``X-Accel-Limit-Rate`` header.
          If ``False``, then makes sure that the header disables limit rate.
          If ``None``, then makes sure that the header is not set.

        """
        self.assert_x_accel_redirect_response(test_case, response)
        for key, value in iteritems(assertions):
            assert_func = getattr(self, 'assert_%s' % key)
            assert_func(test_case, response, value)

    def assert_x_accel_redirect_response(self, test_case, response):
        test_case.assertTrue(isinstance(response, XAccelRedirectResponse))

    def assert_basename(self, test_case, response, value):
        test_case.assertEqual(response.basename, value)

    def assert_content_type(self, test_case, response, value):
        test_case.assertEqual(response['Content-Type'], value)

    def assert_redirect_url(self, test_case, response, value):
        test_case.assertEqual(response['X-Accel-Redirect'], value)

    def assert_charset(self, test_case, response, value):
        test_case.assertEqual(response['X-Accel-Charset'], value)

    def assert_with_buffering(self, test_case, response, value):
        header = 'X-Accel-Buffering'
        if value is None:
            test_case.assertFalse(header in response)
        elif value:
            test_case.assertEqual(header, 'yes')
        else:
            test_case.assertEqual(header, 'no')

    def assert_expires(self, test_case, response, value):
        header = 'X-Accel-Expires'
        if value is None:
            test_case.assertFalse(header in response)
        elif not value:
            test_case.assertEqual(header, 'off')
        else:
            test_case.assertEqual(header, value)

    def assert_limit_rate(self, test_case, response, value):
        header = 'X-Accel-Limit-Rate'
        if value is None:
            test_case.assertFalse(header in response)
        elif not value:
            test_case.assertEqual(header, 'off')
        else:
            test_case.assertEqual(header, value)

    def assert_attachment(self, test_case, response, value):
        header = 'Content-Disposition'
        if value:
            test_case.assertTrue(response[header].startswith('attachment'))
        else:
            test_case.assertFalse(header in response)


def assert_x_accel_redirect(test_case, response, **assertions):
    """Make ``test_case`` assert that ``response`` is a XAccelRedirectResponse.

    Optional ``assertions`` dictionary can be used to check additional items:

    * ``basename``: the basename of the file in the response.

    * ``content_type``: the value of "Content-Type" header.

    * ``redirect_url``: the value of "X-Accel-Redirect" header.

    * ``charset``: the value of ``X-Accel-Charset`` header.

    * ``with_buffering``: the value of ``X-Accel-Buffering`` header.
      If ``False``, then makes sure that the header disables buffering.
      If ``None``, then makes sure that the header is not set.

    * ``expires``: the value of ``X-Accel-Expires`` header.
      If ``False``, then makes sure that the header disables expiration.
      If ``None``, then makes sure that the header is not set.

    * ``limit_rate``: the value of ``X-Accel-Limit-Rate`` header.
      If ``False``, then makes sure that the header disables limit rate.
      If ``None``, then makes sure that the header is not set.

    """
    validator = XAccelRedirectValidator()
    return validator(test_case, response, **assertions)
