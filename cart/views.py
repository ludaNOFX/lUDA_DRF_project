from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    return HttpResponse("Страница приложения store.")


def archive(request, year):
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

