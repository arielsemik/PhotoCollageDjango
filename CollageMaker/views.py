from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import requests


def index(request):
    return render(request, 'index.html')
    # return HttpResponse("sdada2sd")
def test(request):
    print("sadasdas")
    return JsonResponse({1:"aaaa"})
def check_url_format(url: str) -> bool:
    IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'tiff']
    url_check_format = str(url).split('.')
    if len(url_check_format) >=2 and url_check_format[-1] in IMAGE_FORMATS:
        return True
    else:
        return False

def check_url_response(url:str) -> bool:
    try:
        if requests.get(url).status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.MissingSchema:
        return False

def check_url(request) -> JsonResponse:

    url = request.GET.get('url')

    if check_url_format(url) == True and check_url_response(url) ==True:
        is_valid = True
    else:
        is_valid = False
    return JsonResponse({'is_valid': is_valid})
