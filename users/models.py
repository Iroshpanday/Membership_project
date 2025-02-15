from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self,phone_number,password=None,**extra_fields):
        if not phone_number:
            raise ValueError('The phone Number fiels must be set')
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password) # yo set_password fxn lah password hashe(encrypt) garxa
        user.save(using=self._db) # using= self._db vanya chai yahi db mah hal vanako incase if we  are using multiple db
        return user
    
    def create_superuser(self,phone_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(phone_number,password,**extra_fields)


class CustomUser(AbstractBaseUser , PermissionsMixin):
    MEMBERSHIP_CHOICES =[
        ('SILVER','silver'),
        ('GOLD','gold'),
        ('DIAMOND','diamond'),
    ]
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=30, blank=True,unique=True)
    membership_type = models.CharField(max_length=10,choices=MEMBERSHIP_CHOICES,default='SILVER')
    membership_start_date = models.DateTimeField(null=True,blank=True)
    membership_expiry_date = models.DateTimeField(null=True,blank=True)

    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default= False)

    objects = CustomUserManager() # yo line bina default  user manage use hunxa so to avoid it we call sutom usermanager ko object


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS =[] # This specifies the fields that are required when creating a user via createsuperuser

    def save(self,*args, **kwargs):
        #membership start date initialize garako based on today
        if self.membership_type and not self.membership_start_date:
            self.membership_start_date = timezone.now()

            # expiry date set garako

            if self.membership_type=='SILVER':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=30)
            elif self.membership_type=='GOLD':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=90)
            elif self.membership_type=='DIAMOND':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=365)


        super().save(*args,**kwargs)   # we call seper().save() to continue with the normal save process


            

        

