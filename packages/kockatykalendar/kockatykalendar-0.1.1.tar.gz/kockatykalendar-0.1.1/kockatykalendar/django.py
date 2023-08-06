from django.http import JsonResponse

from kockatykalendar import scheme_version
from kockatykalendar.generators import CalendarGenerator


def kockatykalendar_json(request, generators):
    if isinstance(generators, CalendarGenerator):
        generators = [generators]

    data = []
    for generator in generators:
        data += generator.to_json()

    return JsonResponse({
        "data": data,
        "_kk_version": scheme_version
    })
