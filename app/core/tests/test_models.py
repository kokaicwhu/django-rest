from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Ingredient


def sample_user(email='sample@qa.pthree.com', password="sample0000"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an emial is successful"""
        email = 'test@cw.pthree.com'
        password = "test0000"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test2@CW.PTHREE.COM'
        user = get_user_model().objects.create_user(email, 'test0000')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test0000')
    
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@cw.pthree.com', 'admin0000'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_tag_user(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(), name='Sample Tag'
        )

        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        """Test the string representation"""
        ingredient = Ingredient.objects.create(
            user=sample_user(), name='Cucuber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
