from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='example2', password='123456789')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix_1', about='Streaming_1', website='https://netflix.com')

    def test_stream_platform_create(self):
        data = {
            'name': 'Netflix_1',
            'about': 'Streaming_1',
            'website': 'https://netflix.com'
        }
        response = self.client.post(reverse('stream'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        response = self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_ind(self):
        response = self.client.get(reverse('stream-platform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchlistTesCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='example3', password='12345678910')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix_2', about='Streaming_2', website='https''://netflix2.com')
        self.watchclist = models.WatchList.objects.create(platform=self.stream, title='Example Movie', storyline='example movie', active=True)

    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Exaample Movie',
            'storyline': 'Example story',
            'active': True,
        }
        response = self.client.get(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-list', args=self.watchclist.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='example4', password='12345678911')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name='Netflix_1', about='Streaming_1', website='https://netflix.com')
        self.watchclist = models.WatchList.objects.create(platform=self.stream, title='Example Movie', description='example movie', active=True)
        self.watchclist2 = models.WatchList.objects.create(platform=self.stream, title='Example Movie', description='example movie', active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description='Great', watchlist=self.watchclist2, active=True)

    def test_review_create(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'Great',
            'watchlist': self.watchclist,
            'active': True,
        }
        response = self.client.post(reverse('review-create', args=self.watchclist.id), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('review-create', args=self.watchclist.id), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'Great',
            'watchlist': self.watchclist,
            'active': True,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=self.watchclist.id), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'review_user': self.user,
            'rating': 3,
            'description': 'Great-Updated',
            'watchlist': self.watchclist,
            'active': True,
        }
        response = self.client.put(reverse('review-create', args=self.review.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=self.watchclist.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-details', args=self.review.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('watch/reviews?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

