from django.conf.urls import url, include

from .views import ReviewListAPIView, ReviewDetailAPIView, ReviewCreateAPIView, BaseReviewStatusSetAPIView, BaseReviewDeleteAPIView, BaseReviewChildrenAPIView

app_name = 'reviews'

urlpatterns = [
    url(r'^$', ReviewListAPIView.as_view(), name='list'),
    url(r'^(?P<review_id>\d+)/status-set/$', BaseReviewStatusSetAPIView.as_view(), name='status-set'),
    url(r'^(?P<review_id>\d+)/delete/$', BaseReviewDeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<review_id>\d+)/$', ReviewDetailAPIView.as_view(), name='details'),
    url(r'^(?P<review_id>\d+)/children/$', BaseReviewChildrenAPIView.as_view(), name='children'),
    url(r'^model/(?P<model_id>\d+)/$', ReviewListAPIView.as_view(), name='models-list'),
    url(r'^(?P<review_id>\d+)/like/', include('aparnik.contrib.reviews.api.urls-like', namespace='like')),
    url(r'^(?P<review_id>\d+)/dislike/', include('aparnik.contrib.reviews.api.urls-dislike', namespace='dislike')),
    url(r'^create/$', ReviewCreateAPIView.as_view(), name='create'),
]