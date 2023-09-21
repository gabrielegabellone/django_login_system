from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIClient


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.username, self.password, self.email = 'user', 'pass', 'testuser@email.com'
        User.objects.create_user(username=self.username, password=self.password, email=self.email)

        self.client = APIClient()
        self.user = User.objects.get(username=self.username)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=None)
    def test_login(self):
        """Tests the correct functioning of the endpoint if the user is correctly authenticated."""
        response = self.client.post('/auth/login/', data={'username': self.username, 'password': self.password})

        actual_data = response.json()
        self.assertIn('key', actual_data, 'Expected a key in the response.')
        self.assertIsNotNone(actual_data['key'], 'Expected that the key is not None.')

        self.assertEqual(200, response.status_code)

    def test_login_email_not_verified(self):
        """Tests the correct functioning of the endpoint if the user's email is not verified."""
        response = self.client.post('/auth/login/', data={'username': self.username, 'password': self.password})

        actual_data = response.content
        expected_data = b'{"non_field_errors":["E-mail is not verified."]}'
        self.assertIn(expected_data, actual_data)

        self.assertEqual(400, response.status_code)

    def test_logout(self):
        """Tests the correct functioning of the logout endpoint."""
        response = self.client.post('/auth/logout/')

        actual_data = response.content
        current_user = response.wsgi_request.user

        self.assertIn(b'{"detail":"Successfully logged out."}', actual_data)
        self.assertIsInstance(current_user, AnonymousUser, 'Expected that the current user is an AnonymousUser.')
        self.assertEqual(200, response.status_code)

    def test_user(self):
        """Tests the correct functioning of the user detail endpoint."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/auth/user/')

        actual_data = response.content
        expected_data = b'{"pk":1,"username":"user","email":"testuser@email.com","first_name":"","last_name":""}'
        self.assertIn(expected_data, actual_data)
        self.assertEqual(200, response.status_code)

    def test_password_change_passwords_ok(self):
        """Tests the correct functioning of the endpoint to change the password."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/auth/password/change/', data={'new_password1': 'new_password', 'new_password2': 'new_password'})

        actual_data = response.json()
        expected_data = {'detail': 'New password has been saved.'}

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(200, response.status_code)

    def test_password_change_passwords_not_match(self):
        """Tests the correct functioning of the endpoint to change the password, if the two passwords entered by the
        user do not match."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/auth/password/change/', data={'new_password1': 'new_password', 'new_password2': 'different_password'})

        actual_data = response.json()
        expected_data = {'new_password2': ['The two password fields didn’t match.']}

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(400, response.status_code)

    def test_password_reset(self):
        """Tests the correct functioning of the password reset endpoint."""
        response = self.client.post('/auth/password/reset/', data={'email': self.email})

        actual_data = response.content
        expected_data = b'{"detail":"Password reset e-mail has been sent."}'

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(200, response.status_code)

    def test_password_reset_confirm(self):
        """Tests the correct functioning of the password reset confirm endpoint."""
        # send an email with a password reset link
        self.client.post('/auth/password/reset/', data={'email': self.email})

        # get the user_id and token from the url in the received email
        email_received = str(mail.outbox[0].message())
        url_reset_password = email_received[email_received.find("http"):].split("\n")[0]
        data = url_reset_password.replace("http://testserver/", "").split("/")
        user_id, token = data[1], data[2]
        response = self.client.post('/auth/password/reset/confirm/',
                                    data={'new_password1': 'newpassword1234', 'new_password2': 'newpassword1234', 'uid': user_id, 'token': token})

        actual_data = response.content
        expected_data = b'{"detail":"Password has been reset with the new password."}'

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(200, response.status_code)

    def test_registration(self):
        """Tests the correct functioning of the registration endpoint."""
        response = self.client.post('/auth/registration/', data={'username': 'newuser', 'email': 'testemail@email.com', 'password1': 'testpassword', 'password2': 'testpassword'})
        actual_data = response.content
        expected_data = b'{"detail":"Verification e-mail sent."}'

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(201, response.status_code)

    def test_account_confirm_email(self):
        """Tests the correct functioning of the account-confirm-email endpoint."""
        # sending an email containing a link with a key to confirm the account
        self.client.post('/auth/registration/', data={'username': 'newuser', 'email': 'testemail@email.com', 'password1': 'testpassword', 'password2': 'testpassword'})

        # get the key to confirm the account through the link received in the email
        email_received = str(mail.outbox[0].message())
        link_received = email_received[email_received.find('http'):].split('\n')[0]
        endpoint_to_confirm_account = link_received.replace('http://testserver', '')
        data = endpoint_to_confirm_account.split('/')
        key = data[3]
        response = self.client.post(endpoint_to_confirm_account, data={'key': key})

        actual_data = response.content
        expected_data = b'{"detail":"ok"}'

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(200, response.status_code)

    def test_hello_world(self):
        """Tests the correct functioning of the hello endpoint."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/auth/hello/')

        actual_data = response.content
        expected_data = b'{"message":"Hello user!"}'

        self.assertEqual(expected_data, actual_data)
        self.assertEqual(200, response.status_code)
