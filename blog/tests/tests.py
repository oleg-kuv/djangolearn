from django.test import TestCase
from blog.tests.helpers import HelperFabricObjectsMixin


class LoginTestCase(TestCase, HelperFabricObjectsMixin):
    # Вход с несуществующим логином
    def test_non_exists_login(self):
        login = self.client.login(
            username='somebody', password='dkekdkd')
        self.assertFalse(login)

    # Вход с существующим логином
    def test_login(self):
        user = self.create_reader_user()

        login = self.client.login(
            username=user.username,
            password=self.test_password
        )
        self.assertTrue(login)


class AccessTestCase(TestCase, HelperFabricObjectsMixin):
    def test_index(self):
        # Доступность главной
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorised_create_post(self):
        # Отсутствие доступа неавторизованного к добавлению поста
        response = self.client.get('/post/add_new/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/post/add_new/', response.url)

    def test_unauthorised_edit_post(self):
        # Отсутствие доступа неавторизованного к редактированию поста
        author = self.create_author_user()
        new_post = self.create_post(author)

        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            f"/accounts/login/?next=/post/{new_post.id}/edit/", response.url)

    def test_authorised_simple_user_create_post(self):
        # Отсутствие доступа простого авторизованного пользователя к созданию поста
        user = self.create_reader_user()

        self.client.login(username=user.username,
                          password=self.test_password)
        response = self.client.get('/post/add_new/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/post/add_new/', response.url)

    def test_authorised_simple_user_edit_post(self):
        # Отсутствие доступа простого авторизованного пользователя к редактированию поста
        user = self.create_reader_user()
        author = self.create_author_user()
        new_post = self.create_post(author)

        self.client.login(username=user.username,
                          password=self.test_password)
        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            f"/accounts/login/?next=/post/{new_post.id}/edit/", response.url)

    def test_authorised_author_create_post(self):
        # Наличие доступа автора к созданию поста
        author = self.create_author_user()

        self.client.login(username=author.username,
                          password=self.test_password)
        response = self.client.get('/post/add_new/')
        self.assertEqual(response.status_code, 200)

    def test_authorised_author_edit_post(self):
        # Наличие доступа редактированию к созданию поста
        author = self.create_author_user()
        new_post = self.create_post(author)

        self.client.login(username=author.username,
                          password=self.test_password)
        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_other_author_edit(self):
        # Попытка отредактировать чужой пост
        author = self.create_author_user()
        other_author = self.create_author_user('Ivan')
        new_post = self.create_post(author)

        self.client.login(username=other_author.username,
                          password=self.test_password)

        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 403)
