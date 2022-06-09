from typing import Any

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError, CommandParser

User = get_user_model()


class Command(BaseCommand):
    """
    Sets the user access to the platform

    python src/manage.py changeuseraccess --email tiago.silva@colibridigital.io --level admin
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--email",
            "-e",
            dest="email",
            help="Email to update",
            type=str,
            required=True,
        )
        parser.add_argument(
            "--level",
            "-l",
            dest="level",
            help="Level of access",
            type=str,
            required=True,
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handles with the update of a user via email.
        """
        email = options["email"]
        level = options["level"]

        access_level = ["admin", "user", "manager", "viewer", "other"]

        email = email.strip()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise CommandError(f"User with email {email} does not exist.")

        if level not in access_level:
            raise CommandError(
                f"Access level {level} is not recognized. The available levels are {', '.join(access_level)}"
            )

        user.hub_user.profile_type = level
        user.hub_user.save()

        self.stdout.write("User access updated!")