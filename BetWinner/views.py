# import it
import json

import os
from django.http import JsonResponse


def my_json_view(request):
    # do something with the your data
    data = {"JsonView": True}

    # just return a JsonResponse
    return JsonResponse(data)


def my_data_view(request):
    # do something with the your data
    data_path = os.path.join("DataDownloader", "data", "data.txt")
    with open(data_path) as json_file:
        data = json.load(json_file)
    # just return a JsonResponse
    return JsonResponse(data, safe=False)
