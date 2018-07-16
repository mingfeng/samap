from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.gis.geos import Point, Polygon
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..views import service_area

TEST_SERVICE_AREA = Polygon([[0,0], [1,0], [1,1], [0,1], [0,0]], srid=settings.SRID)


class TestServiceArea(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_return_service_area_for_valid_query_params(self):
        url = '{0}?{1}'.format(reverse('service_area:service-area'), 'location=60,20&distance=100&srs=EPSG:4326')
        request = self.factory.get(url)

        with patch(
            'service_area.views.get_service_area',
            MagicMock(return_value=TEST_SERVICE_AREA),
        ) as mock_get_service_area:
            response = service_area(request)
            self.assertEqual(response.status_code, 200)
            location = Point(60, 20, srid=4326)
            location.transform(settings.SRID)
            mock_get_service_area.assert_called_once_with(location, 100)

    def test_return_bad_request_for_invalid_query_params(self):
        url = '{0}?{1}'.format(reverse('service_area:service-area'), 'location=abc,123&distance=100&srs=EPSG:4326')
        request = self.factory.get(url)
        response = service_area(request)
        self.assertEqual(response.status_code, 400)

    def test_return_bad_request_for_invalid_srs(self):
        url = '{0}?{1}'.format(reverse('service_area:service-area'), 'location=abc,123&distance=100&srs=EPSG:-123')
        request = self.factory.get(url)
        response = service_area(request)
        self.assertEqual(response.status_code, 400)
