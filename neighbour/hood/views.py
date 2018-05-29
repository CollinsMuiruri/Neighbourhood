# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import RegisterUserForm, InfoImageForm
from .models import UserProfileModel, Post, Business, Profile, Comment
import datetime as dt

# Create your views here.


@login_required(login_url='/accounts/login')
def welcome(request):
    return render(request, 'index.html')


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "registration/registration_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseForbidden()

        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        UserProfileModel.objects.create(user=user)
        return HttpResponse('User registered')


def liveshowoffs(request):
    date = dt.date.today()
    images = Post.latest_showoffs()
    return render(request, 'showme/liveshowoffs.html', {"date": date, "images": images})


def savedshowoffs(request, past_date):

    try:
        # converting data from the string url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # raising 404 error page
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(liveshowoffs)

    return render(request, 'showme/savedshowoffs.html', {"date": date})


def detail(request, image_id):
    image = Post.objects.get(id=image_id)
    return render(request, 'showme/details.html', {"image": image})


def search_results(request):
    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        searched_images = Business.search_by_business_name(search_term)
        message = f"{search_term}"

        return render(request, 'we/search.html', {"message": message, "images": searched_images})

    else:
        message = "because you haven't searched for any term "
        return render(request, 'we/search.html', {"message": message})


@login_required(login_url='/accounts/login')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = InfoImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
    else:
        form = InfoImageForm()
    return render(request, "profiles/new_image.html", {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request):
    title = 'Profile Page'
    current_user = request.user
    profile = Profile.get_profile()
    image = Post.get_images()
    comments = Comment.get_comment()
    return render(request, 'profiles/profile.html', {"title": title, "comments": comments, "image": image, "user": current_user, "profile": profile})
