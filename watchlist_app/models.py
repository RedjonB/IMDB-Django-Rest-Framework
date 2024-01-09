from django.db.models import (Model, CharField, BooleanField, URLField, ForeignKey, PositiveIntegerField, DateTimeField,
                              FloatField, IntegerField)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class StreamPlatform(Model):
    class Meta:
        db_table = 'stream_platform'

    name = CharField(max_length=30)
    about = CharField(max_length=150)
    website = URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(Model):
    class Meta:
        db_table = 'watch_list'

    title = CharField(max_length=50)
    description = CharField(max_length=50)
    active = BooleanField(default=True)
    created = DateTimeField(auto_now=True)
    avg_rating = FloatField(default=0)
    number_rating = IntegerField(default=0)
    platform = ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')

    def average(self):
        return self.number_rating/2

    def __str__(self):
        return self.title


class Review(Model):
    class Meta:
        db_table = 'review'

    review_user = ForeignKey(User, on_delete=models.CASCADE)
    rating = PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = CharField(max_length=50)
    active = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)
    update = DateTimeField(auto_now=True)
    watchlist = ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews', null=True)

    def __str__(self):
        return str(self.rating) + ' | ' + self.watchlist.title + ' | ' + str(self.review_user)
