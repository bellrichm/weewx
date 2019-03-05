#
#    Copyright (c) 2019 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Test restx services"""

import time
import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from six.moves import queue
from six.moves import urllib
from six.moves import http_client

import weewx
import weewx.restx


def get_patcher(response_body=[]):
    patcher = mock.patch('weewx.restx.urllib.request.urlopen')
    mock_urlopen = patcher.start()
    mock_urlopen.return_value = mock.MagicMock(name='return value')
    mock_urlopen.return_value.code = 200
    mock_urlopen.return_value.__iter__.return_value = iter(response_body)
    return mock_urlopen


class MatchRequest(object):
    """Allows equality testing against Request objects"""

    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent

    def __eq__(self, other):
        # In what follows, we could just return 'False', but raising the AssertionError directly
        # gives a more useful error message.

        other_split = urllib.parse.urlsplit(other._Request__original)
        other_query = urllib.parse.parse_qs(other_split.query)
        my_split = urllib.parse.urlsplit(self.url)
        my_query = urllib.parse.parse_qs(my_split.query)

        if other_split.hostname != my_split.hostname:
            raise AssertionError("Mismatched hostnames: \nActual:'%s'\nExpect:'%s' " % (other_split.hostname, my_split.hostname))
        if other_query != my_query:
            raise AssertionError("Mismatched queries: \nActual:'%s'\nExpect:'%s' " % (other_query, my_query))
        if other.headers.get('User-agent') != self.user_agent:
            raise AssertionError("Mismatched user-agent: \nActual:'%s'\nExpect:'%s'"
                                 % (other.headers.get('User-agent'), self.user_agent))
        return True


class TestAmbient(unittest.TestCase):
    """Test the Ambient RESTful protocol"""

    station = 'KBZABCDEF3'
    password = 'somepassword'
    server_url = 'http://www.testserver.com/testapi'

    def test_request(self):
        """Test that we are forming the right Request object"""

        mock_urlopen = get_patcher()
        try:
            # mock_response = mock.MagicMock()
            # mock_response.code = 200
            # mock_urlopen.return_value = mock_response
            # mock_response.__iter__.return_value = iter([b'ERROR'])
            #
            q = queue.Queue()
            obj = weewx.restx.AmbientThread(q,
                                            manager_dict=None,
                                            station=TestAmbient.station,
                                            password=TestAmbient.password,
                                            server_url=TestAmbient.server_url,
                                            )
            ts = time.mktime(time.strptime("2018-03-22", "%Y-%m-%d"))
            record = {'dateTime': ts,
                      'usUnits': weewx.US,
                      'interval': 5,
                      'outTemp': 20.0,
                      'barometer': 30.1
                      }
            q.put(record)
            q.put(None)
            obj.run()

            matcher = MatchRequest('%s?action=updateraw&ID=%s&PASSWORD=%s&softwaretype=weewx-%s'
                                   '&dateutc=2018-03-22%%2007%%3A00%%3A00'
                                   '&baromin=30.100&tempf=20.0'
                                   % (TestAmbient.server_url,
                                      TestAmbient.station,
                                      TestAmbient.password,
                                      weewx.__version__),
                                   'weewx/%s' % weewx.__version__)

            mock_urlopen.assert_called_once_with(matcher, data=None, timeout=10)
        finally:
            mock_urlopen.stop()


if __name__ == '__main__':
    unittest.main()