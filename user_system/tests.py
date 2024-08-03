from django.test import TestCase, override_settings
from user_system.models import CustomUser


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LoginTest(TestCase):
    def test_login_menu(self):
        user = CustomUser(username='username', password='1234')
        user.save()
        self.client.login(username='username', password='1234')

        response_1 = self.client.get('/log_in/')

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 1)
