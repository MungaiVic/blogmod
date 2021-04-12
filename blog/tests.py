from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import *
from .forms import NewUserForm, UpgradeToBloggerForm


class UserAccountTests(TestCase):
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



    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'username', 'first_name','last_name', 'password', is_superuser=True, is_staff=True, is_active=True)
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertEqual(super_user.first_name, 'first_name')
        self.assertEqual(super_user.last_name, 'last_name')
        self.assertTrue(super_user.is_superuser),
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'username')

        # is_superuser test
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@superuser.com', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_superuser=False # is_superuser should be true
            )
        # is_staff test
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@superuser.com', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_staff=False # is_staff should be true
            )
        #is_active test
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@superuser.com', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_active=False # is_active should be true
            )
        # Email ValueError test
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='username1', first_name='fist_name', last_name='last_name', password='password', is_superuser=True # Email field should be filled.
            )


class PostTests(TestCase):
    def test_new_post(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com','username','first_name', 'last_name', 'password'
        )
        blogpost = Post
        new_post = blogpost.objects.create(
            title='title', slug='slug', summary='summary', author=user,body='body',
        )
        self.assertEqual(new_post.title, 'title')
        self.assertEqual(new_post.slug,'slug')
        self.assertEqual(new_post.summary,'summary')
        self.assertEqual(new_post.author,user)
        self.assertEqual(new_post.body,'body')
        self.assertEqual(str(new_post), 'title')



class CommentTests(TestCase):
    def test_new_comment(self):
        db = get_user_model()
        commentor = db.objects.create_user(
            'testuser@user.com','username','first_name', 'last_name', 'password'
        )
        comment = Comment
        blogpost = Post
        new_post = blogpost.objects.create(
            title='title', slug='slug', summary='summary', author=commentor,body='body',
        )
        new_comment = comment.objects.create(
            post = new_post, user=commentor, body='body'
        )
        self.assertEqual(new_comment.post, new_post)
        self.assertEqual(new_comment.user, commentor)
        self.assertEqual(new_comment.body, 'body')
        self.assertEqual(str(new_comment), 'Comment by username on title')

# Testing CBVs: https://docs.djangoproject.com/en/3.1/topics/testing/advanced/


class TagTest(TestCase):
    def test_new_tag(self):
        db=Tag
        new_tag = db.objects.create(name='tag')
        self.assertEqual(new_tag.name, 'tag')
        self.assertEqual(str(new_tag),'tag')



class FormTests(TestCase):
    upgrade_form = UpgradeToBloggerForm

    def new_user_form_test(self):
        newuser_form = NewUserForm
        form = newuser_form(
            first_name='first_name',last_name='last_name',user_name='username',email='testuser@user.com',
            password1='password', password2='password'
            )
        self.assertEquals(newuser_form.password1,newuser_form.password2)
        self.assertTrue(newuser_form.save())



class ViewsTests(TestCase):
    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')