from django.shortcuts import render, redirect
from .models import Status, Comment, CommentNotification, LikeNotification
from user.models import Friend, UserProfile
from django.utils import timezone
from .functions.functions import *
from user.functions.functions import get_users_profile
from .forms import StatusForm

# Create your views here.
def news_feed(request):
    """
    Will show users all their friends posts
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    all_friends = get_all_friends(request)
    news_feed = get_news_feed(request)
    user_profile = get_users_profile(request, request.user.id)

    context = {
        'news_feed': news_feed,
        'user_profile': user_profile,
        'status_form': StatusForm,
    }

    return render(request, 'status/news_feed.html', context)

def update_status(request, operation, pk):
    """
    Add the users status to the database
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    # Add the status to the database, else remove the status from the database
    if operation == 'add':
        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

    elif operation == 'remove':
        status = Status.objects.get(pk=pk)
        status.delete()

    return redirect('profile')

def like_status(request, pk):
    """
    Add a like to the users status
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')


    if request.is_ajax():
        add_like_and_notification(request, pk)

    return redirect('news_feed')

def add_comment(request, pk, redirect_user):
    """
    Add a comment to the select status and send a notification to the user.
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    if request.is_ajax():
        create_comment_and_status_notification(request, pk)
   
    if redirect_user == 'profile':
        return redirect('profile')
    if redirect_user == 'news_feed':
        return redirect('news_feed')

def view_status(request, pk):
    """
    Take the user to a page that shows one status from their notificats or from the news feed.
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    status = Status.objects.get(pk=pk)

    context = {
        'news': status,
    }

    return render(request, 'status/view_status.html', context)