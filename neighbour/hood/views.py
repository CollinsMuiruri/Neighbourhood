# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterUserForm, InfoImageForm, EditProfile, SocialDetailsForm
from .models import UserProfileModel, Post, Business, Profile, NeighbourhoodDetails
import datetime as dt

# Create your views here.


@login_required(login_url='/accounts/login')
def welcome(request):
    '''
    the home page
    '''
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def chat(request):
    '''
    Where notices, businesses and social contacts are shown
    '''
    post = Post.objects.all()
    public = NeighbourhoodDetails.objects.all()
    return render(request, 'the_real_home.html', {"post": post, "public": public})


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


def detail(request, image_id):
    '''
    Where details of a clicked post are seen
    '''
    image = Post.objects.get(id=image_id)
    return render(request, 'we/details.html', {"image": image})


def search_results(request):
    '''
    searching for businesses
    '''
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
    '''
    posting a new post
    '''
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
    '''
    the user profile
    '''
    title = 'Profile Page'
    current_user = request.user
    profile = Profile.get_profile()
    image = Post.get_images()
    return render(request, 'profiles/profile.html', {"title": title, "image": image, "user": current_user, "profile": profile})


@login_required(login_url='/accounts/login/')
def edit(request):
    '''
    the profile editing view
    '''
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            current_user = request.user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', current_user.id)
    else:
        form = EditProfile()
    return render(request, 'profiles/change_profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def social_ammenities(request):
    current_user = request.user
    if request.method == 'POST':
        form = SocialDetailsForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.user = current_user
            social.save()
            return redirect('homepage')
    else:
        form = SocialDetailsForm()
    return render(request, 'we/neighbourhood_details.html', {"form": form})


@login_required(login_url='/accounts/login')
def error(request):
    '''
    the error page
    '''
    return render(request, 'we/home.html')
