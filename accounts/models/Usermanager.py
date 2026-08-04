from django.contrib.auth.models import (
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    """Class to manage the creation of user objects"""
    
    def make_random_password(self, length=16):
        """Generates a random password of given length using allowed characters"""
        # define the allowed characters including all leters, digits, and some special characters
        allowed_chars = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789'
            '!@#$%^&*()-_=+[]{}|;:,.<>?'
        )
        # use random.choice to select characters from the allowed set and join them to form a password of the specified length
        import random
        return ''.join(random.choice(allowed_chars) for _ in range(length))
        
    def get_queryset(self):
        """Returns the queryset of users"""
        return super().get_queryset().filter(is_active=True)

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a user object
        Arguments:
        email: the string to use as email
        password: the string to use as password

        Optionals:
        Any additional fields to set on the User model

        Return:
            A user object
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates an admin user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Return:
            A user object
        """
        user = self.create_user(email, password=password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user