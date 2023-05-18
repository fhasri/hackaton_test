
from rest_framework import generics, filters, viewsets
from .models import Category, Product, Order, Comment, Feedback, Rating, Like
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    CommentCreateSerializer,
    RatingSerializer,
    LikeSerializer,
    FeedbackSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAdminOrActivePermission, IsOwnerPermission


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'tags__title']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = []
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        rating = Rating.objects.filter(author=request.user, post=pk).first()
        serializer = RatingSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('You have already rated the post!')
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response('You have updated your rate on this post', status=204)
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'Disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author=user, is_like=True)
            like.save()
            message = 'Liked'
        return Response(message, status=201)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
