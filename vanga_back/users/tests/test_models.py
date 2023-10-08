from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='TestUser'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        user = UserModelTest.user

        self.assertEqual(str(user),'TestUser')

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        user = UserModelTest.user

        field_verbose = {'username': 'Логин'}

        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).verbose_name, expected_value)
