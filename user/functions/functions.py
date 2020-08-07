from django.contrib.auth.models import User
from status.models import CommentNotification, LikeNotification
from user.models import FriendRequests, Friend, UserProfile, AcceptedFriendRequests
from shopping.models import PartnerRequest, Partner
from message.models import MessageNotification, Message
from shopping.models import Item
from django.db.models import Q

def get_partner_requests(request):
    """
    Get the users partner notification requests.
    """
    try:
        partner_requests = PartnerRequest.objects.filter(to_user=request.user)
    except:
        partner_requests = []

    return partner_requests

def find_friends(request):
    """
    Find all users friends accounts.
    """
    try:
        friends = Friend.objects.get(current_user=request.user)
        all_friends = friends.users.all()
    except:
        all_friends = []

    return all_friends

def get_users_profile(request, pk):
    """
    Find user profile or create a friend list and user profile if new user.
    """
    requested_user = User.objects.get(pk=pk)

    try:
        user_profile = UserProfile.objects.get(user=requested_user)
    except:
        user_profile = UserProfile(
            user = requested_user,
            age = 18,
            profile_image = '',
            bio = "Click add on your profile image to add a personalised image and bio!",
            premium = False,
        )
        user_profile.save()

        friends_list = Friend(
            current_user = requested_user,
        )
        friends_list.save()

    return user_profile

def get_message_notifications(request):
    """
    Get the number of message notifications the user has.
    """
    try:
        message_notification_data = MessageNotification.objects.filter(user=request.user)
        message_notification = len(message_notification_data)
    except:
        message_notification = 0
    
    return message_notification

def get_all_shopping_items(request):
    """
    Get all the current users shopping items and their shopping partners items.
    """
    # Get the current users shopping partners
    try:
        shopping_partners = Partner.objects.get(current_user=request.user)
        shopping_partners_list = shopping_partners.partners.all()
    except:
        shopping_partners = []
        shopping_partners_list = []

    # Get all the current users items
    items = Item.objects.filter(user=request.user).order_by('item')

    all_items = [item for item in items]

    # Add all the users items and their shopping partners items into all_items
    for shopping_partner in shopping_partners_list:
        if not shopping_partner == request.user:
            partners_shopping_list = Item.objects.filter(user=shopping_partner)
            for item in partners_shopping_list:
                all_items.append(item)

    # Add the quantity of any duplicate items
    all_items_no_duplicates = []

    for loop_index, item in enumerate(all_items):
        if loop_index == 0:
            all_items_no_duplicates.append(item)
        else:
            item_is_not_a_copy = True
            for list_item in all_items_no_duplicates:
                if list_item.item == item.item:
                    item_is_not_a_copy = False
                    list_item.quantity += item.quantity

            if item_is_not_a_copy:
                all_items_no_duplicates.append(item)
                
    return all_items_no_duplicates

def get_all_notifications(request):
    # get like and comment notifications and order them by date
    notifications = []

    comment_notifications = CommentNotification.objects.filter(user=request.user)
    like_notifications = LikeNotification.objects.filter(user=request.user)
    accepted_friend_requests = AcceptedFriendRequests.objects.filter(from_user=request.user)

    for notification in comment_notifications:
        notifications.append(notification)

    for notification in like_notifications:
        notifications.append(notification)

    for notification in accepted_friend_requests:
        notifications.append(notification)
   
    notifications = sorted(notifications, key = lambda x: x.created_date, reverse=True)

    return notifications

def search_users(request):
    try:
        query = request.GET['q']
        queries = Q(username__startswith=query) | Q(first_name__startswith=query) | Q(last_name__startswith=query) | Q(username__startswith=query.capitalize()) | Q(first_name__startswith=query.capitalize()) | Q(last_name__startswith=query.capitalize())
        all_users = User.objects.filter(queries)
        searched_users = []
        for one_user in all_users:
            user_profile = UserProfile.objects.get(user=one_user)

            user_dict = {
                'first_name': one_user.first_name,
                'last_name': one_user.last_name,
                'username': one_user.username,
                'id': one_user.id,
                'user_profile': {
                    'profile_image': user_profile.profile_image,
                }
            }
            searched_users.append(user_dict)
    except:
        searched_users = []

    return searched_users