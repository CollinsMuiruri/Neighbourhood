# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterUserForm, InfoImageForm, EditProfile, SocialDetailsForm, BusinessForm, NewNeighbourhoodForm
from .models import UserProfileModel, Post, Business, Profile, NeighbourhoodDetails, Neighbourhood, Join
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
    posts = Post.objects.all()
    contacts = NeighbourhoodDetails.objects.all()
    print(contacts)
    return render(request, 'we/contacts.html', {"posts": posts, "contacts": contacts})


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
            return redirect('index')
    else:
        form = InfoImageForm()
    return render(request, "profiles/new_image.html", {"form": form})


@login_required(login_url='/accounts/login/')
def detail(request, image_id):
    '''
    Where details of a clicked post are seen
    '''
    image = Post.objects.get(id=image_id)
    return render(request, 'we/details.html', {"image": image})


def posts(request):
    posts = Post.objects.all()
    return render(request, 'the_real_home.html', {"posts": posts})


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
            return redirect('profile')
    else:
        form = EditProfile()
    return render(request, 'profiles/change_profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def social_details(request):
    '''
    social contacts view
    '''
    current_user = request.user
    if request.method == 'POST':
        form = SocialDetailsForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.user = current_user
            social.save()
            return redirect('social')
    else:
        form = SocialDetailsForm()
    return render(request, 'we/social_details.html', {"form": form})


@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user = request.user
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
            return redirect('businesses')
    else:
        form = BusinessForm()
    return render(request, 'we/new_business.html', {"form": form})


@login_required(login_url='/accounts/login/')
def business_details(request, image_id):
    '''
    Where details of a clicked post are seen
    '''
    image = Post.objects.get(id=image_id)
    return render(request, 'we/business_details.html', {"image": image})


@login_required(login_url='/accounts/login/')
def social(request, image_id):
    '''
    Where social contacts are seen
    '''
    image = NeighbourhoodDetails.objects.get(id=image_id)
    return render(request, 'we/business_details.html', {"image": image})


@login_required(login_url='/accounts/login/')
def new_neighbourhood(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewNeighbourhoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.save()
            return redirect('neighbourhoods')
    else:
        form = NewNeighbourhoodForm()
    return render(request, 'we/new_neighbourhood.html', {"form": form})


@login_required(login_url='/accounts/login/')
def businesses(request):
    business = Business.objects.all()
    return render(request, 'we/businesses.html', {"business": business})


@login_required(login_url='/accounts/login/')
def neighbourhoods(request):
    neighbourhoods = Neighbourhood.objects.all()
    return render(request, 'we/neighbourhoods.html', {"neighbourhoods": neighbourhoods})


@login_required(login_url='/accounts/login')
def error(request):
    '''
    the error page
    '''
    return render(request, 'we/home.html')


def join(request, hoodId):
    '''
    This view function will enable new users join a given neighbourhood
    '''
    neighbourhood = Neighbourhood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
        return redirect('neighbourhoods')
    else:
        Join(user_id=request.user, hood_id=neighbourhood).save()
        return redirect('neighbourhoods')


def exitHood(request, hoodId):
    '''
    View function to delete a user from a neighbourhood instance in the join table
    '''
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.get(user_id=request.user).delete()

        return redirect('index')

# def chatty(request):
#     if request.method == 'POST':
#         post_form = InfoImageForm(request.POST)
#         if post_form.is_valid():
#             post_form.save()
#
#     else:
#         post_form = InfoImageForm()
#
#     return render(request, 'profiles/new_image.html', {'post_form': post_form})
