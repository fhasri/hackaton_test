
from django.contrib import admin
from .models import Category, Product, Order, Comment, Feedback, Rating, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ['category']
    search_fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'created_at')
    list_filter = ['buyer']
    search_fields = ['buyer__username', 'product__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'body', 'created_at')
    list_filter = ['author']
    search_fields = ['author__username', 'post__title', 'body']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'created_at')
    search_fields = ['author', 'email']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'rating')
    list_filter = ['author']
    search_fields = ['author__username', 'post__title']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_like')
    list_filter = ['author']
    search_fields = ['author__username', 'post__title']
