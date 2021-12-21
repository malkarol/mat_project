from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.core.mail import send_mail

#  Specify a translation string by using the function gettext().
#  It’s convention to import this as a shorter alias, _, to save typing.
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.

        """
        if not email:
            raise ValueError('User does not have: email address')
        if not first_name:
            raise ValueError('User does not have: first name')
        if not last_name:
            raise ValueError('User does not have: last name')
        if not username:
            raise ValueError('User does not have: username')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, username):


        user = self.create_user(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user



# Source for creating enum
# 1. Django official documentation
# 2. https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# 3. https://www.youtube.com/watch?v=eCeRC7E8Z7Y
class User(AbstractBaseUser):
    # email will be used for authentication
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    # those 7 fields are not required to override AbstractBaseUser
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active	= models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = [ 'username','first_name', 'last_name']

    objects = UserManager()
    # setting PricingPlanEnum value
    class PricingPlanEnum(models.IntegerChoices):
        FREE = 0, _('Free')
        PREMIUM = 1, _('Paid')

    pricing_plan = models.IntegerField(
      choices=PricingPlanEnum.choices,
      default=PricingPlanEnum.FREE
    )

    # setting MLBackgroundEnum value
    class MLBackgroundEnum(models.IntegerChoices):
        STUDENT = 0, _('Student')
        PROFESSOR = 1, _('Professor')
        PROFESSIONAL = 2, _('Professional')
        HOBBYST = 3, _('Hobbyst')

    ml_background = models.IntegerField(
      choices=MLBackgroundEnum.choices,
      default=MLBackgroundEnum.HOBBYST
    )

    # setting UserTypeEnum value
    class UserTypeEnum(models.IntegerChoices):
        NORMAL = 0, _('Normal')
        ADMIN= 1, _('Admin')

    user_type = models.IntegerField(
      choices=UserTypeEnum.choices,
      default=UserTypeEnum.NORMAL
    )

    # def __iter__(self):
    #         return iter(self.email)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_username(self):
        '''
        Returns the username for the user.
        '''
        return self.username

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this user.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)
