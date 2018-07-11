from django import forms
from django.test import TestCase

from ..forms import ServiceAreaForm


class TestServiceAreaForm(TestCase):

    def test_clean_location_do_not_raise_validation_error_for_valid_coordinates(self):
        form = ServiceAreaForm()
        form.cleaned_data = {
            'location': '123,456'
        }
        try:
            form.clean_location()
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
