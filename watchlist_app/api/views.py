# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
import rest_framework.response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
# from rest_framework import mixins
# from rest_framework.decorators import api_view
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
# UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
# from rest_framework import filters

from watchlist_app.api.pagination import WatchlistCPagination
# WatchlistPagination, WatchlistLOPagination,
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer,
                                           StreamPlatformSerializer, ReviewSerializer)
from user_app.throttling import ReviewListThrottle, ReviewCreateThrottle


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username) # ?? pse __username

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        if Review.objects.filter(watchlist=movie, review_user=review_user).exists():
            raise ValidationError('You have already sent a review for this film')

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2

        movie.number_rating = movie.number_rating + 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, ReviewListThrottle]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['review_user__username', 'active']
    # ordering_fields = []

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-details'


# class ReviewDetails(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(self, request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListListGV(generics.ListAPIView):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()
    pagination_class = WatchlistCPagination

    # permission_classes = [IsAuthenticated]
    # throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['active']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['platform__name', 'title']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']


class WatchListListAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    @staticmethod
    def get(request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return rest_framework.response.Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(serializer.data)
        else:
            return rest_framework.response.Response(serializer.errors)


class WatchListDetailsAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    @staticmethod
    def get(request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return rest_framework.response.Response({'Error': '!!!!!!!!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WatchListSerializer(movie)
        return rest_framework.response.Response(serializer.data)

    @staticmethod
    def put(request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(serializer.data)
        else:
            return rest_framework.response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return rest_framework.response.Response(status=status.HTTP_204_NO_CONTENT)

# StreamPlatform Class Based Views /////////////////////////////////////////////////////////////////////////////


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    @staticmethod
    def get(request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return rest_framework.response.Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(serializer.data)
        else:
            return rest_framework.response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailsAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    @staticmethod
    def get(request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return rest_framework.response.Response({'Error': 'Does not EXIST'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return rest_framework.response.Response(serializer.data)

    @staticmethod
    def put(request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rest_framework.response.Response(serializer.data)
        else:
            return rest_framework.response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return rest_framework.response.Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movies)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#     elif request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
