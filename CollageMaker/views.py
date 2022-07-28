from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from CollageMaker.models import Image_iItem, Collage
from PIL import Image
from django.core.files import File
from tempfile import NamedTemporaryFile
from urllib.request import urlopen, Request

from .forms import CollageForms


def index(request) -> HttpResponse:
    if request.method == "POST":
        form = CollageForms(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            urls_not_clean = [
                form_data["url_1"],
                form_data["url_2"],
                form_data["url_3"],
                form_data["url_4"],
                form_data["url_5"],
                form_data["url_6"],
            ]
            urls = [url for url in urls_not_clean if url != ""]
            file_names = save_images(urls)

            form_width = form_data["width"]
            form_height = form_data["height"]
            slp = {}
            if form_height != None:
                slp["height"] = int(form_height)
            if form_width != None:
                slp["width"] = int(form_width)

            form_row = form_data["rows"]
            form_column = form_data["columns"]
            if form_column != None:
                slp["cols"] = int(form_column)
            if form_row != None:
                slp["rows"] = int(form_row)

            image = generate_collage(file_names, **slp)

            return render(request, "generated.html", {"image": image})

    else:
        collage_form = CollageForms()
    return render(request, "index.html", {"collage_form": collage_form})


def download_image(url: str) -> NamedTemporaryFile:
    img_temp = NamedTemporaryFile(delete=True)
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    headers = {"User-Agent": user_agent}
    req = Request(url, headers=headers)

    img_temp.write(urlopen(req).read())
    img_temp.flush()
    return img_temp


def save_images(urls: list) -> list:
    file_names = []
    for url in urls:
        im = Image_iItem(image_url=url)
        im.save()
        img_name = f"image_{im.pk}.jpg"
        img_temp = download_image(url)
        im.image_file.save(img_name, File(img_temp))
        im.save()
        file_names.append(f"media/images/{img_name}")
    return file_names


def resize_images(
    file_names: list, width: int, height: int, cols: int, rows: int
) -> tuple:
    while cols * rows < len(file_names):
        rows += 1
    thumbnail_width = width // cols
    thumbnail_height = height // rows
    size = thumbnail_width, thumbnail_height
    ims = []

    for p in file_names:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    return ims, thumbnail_height, thumbnail_width


def create_collage(
    rows: int,
    cols: int,
    ims: list,
    thumbnail_height: int,
    thumbnail_width: int,
    width: int,
    height: int,
) -> Image:
    item = 0
    x_coordinates = 0
    y_coordinates = 0
    new_im = Image.new("RGB", (width, height))

    for row in range(rows):
        for col in range(cols):
            if item + 1 <= len(ims):
                new_im.paste(ims[item], (x_coordinates, y_coordinates))
                item += 1
                x_coordinates += thumbnail_width
            else:
                break
        y_coordinates += thumbnail_height
        x_coordinates = 0
    return new_im


def create_namespace(file_names: list) -> str:
    collage_name_clean = "-".join(
        [name.split("_")[-1].split(".")[-2] for name in file_names]
    )
    collage_name = f"collage_{collage_name_clean}.jpg"
    return f"media/collages/{collage_name}"


def generate_collage(
    file_names: list,
    width: int = 1920,
    height: int = 1080,
    cols: int = 3,
    rows: int = 2,
) -> File:

    parameters = {
        "file_names": file_names,
        "width": width,
        "height": height,
        "cols": cols,
        "rows": rows,
    }
    ims, thumbnail_height, thumbnail_width = resize_images(**parameters)

    parameters = {
        "ims": ims,
        "thumbnail_height": thumbnail_height,
        "thumbnail_width": thumbnail_width,
        "width": width,
        "height": height,
        "cols": cols,
        "rows": rows,
    }
    new_im = create_collage(**parameters)
    path_to_collage = create_namespace(file_names)

    # TODO Przerobić aby tworzyło się w temp
    new_im.save(path_to_collage)
    f = open(path_to_collage, "r+b")
    image_as_File = File(f)

    col_imm = Collage()

    col_imm.collage = image_as_File
    col_imm.save()
    return image_as_File


def check_url_format(url: str) -> bool:
    IMAGE_FORMATS = ["jpg", "jpeg", "png", "tiff"]
    url_check_format = str(url).split(".")
    if len(url_check_format) >= 2 and url_check_format[-1] in IMAGE_FORMATS:
        return True
    else:
        return False


def check_url_response(url: str) -> bool:
    try:
        if requests.get(url).status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.MissingSchema:
        return False


def check_url(request) -> JsonResponse:
    url = request.GET.get("url")

    if check_url_response(url) == True and check_url_format(url) == True:

        return JsonResponse({"is_valid": True})
    else:
        return JsonResponse({"is_valid": False})
