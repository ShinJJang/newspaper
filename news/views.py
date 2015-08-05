from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "signup.html")


def signup_submit(request):
    return redirect("index")