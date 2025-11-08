from unittest import mock

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post(
            "/accounts/send_login_email/", data={"email": "test@example.com"}
        )
        self.assertRedirects(response, "/")

    def test_adds_success_message(self):
        response = self.client.post(
            "/accounts/send_login_email/",
            data={"email": "test@example.com"},
            follow=True,
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.",
        )
        self.assertEqual(message.tags, "success")

    @mock.patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email/", data={"email": "test@example.com"}
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["test@example.com"])

    def test_creates_token_associated_with_email(self):
        self.client.post(
            "/accounts/send_login_email/", data={"email": "test@example.com"}
        )
        token = Token.objects.get()
        self.assertEqual(token.email, "test@example.com")

    @mock.patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email/", data={"email": "test@example.com"}
        )
        token = Token.objects.get()
        expected_url = f"http://testserver/accounts/login/?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.get("/accounts/login/?token=abcd123")
        self.assertRedirects(response, "/")
