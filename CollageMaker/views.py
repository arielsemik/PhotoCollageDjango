import time

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import requests
from CollageMaker.models import Image_iItem, Collage
from PIL import Image
from django.core.files import File
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from .forms import CollageForms
def index(request) -> HttpResponse:
    if request.method == 'POST':
        form = CollageForms(request.POST)
        if form.is_valid():
            form_data =form.cleaned_data

            urls_not_clean = [form_data['url_1'], form_data['url_2'], form_data['url_3'], form_data['url_4'], form_data['url_5'], form_data['url_6']]
            urls = [ url for url in urls_not_clean if url != '']
            file_names = save_images(urls)


            form_width = form_data['width']
            form_height =form_data['height']
            slp = {}
            if form_height != None:
                slp['height'] = int(form_height)
            if form_width != None:
                slp['width'] = int(form_width)

            form_row = form_data['rows']
            form_column =form_data['columns']
            if form_column != None:
                slp['cols'] = int(form_column)
            if form_row != None:
                slp['rows'] = int(form_row)


            image = create_collage(file_names,**slp)


            return render(request, 'test.html',{'image':image})

    else:
        collage_form = CollageForms()
    return render(request, 'index.html',{'collage_form':collage_form})

def save_images(urls: list) -> list:
    file_names = []
    for url in urls:
        im =Image_iItem(
            image_url = url
        )
        im.save()
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        img_name = f'image_{im.pk}.jpg'
        
        im.image_file.save(img_name, File(img_temp))
        im.save()
        file_names.append(f'media/images/{img_name}')
    return file_names

def create_collage(file_names: list, width: int = 1920, height: int =1080, cols:int =3, rows:int = 2) -> File:
    while cols*rows< len(file_names):
        rows+=1
    thumbnail_width = width // cols
    thumbnail_height = height // rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []

    for p in file_names:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    item = 0
    x_coordinates = 0
    y_coordinates = 0


    for row in range(rows):
        for col in range(cols):
            if item+1 <= len(ims):
                new_im.paste(ims[item], (x_coordinates, y_coordinates))
                item += 1
                x_coordinates += thumbnail_width
            else:
                break
        y_coordinates += thumbnail_height
        x_coordinates = 0
    collage_name = '-'.join([name.split('/')[-1].split('.')[-2] for name in file_names])
    path_to_collage = f'collage_{collage_name}.jpg'
    pat = f"media/collages/{path_to_collage}"
    new_im.save(pat)

    f = open(pat, 'r+b')
    pp = File(f)
    col_imm =Collage(
        # collage=pp
    )
    col_imm.collage = pp
    col_imm.save()
    return pp

# @csrf_exempt
# def generate_collage(request):
#     height = request.POST.get('height')
#     width =  request.POST.get('width')
#     slp = {}
#
#     if height != "":
#         slp['height'] = int(height)
#     if width != "":
#         slp['width'] = int(width)
#     urls = json.loads(request.POST.get('urls')).values()
#     urls_list = [url for url in urls if url != '']
#
#
#     file_names =save_images(urls_list)
#     image = create_collage(file_names,**slp)
#     print('adasdsa')
#     # return redirect('generate_collage')
#     # return render(request,'generated_collage.html', {'collage': image})
#     print(type(image))
#     # Image.open(image).show()
#     aa =Image_iItem.objects.all()[0]
#     print(aa)
#     print(type(aa))
#     # return HttpResponse({'image':aa})
#     return render(request,'test.html',{'imm':image})

# def check_url_format(url: str) -> bool:
#     IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'tiff']
#     url_check_format = str(url).split('.')
#     if len(url_check_format) >= 2 and url_check_format[-1] in IMAGE_FORMATS:
#         return True
#     else:
#         return False

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

    # if check_url_format(url) == True and check_url_response(url) ==True:
    # if  check_url_response(url) ==True:
    #     is_valid = True
    # else:
    #     is_valid = False
    return JsonResponse({'is_valid': check_url_response(url)})
