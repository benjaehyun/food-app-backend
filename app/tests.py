from django.test import TestCase
from django.urls import reverse
from .models import Food
from django.contrib.auth.models import User 


# Create your tests here.

# class FoodModelTest(TestCase): 
#     def setUp(self): 
#         Food.objects.create(title='risotto', description='italian', completed=False)
#         Food.objects.create(title='pho', description='vietnamese', completed=True)

#     def test_food_content(self):
#         risotto = Food.objects.get(title='risotto')
#         pho = Food.objects.get(title='pho')
#         self.assertEqual(risotto.description, 'italian')
#         self.assertEqual(pho.completed, True)

class AuthTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing login
        cls.test_user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_login_view_sets_httponly_cookies(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword123'}, secure=True)
        self.assertTrue(response.cookies.get('access_token').value)
        self.assertTrue(response.cookies['access_token']['httponly'])
        self.assertTrue(response.cookies.get('refresh_token').value)
        self.assertTrue(response.cookies['refresh_token']['httponly'])


    def test_logout_view_clears_cookies(self):
        # Log in to set the cookies
        self.client.login(username='testuser', password='testpassword123')
        # Then, log out
        response = self.client.post(reverse('logout'), secure=True)
        self.assertFalse(response.cookies.get('access_token').value)
        self.assertFalse(response.cookies.get('refresh_token').value)

    # def test_refresh_token_view(self):
    #     # Log in to set the refresh token cookie
    #     self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword123'}, secure=True)
    #     # Attempt to refresh the token using the refresh token endpoint
    #     response = self.client.post(reverse('token_refresh'), secure=True)
    #     self.assertTrue(response.cookies.get('access_token').value)
    #     self.assertTrue(response.cookies['access_token']['httponly'])
        
    def test_refresh_token_view(self):
        # Log in to set the refresh token cookie
        login_response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword123'}, secure=True)
        # Verify that the refresh token cookie is set
        self.assertIn('refresh_token', login_response.cookies)
        self.assertTrue(login_response.cookies['refresh_token'].value)

        # Attempt to refresh the token using the refresh token endpoint
        # Note: Since the test client automatically uses cookies stored from previous responses,
        # the refresh token cookie will be included in this request.
        refresh_response = self.client.post(reverse('token_refresh'), secure=True)
        
        # Verify that a new access token is provided in the response cookies
        self.assertIn('access_token', refresh_response.cookies)
        self.assertTrue(refresh_response.cookies['access_token']['httponly'])

        # Check if the access token cookie is correctly set
        self.assertIsNotNone(refresh_response.cookies.get('access_token').value)