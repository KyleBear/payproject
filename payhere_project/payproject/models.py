# from django.db import models

# Create your models here.
# models.py

# Create your models here
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class Owner(models.Model):
#     phone_number = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)

# class Product(models.Model):
#     category = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     cost_price = models.DecimalField(max_digits=10, decimal_places=2)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     barcode = models.CharField(max_length=255, blank=True, null=True)
#     expiration_date = models.DateField(blank=True, null=True)
#     size = models.CharField(max_length=10, choices=(('small', 'Small'), ('large', 'Large')))
#     owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
# Create model here

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password

class OwnerManager(BaseUserManager):
    # def create_user(self, phone_number, password=None):
    #     if not phone_number:
    #         raise ValueError('Users must have a phone number')

    #     user = self.model(
    #         phone_number=phone_number,
    #     )

    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, phone_number, password):
    #     user = self.create_user(
    #         phone_number=phone_number,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user
    def authenticate(self, phone_number=None, password=None):
        if not phone_number or not password:
            return None
        
        owner = self.get_queryset().filter(phone_number=phone_number).first()
        if owner and check_password(password, owner.password):
            return owner
        return None

class Owner(AbstractBaseUser):
    phone_number = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    objects = OwnerManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Product(models.Model):
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    size = models.CharField(max_length=10, choices=(('small', 'Small'), ('large', 'Large')))
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
