from django.contrib.auth import get_user_model

from django_sso_app.core.tests.factories import UserTestCase

from ...emails.models import EmailAddress
from ...groups.models import Group
from ...profiles.models import Profile

User = get_user_model()


class UserTestCase(UserTestCase):
    def test_add_profile_to_group_updates_rev(self):
        user = self._get_new_user()

        group = Group.objects.create(name='new_group')

        profile = user.sso_app_profile

        profile_rev = profile.sso_rev

        profile.groups.add(group)

        print('profile groups', profile.groups.all())

        profile.refresh_from_db()

        self.assertEqual(profile.sso_rev, profile_rev + 1)

    def test_user_creation_adds_default_groups(self):
        group_name = self._get_random_string()

        with self.settings(DJANGO_SSO_APP_DEFAULT_USER_GROUPS=[group_name]):
            user = self._get_new_user()

            user_groups = user.groups.values_list('name', flat=True)

            assert group_name in user_groups
