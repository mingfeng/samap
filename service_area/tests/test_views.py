from unittest.mock import patch, MagicMock

from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..views import service_area

TEST_SERVICE_AREA = b'{"type":"Polygon","coordinates":[[[0,0], [1,0], [1,1], [0,1], [0,0]]}'


class TestServiceArea(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_return_service_area_for_valid_query_params(self):
        url = '{0}?{1}'.format(reverse('service_area:service-area'), 'location=123,456&distance=100')
        request = self.factory.get(url)

        with patch(
            'service_area.views.get_service_area',
            MagicMock(return_value=TEST_SERVICE_AREA),
        ) as mock_get_service_area:
            response = service_area(request)
            self.assertEqual(response.content, TEST_SERVICE_AREA)
            self.assertEqual(response.status_code, 200)
            mock_get_service_area.assert_called_once_with(123, 456, 100)

    def test_return_bad_request_for_invalid_query_params(self):
        url = '{0}?{1}'.format(reverse('service_area:service-area'), 'location=abc,123&distance=100')
        request = self.factory.get(url)
        response = service_area(request)
        self.assertEqual(response.status_code, 400)
