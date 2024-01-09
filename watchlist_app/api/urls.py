from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (WatchListListAV, WatchListDetailsAV, StreamPlatformAV, ReviewCreate,
                                     StreamPlatformVS, ReviewList, ReviewDetails, UserReview, WatchListListGV
                                     # StreamPlatformDetailsAV
                                     )

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='stream-platform')

urlpatterns = [
    path('list/', WatchListListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='movie-details'),
    path('list2/', WatchListListGV.as_view(), name='watch-list'),

    path('', include(router.urls)),

    path('stream1/', StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetails.as_view(), name='review-details'),
    path('reviews/', UserReview.as_view(), name='user-review-details'),

]
