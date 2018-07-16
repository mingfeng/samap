from django.http import HttpResponse, JsonResponse

from .forms import ServiceAreaForm
from .utils import get_service_area


def service_area(request):
    form = ServiceAreaForm(request.GET)
    if form.is_valid():
        distance = form.cleaned_data['distance']
        srs = form.cleaned_data['srs']
        area = get_service_area(form.transformed_location, distance)
        area.transform(srs.srid)
        return HttpResponse(area.geojson, content_type='application/json')
    else:
        return JsonResponse(form.errors, status=400)
