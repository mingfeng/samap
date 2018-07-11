from django import forms


class ServiceAreaForm(forms.Form):
    location = forms.CharField()
    distance = forms.FloatField(min_value=0)

    def clean_location(self):
        location = self.cleaned_data['location']
        try:
            x, y = location.split(',')
            return float(x), float(y)
        except ValueError:
            raise forms.ValidationError('Invalid coordinates', code='invalid_coords')
