# from django.urls import path
# from .views import CategoryListView, OrderViewSet, RatingViewSet, LikeViewSet,CommentViewSet, FeedbackViewSet


# urlpatterns = [
#     path('')
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView,
    ProductViewSet,
    OrderViewSet,
    CommentViewSet,
    FeedbackViewSet,
    RatingViewSet,
    LikeViewSet,
)


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('comments', CommentViewSet)
router.register('feedbacks', FeedbackViewSet)
router.register('ratings', RatingViewSet)
router.register('likes', LikeViewSet)

urlpatterns = [

    path('categories/', CategoryListView.as_view()),

    path('', include(router.urls)),

]
