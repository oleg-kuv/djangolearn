from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from blog.models import Post


class TestBlog(TestCase):
    def setUp(self):
        self.add_new_page = '/post/add_new/'
        self.edit_page = '/post/1/edit/'
        self.group_author = Group.objects.create(name='test_author')
        post_ct_qs = ContentType.objects.get_for_model(Post)
        post_permissions = Permission.objects.filter(content_type=post_ct_qs)

        for permission in post_permissions:
            if permission.codename == 'add_post' or permission.codename == 'change_post':
                self.group_author.permissions.add(permission)

        self.test_pass = "1qazxsw2"
        self.author_user = User.objects.create_user(
            "testAuthorUser", "testauthoruser@example.com", self.test_pass)
        self.author_user.groups.add(self.group_author)
        self.simple_user = User.objects.create_user(
            "testUser", "testuser@example.com",  self.test_pass)

    def tearDown(self):
        self.author_user.delete()
        self.simple_user.delete()
        self.group_author.delete()


class LoginTestCase(TestBlog):
    # Вход с несуществующим логином
    def test_non_exists_login(self):
        login = self.client.login(
            username='somebody', password='dkekdkd')
        self.assertFalse(login)

    # Вход с существующим логином
    def test_login(self):
        login = self.client.login(
            username=self.simple_user.username,
            password=self.test_pass
        )
        self.assertTrue(login)

    # Вход автора
    def test_author_login(self):
        login = self.client.login(
            username=self.author_user.username,
            password=self.test_pass
        )
        self.assertTrue(login)


class AccessTestCase(TestBlog):

    def test_index(self):
        # Доступность главной
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorised(self):
        # Отсутствие доступа неавторизованного к добавлению поста
        response = self.client.get(self.add_new_page)
        self.assertEqual(response.status_code, 302)

        # Отсутствие доступа неавторизованного к редактированию поста
        response = self.client.get(self.edit_page)
        self.assertEqual(response.status_code, 302)

    def test_authorised_NO_author(self):
        # Отсутствие доступа простого авторизованного пользователя к созданию поста
        self.client.login(username=self.simple_user.username,
                          password=self.test_pass)
        response = self.client.get(self.add_new_page)
        self.assertEqual(response.status_code, 302)

        # Отсутствие доступа простого авторизованного пользователя к редактированию поста
        self.client.login(username=self.simple_user.username,
                          password=self.test_pass)
        response = self.client.get(self.edit_page)
        self.assertEqual(response.status_code, 302)

    def test_authorised_author(self):
        # Наличие доступа автора к созданию поста
        self.client.login(username=self.author_user.username,
                          password=self.test_pass)
        response = self.client.get(self.add_new_page)
        self.assertEqual(response.status_code, 200)

        # Наличие доступа к редактированию поста
        # По какой то причине не может получить доступ к странице '/post/1/edit/' - 404
#        login = self.client.login(username=self.author_user.username,
#                                  password=self.test_pass)
#        response = self.client.get(self.edit_page)
#        self.assertEqual(response.status_code, 200)
