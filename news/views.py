from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from news.models import Thread
from django.contrib.auth.decorators import login_required
from news.parser import parse_title


def index(request):
    return render(request, "index.html")


def signup(request):
    try:
        if request.session["error"]:
            error_message = request.session["error"]
            del request.session["error"]
    except KeyError:
        error_message = None

    context = {
        "error_message": error_message
    }
    return render(request, "signup.html", context)


def signup_submit(request):
    try:
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        confirm_password = request.POST["confirm_password"].strip()
        email = request.POST["email"].strip()

        if username and password and confirm_password:
            if password == confirm_password:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                return redirect("index")
    except KeyError:
        request.session["error"] = "올바른 요청이 아닙니다"
        return redirect("signup")
    except IntegrityError:
        request.session["error"] = "이미 존재하는 계정입니다"
        return redirect("signup")
    else:
        request.session["error"] = "입력한 정보가 올바르지 않습니다"
        return redirect("signup")


def user_logout(request):
    logout(request)
    return redirect("index")


def newest_list(request):
    context = {
        "threads": Thread.objects.order_by('-pub_date')[:20]
    }
    return render(request, 'newest_list.html', context)


def read_thread(request, thread_id):
    context = {
        "thread": get_object_or_404(Thread, id=thread_id)
    }
    return render(request, 'thread.html', context)


@login_required
def new_thread(request):
    try:
        if request.session["error"]:
            error_message = request.session["error"]
            del request.session["error"]
    except KeyError:
        error_message = None

    context = {
        "error_message": error_message
    }
    return render(request, 'new_thread.html', context)


@login_required
def submit_thread(request):
    try:
        title = request.POST["title"].strip()
        url = request.POST["url"].strip()
        content = request.POST["content"].strip()

        if not title and not url:
            request.session["error"] = "입력한 정보가 올바르지 않습니다"
            return redirect("new_thread")

        elif not title and url:
            title = parse_title(url)

        thread = Thread(title=title, url=url, content=content, writer_id=request.user.id)
        thread.save()
        return redirect("newest_list")

    except KeyError:
        request.session["error"] = "올바른 요청이 아닙니다"
        return redirect("new_thread")