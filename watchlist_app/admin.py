from django.contrib import admin
from watchlist_app.models import WatchList, StreamPlatform, Review

mylist = [WatchList, StreamPlatform, Review]

for item in mylist:
    admin.site.register(item)
