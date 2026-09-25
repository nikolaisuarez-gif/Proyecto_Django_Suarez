from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Create the 'editores' group (add/change movies, no delete) and an editor user."

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Movie)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["add_movie", "change_movie"],
        )

        group, _ = Group.objects.get_or_create(name="editores")
        group.permissions.set(permissions)

        editor, created = User.objects.get_or_create(
            username="editor",
            defaults={"email": "editor@tecsup.edu.pe"},
        )
        if created:
            editor.set_password("editor12345")
        editor.is_staff = True
        editor.save()
        editor.groups.add(group)

        self.stdout.write(
            self.style.SUCCESS(
                f"Group: {group.name} | Permissions: "
                f"{sorted(group.permissions.values_list('codename', flat=True))} "
                f"| User: {editor.username} | Can delete movie: "
                f"{editor.has_perm('movies.delete_movie')}"
            )
        )
