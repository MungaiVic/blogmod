from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'username', 'first_name','last_name', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertEqual(super_user.first_name, 'first_name')
        self.assertEqual(super_user.last_name, 'last_name')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertEqual(str(super_user), 'username')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@superuser.com', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_superuser=False # is_superuser should be true
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@superuser.com', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_staff=False # is_staff should be true
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_superuser=True # Email field should be filled.
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com','username','first_name', 'last_name', 'password'
        )
        self.assertEqual(user.email,'testuser@user.com')
        self.assertEqual(user.first_name, 'first_name')
        self.assertEqual(user.last_name, 'last_name')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='',user_name='a', first_name='first_name', last_name='last_name', password='password'
            )