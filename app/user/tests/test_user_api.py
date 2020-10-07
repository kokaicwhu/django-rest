from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test pulic users API"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': 'test0000',
            'name': 'tester'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_create_user_exists(self):
        """Test creating an user that already exists should be failed"""
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': 'test0000',
            'name': 'tester'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Password must be more than 5 characters"""
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': '0000',
            'name': 'tester'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)  # this user shouldn't be registered

    def test_create_token_for_user(self):
        """Test a token can be created"""
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': '0000'
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test the token is not created if credentials are wrong"""
        create_user(**{
            'email': 'tester@qa.pthree.com',
            'password': '0000',
            'name': 'tester'}
        )
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': '1111'
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_toekn_no_user(self):
        """Test the token is not created if user doesn't exist"""
        payload = {
            'email': 'tester@qa.pthree.com',
            'password': '0000'
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test the email and password are required to create token"""
        res = self.client.post(CREATE_TOKEN_URL, {'email': 'tester@qa.pthree.com'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """Test user auth is required"""
        res = self.client.get(PROFILE_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that need user authentication"""

    def setUp(self):
        self.user = create_user(
            email='test1@qa.pthree.com',
            password='test0000',
            name='Tester 1'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    
    def test_post_profile_not_allowed(self):
        """POST method is not allowed for profile API"""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """Test updating user profile by PATCH method"""
        payload = {'name': 'New Tester', 'password': 'test1111'}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
