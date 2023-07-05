from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from blog.models import Post

test_pass = 'a;sldkfj123'


def create_author_group_helper():
    group_author = Group.objects.create(name='test_author')
    post_ct_qs = ContentType.objects.get_for_model(Post)
    post_permissions = Permission.objects.filter(content_type=post_ct_qs)

    for permission in post_permissions:
        if permission.codename == 'add_post' or permission.codename == 'change_post':
            group_author.permissions.add(permission)
    return group_author


def create_author_user_helper(username="testAuthorUser"):
    group_author = create_author_group_helper()
    user = User.objects.create_user(
        username, f"{username}@example.com", test_pass)
    user.groups.add(group_author)
    return user


def create_reader_user_helper():
    user = User.objects.create_user(
        "testUser", "testuser@example.com", test_pass)
    return user


def remove_test_user_helper(user: User):
    user.delete()


def create_post_helper(author_user_object: User, title="Test post", active=True):
    post = Post()
    post.title = title
    post.text = 'text'
    post.active = active
    post.author = author_user_object
    post.save()

    return post


def remove_new_post_helper(post: Post):
    post.delete()


class LoginTestCase(TestCase):
    # Вход с несуществующим логином
    def test_non_exists_login(self):
        login = self.client.login(
            username='somebody', password='dkekdkd')
        self.assertFalse(login)

    # Вход с существующим логином
    def test_login(self):
        user = create_reader_user_helper()

        login = self.client.login(
            username=user.username,
            password=test_pass
        )
        self.assertTrue(login)


class AccessTestCase(TestCase):
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
        author = create_author_user_helper()
        new_post = create_post_helper(author)

        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            f"/accounts/login/?next=/post/{new_post.id}/edit/", response.url)

    def test_authorised_simple_user_create_post(self):
        # Отсутствие доступа простого авторизованного пользователя к созданию поста
        user = create_reader_user_helper()

        self.client.login(username=user.username,
                          password=test_pass)
        response = self.client.get('/post/add_new/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/accounts/login/?next=/post/add_new/', response.url)

    def test_authorised_simple_user_edit_post(self):
        # Отсутствие доступа простого авторизованного пользователя к редактированию поста
        user = create_reader_user_helper()
        author = create_author_user_helper()
        new_post = create_post_helper(author)

        self.client.login(username=user.username,
                          password=test_pass)
        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            f"/accounts/login/?next=/post/{new_post.id}/edit/", response.url)

    def test_authorised_author_create_post(self):
        # Наличие доступа автора к созданию поста
        author = create_author_user_helper()

        self.client.login(username=author.username,
                          password=test_pass)
        response = self.client.get('/post/add_new/')
        self.assertEqual(response.status_code, 200)

    def test_authorised_author_edit_post(self):
        # Наличие доступа редактированию к созданию поста
        author = create_author_user_helper()
        new_post = create_post_helper(author)

        self.client.login(username=author.username,
                          password=test_pass)
        response = self.client.get(f"/post/{new_post.id}/edit/")
        self.assertEqual(response.status_code, 200)
