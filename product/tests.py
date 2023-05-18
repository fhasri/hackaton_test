# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Category, Product, Order, Comment, Feedback, Rating, Like


# class CategoryModelTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(title='Test Category')

#     def test_title_label(self):
#         field_label = self.category._meta.get_field('title').verbose_name
#         self.assertEqual(field_label, 'title')

#     def test_title_max_length(self):
#         max_length = self.category._meta.get_field('title').max_length
#         self.assertEqual(max_length, 100)


# class ProductModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)

#     def test_name_label(self):
#         field_label = self.product._meta.get_field('name').verbose_name
#         self.assertEqual(field_label, 'name')

#     def test_price_max_digits(self):
#         max_digits = self.product._meta.get_field('price').max_digits
#         self.assertEqual(max_digits, 10)

#     def test_user_username(self):
#         username = self.product.user.username
#         self.assertEqual(username, 'testuser')


# class OrderModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)
#         self.order = Order.objects.create(product=self.product, user=self.user, quantity=2)

#     def test_product_name(self):
#         product_name = self.order.product.name
#         self.assertEqual(product_name, 'Test Product')

#     def test_user_username(self):
#         username = self.order.user.username
#         self.assertEqual(username, 'testuser')

#     def test_quantity(self):
#         quantity = self.order.quantity
#         self.assertEqual(quantity, 2)


# class CommentModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)
#         self.comment = Comment.objects.create(product=self.product, user=self.user, text='Test Comment')

#     def test_product_name(self):
#         product_name = self.comment.product.name
#         self.assertEqual(product_name, 'Test Product')

#     def test_user_username(self):
#         username = self.comment.user.username
#         self.assertEqual(username, 'testuser')

#     def test_text(self):
#         text = self.comment.text
#         self.assertEqual(text, 'Test Comment')


# class FeedbackModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)
#         self.feedback = Feedback.objects.create(product=self.product, user=self.user, rating=4, comment='Test Feedback')

#     def test_product_name(self):
#         product_name = self.feedback.product.name
#         self.assertEqual(product_name, 'Test Product')

#     def test_user_username(self):
#         username = self.feedback.user.username
#         self.assertEqual(username, 'testuser')

#     def test_rating(self):
#         rating = self.feedback.rating
#         self.assertEqual(rating, 4)

#     def test_comment(self):
#         comment = self.feedback.comment
#         self.assertEqual(comment, 'Test Feedback')


# class RatingModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)
#         self.rating = Rating.objects.create(product=self.product, user=self.user, value=8)

#     def test_product_name(self):
#         product_name = self.rating.product.name
#         self.assertEqual(product_name, 'Test Product')

#     def test_user_username(self):
#         username = self.rating.user.username
#         self.assertEqual(username, 'testuser')

#     def test_value(self):
#         value = self.rating.value
#         self.assertEqual(value, 8)


# class LikeModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
#         self.category = Category.objects.create(title='Test Category')
#         self.product = Product.objects.create(name='Test Product', category=self.category, price=10.99, user=self.user)
#         self.like = Like.objects.create(product=self.product, user=self.user)

#     def test_product_has_likes(self):
#         product = self.like.product
#         self.assertEqual(product.likes.count(), 1)

#     def test_user_likes(self):
#         user = self.like.user
#         self.assertEqual(user.like_set.count(), 1)
#==========================================================

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category, Product, Order, Comment, Feedback, Rating, Like


class CategoryModelTest(TestCase):
    def test_title_max_length(self):
        category = Category.objects.create(title='A' * 100)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_product_name(self):
        comment = Comment.objects.create(user=self.user, product_name='Test Product')
        self.assertEqual(comment.product_name, 'Test Product')

    def test_text(self):
        comment = Comment.objects.create(user=self.user, text='Test comment')
        self.assertEqual(comment.text, 'Test comment')

    def test_user_username(self):
        comment = Comment.objects.create(user=self.user, user_username='testuser')
        self.assertEqual(comment.user_username, 'testuser')


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_comment(self):
        feedback = Feedback.objects.create(user=self.user, comment='Test feedback')
        self.assertEqual(feedback.comment, 'Test feedback')

    def test_product_name(self):
        feedback = Feedback.objects.create(user=self.user, product_name='Test Product')
        self.assertEqual(feedback.product_name, 'Test Product')

    def test_rating(self):
        feedback = Feedback.objects.create(user=self.user, rating=5)
        self.assertEqual(feedback.rating, 5)

    def test_user_username(self):
        feedback = Feedback.objects.create(user=self.user, user_username='testuser')
        self.assertEqual(feedback.user_username, 'testuser')


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_product_has_likes(self):
        product = Product.objects.create(name='Test Product')
        like = Like.objects.create(user=self.user, product=product)
        self.assertIn(like, product.likes.all())

    def test_user_likes(self):
        product = Product.objects.create(name='Test Product')
        like = Like.objects.create(user=self.user, product=product)
        self.assertIn(like, self.user.likes.all())


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_product_name(self):
        order = Order.objects.create(user=self.user, product_name='Test Product')
        self.assertEqual(order.product_name, 'Test Product')

    def test_quantity(self):
        order = Order.objects.create(user=self.user, quantity=5)
        self.assertEqual(order.quantity, 5)

    def test_user_username(self):
        order = Order.objects.create(user=self.user, user_username='testuser')
        self.assertEqual(order.user_username, 'testuser')


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_name_label(self):
        product = Product.objects.create(name='Test Product')
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_max_digits(self):
        product = Product.objects.create(name='Test Product', price=99.99)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 5)

    def test_user_username(self):
        product = Product.objects.create(name='Test Product', user=self.user)
        self.assertEqual(product.user_username, 'testuser')


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )

    def test_product_name(self):
        rating = Rating.objects.create(user=self.user, product_name='Test Product')
        self.assertEqual(rating.product_name, 'Test Product')

    def test_user_username(self):
        rating = Rating.objects.create(user=self.user, user_username='testuser')
        self.assertEqual(rating.user_username, 'testuser')

    def test_value(self):
        rating = Rating.objects.create(user=self.user, value=5)
        self.assertEqual(rating.value, 5)
