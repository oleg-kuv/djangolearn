from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post, Tag


class HelperFabricObjectsMixin:
    test_password = 'a;sldkfj123'

    def create_author_group(self) -> Group:

        group_author, created = Group.objects.get_or_create(name='test_author')

        post_ct_qs = ContentType.objects.get_for_model(Post)
        post_permissions = Permission.objects.filter(content_type=post_ct_qs)

        for permission in post_permissions:
            if permission.codename == 'add_post' or permission.codename == 'change_post':
                group_author.permissions.add(permission)
        return group_author

    def create_author_user(self, username="testAuthorUser") -> User:
        group_author = self.create_author_group()
        user = User.objects.create_user(
            username, f"{username}@example.com", self.test_password)
        user.groups.add(group_author)
        return user

    def create_reader_user(self) -> User:
        user = User.objects.create_user(
            "testUser", "testuser@example.com", self.test_password)
        return user

    def create_post(self, author_user_object: User, title="Test post", active: bool = True) -> Post:
        post = Post.objects.create(
            title=title,
            text='text',
            active=active,
            author=author_user_object,
        )

        return post

    def create_tag(self, author_user_object: User, title="Test tag", active: bool = True) -> Tag:
        tag = Tag.objects.create(
            title=title,
            description='Test tag',
            active=active,
            author=author_user_object
        )

        return tag

    def assign_tag_to_post(self, post: Post, tag: Tag) -> bool:
        post.tags.add(tag)
