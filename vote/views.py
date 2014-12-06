from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
@csrf_exempt
def post(request):
	print request.body
	return HttpResponse("OK")