from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher


class CustomPBKDF2SHA1PasswordHasher(PBKDF2SHA1PasswordHasher):
    """
    A Subclass of PBKDF2SHA1PasswordHasher that uses 100 times more iterations
    This will slow down possible attackers as it makes the the hash more difficult.
    Because the computer power increases, the number of  iterations should also increase

    A subclass of PBKDF2PasswordHasher that uses 10 times more iterations.
    """
    iterations = PBKDF2SHA1PasswordHasher.iterations * 10
