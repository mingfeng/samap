from django import forms
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import SpatialReference, SRSException


class ServiceAreaForm(forms.Form):
    location = forms.CharField()
    distance = forms.FloatField(min_value=0)
    srs = forms.CharField()

    def clean_location(self):
        location = self.cleaned_data['location']
        try:
            x, y = location.split(',')
            return float(x), float(y)
        except ValueError:
            raise forms.ValidationError('Invalid coordinates', code='invalid_coords')

    def clean_srs(self):
        srs = self.cleaned_data['srs']
        try:
            return SpatialReference(srs)
        except SRSException:
            raise forms.ValidationError('Invalid spatial reference system', code='invalid_srs')

    @property
    def transformed_location(self):
        x, y = self.cleaned_data['location']
        srs = self.cleaned_data['srs']
        location = Point(x, y, srid=srs.srid)
        location.transform(settings.SRID)
        return location
