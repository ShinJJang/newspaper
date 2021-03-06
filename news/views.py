from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from news.models import Thread, Vote
from news.util.parser import parse_title
from news.util.common import SortMethods


def index(request):
    """This view return index page. In index page, there is thread list.
    And thread list can be sorted by score, number of comment, date, title using paging.
    GET parameters are 'sort' and 'page'. 'sort' is sorting methods. 'page' is number of page.

    :param request: Django request object
    :return: Thread list page
    """
    try:
        sort = request.GET["sort"].strip()
        sort_method = SortMethods[sort]
        page = request.GET["page"].strip()
    except KeyError:
        sort_method = SortMethods.score
        page = 1

    if sort_method == SortMethods.date:
        thread_list = Thread.objects.order_by("-pub_date")
    elif sort_method == SortMethods.comment:
        thread_list = Thread.objects.annotate(num_comments=Count('comment')).order_by("-num_comments")
    elif sort_method == SortMethods.title:
        thread_list = Thread.objects.order_by("title")
    else:
        thread_list = Thread.objects.all()
        thread_list = sorted(thread_list, key=lambda x: x.get_score(), reverse=True)

    paginator = Paginator(thread_list, 30)

    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    context = {
        "threads": threads,
        "pages": paginator.page_range,
        "sort": sort_method.name
    }
    return render(request, "index.html", context)


def signup(request):
    """This view return signup page.

    :param request: Django request object
    :return: Signup page
    """
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
    """This view handle signup request, then if success, redirect to index page.
    If fail, redirect to signup page included error message in session.
    Key of error message on session is error.

    :param request: Django request object
    :return: If success, redirect to index. If not, redirect to signup.
    """
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
    """This view is intended to handle submission of thread.
    If submission don't include title and include url,
    then get title through function 'parse_title'.

    :param request: Django request object
    :return: If success, redirect to thread list sorted by date to check submitted thread. If not, error massage
    """
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
        return redirect("/?sort=date&page=1")

    except KeyError:
        request.session["error"] = "올바른 요청이 아닙니다"
        return redirect("new_thread")


def vote(request, thread_id):
    """This view is intended to use ajax and handle vote.
    Checking GET parameter 'is_up' decide upvote or devote.

    :param request: Django request object
    :param thread_id: Voted thread id
    :return: If success, sum of upvote and devote. if not, error message
    """
    try:
        error_message = "올바른 요청이 아닙니다"
        is_up = int(request.GET["is_up"].strip())
        if is_up == 1 or is_up == 0:
            if not request.user.is_authenticated():
                error_message = "로그인을 해주세요"
            else:
                thread = get_object_or_404(Thread, id=thread_id)
                try:
                    vote = thread.vote_set.get(user=request.user)
                except Vote.DoesNotExist:
                    thread.vote_set.create(user=request.user, is_up=is_up)
                else:
                    if vote.is_up == is_up:
                        vote.delete()
                    else:
                        vote.is_up = is_up
                        vote.save()

                json_data = '{"count":"%s"}' % thread.get_vote_count()
                return HttpResponse(json_data, content_type="application/json; charset=utf-8")
    except KeyError:
        json_data = '{"error_message":"%s"}' % "올바른 요청이 아닙니다"
        return HttpResponseBadRequest(json_data, content_type="application/json; charset=utf-8")
    else:
        json_data = '{"error_message":"%s"}' % error_message
        return HttpResponseBadRequest(json_data, content_type="application/json; charset=utf-8")