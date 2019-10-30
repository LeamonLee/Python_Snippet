from django.http import HttpResponse
from django.shortcuts import render


def aboutPage(request):
    # return HttpResponse("About Page")
    return render(request, "aboutPage.html")

def homePage(request):
    # return HttpResponse("Home Page")
    return render(request, "homePage.html")