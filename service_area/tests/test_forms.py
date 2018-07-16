from django import forms
from django.conf import settings
from django.contrib.gis.gdal import SpatialReference
from django.test import TestCase

from ..forms import ServiceAreaForm


class TestServiceAreaForm(TestCase):

    def test_transformed_location(self):
        form_data = {
            'location': '60,20',
            'distance': 100,
            'srs': 'EPSG:4326'
        }
        form = ServiceAreaForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.transformed_location.srid, settings.SRID)

    def test_clean_location_returns_float_coordinates(self):
        form = ServiceAreaForm()
        form.cleaned_data = {
            'location': '123.5,456.7'
        }
        try:
            x, y = form.clean_location()
            self.assertEqual(x, 123.5)
            self.assertEqual(y, 456.7)
        except forms.ValidationError:
            self.fail('Should not raise ValidationError for valid coordinates')

    def test_clean_location_raise_validation_error_for_invalid_coordinates(self):
        form = ServiceAreaForm()
        form.cleaned_data = {
            'location': 'abc,123'
        }
        try:
            form.clean_location()
            self.fail('Should raise ValidationError for invalid coordinates')
        except forms.ValidationError as e:
            self.assertEqual(e.code, 'invalid_coords')

    def test_clean_srs_return_spatial_reference_object(self):
        form = ServiceAreaForm()
        form.cleaned_data = {
            'srs': 'EPSG:4326'
        }
        try:
            srs = form.clean_srs()
            self.assertIsInstance(srs, SpatialReference)
            self.assertEqual(srs.srid, 4326)
        except forms.ValidationError:
            self.faile('Should not raise ValidationError for valid spatial reference system')

    def test_clean_raise_validation_error_for_invalid_cooridnates(self):
        form = ServiceAreaForm()
        form.cleaned_data = {
            'srs': 'EPSG:-123'
        }
        try:
            form.clean_srs()
            self.fail('Should raise ValidationError for invalid spatial reference system')
        except forms.ValidationError as e:
            self.assertEqual(e.code, 'invalid_srs')
