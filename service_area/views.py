from django.http import HttpResponse, JsonResponse

from .forms import ServiceAreaForm
from .utils import get_service_area


def service_area(request):
    form = ServiceAreaForm(request.GET)
    if form.is_valid():
        x, y = form.cleaned_data['location']
        distance = form.cleaned_data['distance']
        area = get_service_area(x, y, distance)
        return HttpResponse(area, content_type='application/json')
    else:
        return JsonResponse(form.errors, status=400)
