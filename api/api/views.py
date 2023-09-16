# Imports
import json

from django.http import HttpRequest, HttpResponse


# Views
def root(request: HttpRequest) -> HttpResponse:
    """The root view"""
    
    return HttpResponse(json.dumps({"test": "OK"}), content_type="application/json; charset=utf-8")