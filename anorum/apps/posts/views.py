from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("posts")


def post(request, post_id):
    response = "post %s"
    return HttpResponse(response % post_id)
