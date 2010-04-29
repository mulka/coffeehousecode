#!/usr/bin/python251
# file: twitterhelper.py
# use example: $ python
# >>> import twitterhelper as th
# >>> th.unfollow_unfollowers()
# requires latest python-twitter dev version!!!
# $ svn checkout http://python-twitter.googlecode.com/svn/trunk/ python-twitter
import twitter
api = twitter.Api(username='quazie', password='adam123')
 
# next variables are collected once in runtime. This method is used, because of twitter
# API call limits. All specific functions should use these variables if they are populated.
 
# all the users, that are followed
followed = None
# all the users, that follows
followers = None
# all the people, that you follow, but who do no follow you
unfollowers = None
# all the people, that follow you, but you are not following them
unfollowed = None
 
# it is good idea to follow people, that follows you until you are a famous person,
# which has proper authority
def follow_unfollowed():
    r = 0
    for user in get_all_unfollowed():
        screen_name = user.screen_name
        r = r + 1
        try:
            api.CreateFriendship(screen_name)
            print "#%s %s" % (r, screen_name)
        except Exception:
            print "#%s could not create relationship with: %s" % (r, screen_name)

def follow_followers():
    r = 0
    for user in get_all_followers():
        screen_name = user.screen_name
        r = r + 1
        try:
            api.CreateFriendship(screen_name)
            print "#%s %s" % (r, screen_name)
        except Exception:
            print "#%s could not create relationship with: %s" % (r, screen_name)
 
# after some days of following, its good idea to purge your list and keep the
# number of followers and followed in a margin of 10%
# there is no 100 call limit on unfollow procedure as there is on follow! I did
# unfollow 900 people on one shot, maybe there is a limit of 1000...
def unfollow_unfollowers():
    r = 0
    for user in get_all_unfollowers():
        screen_name = user.screen_name
        r = r + 1
        try:
            api.DestroyFriendship(screen_name)
            print "#%s %s" % (r, screen_name)
        except Exception:
            print "#%s could not delete relationship with: %s" % (r, screen_name)
 
# you can get only 100 users / call so get_all_followed and get_all_followers
# must make a lot of API calls to get all users
# because of hourly API limit of 100 calls, it is possible, that this method does
# not work but max 5k followers and followed people
def get_all_followed(user = None):
    global followed
    if followed != None: return followed
    users, counter = [], 1
    while not len(users) % 100:
        if user:
            users += api.GetFriends(user, page=counter)
        else:
            users += api.GetFriends(page=counter)
        counter += 1
    followed = users
    return users
 
def get_all_followers(user = None):
    global followers
    if followers != None: return followers
    users, counter = [], 1
    while not len(users) % 100:
        if user:
            users += api.GetFollowers(user, page=counter)
        else:
            users += api.GetFollowers(page=counter)
        counter += 1
    followers = users
    return users
 
def get_all_unfollowers():
    global unfollowers
    if unfollowers != None: return unfollowers
    users = []
    followers = get_all_followers()
    followed = get_all_followed()
    for f in followed:
        if f not in followers:
            users.append(f)
    unfollowers = users
    return users
 
# it is good idea to follow all people, that follow you. its all about equality and interaction.
def get_all_unfollowed():
    global unfollowed
    if unfollowed != None: return unfollowed
    users = []
    followers = get_all_followers()
    followed = get_all_followed()
    for follower in followers:
        if follower not in followed:
            users.append(follower)
    unfollowed = users
    return users
 
# max 1000 / d
def send_direct_message_to_followers(msg):
    r = 0
    for user in get_all_followers():
        screen_name = user.screen_name
        r = r + 1
        try:
            api.PostDirectMessage(screen_name, msg)
            print "#%s %s" % (r, screen_name)
        except Exception:
            print "#%s could not send message to: %s" % (r, screen_name)