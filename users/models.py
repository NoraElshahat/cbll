from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

PASSWORD_LENGTH = 6


class CblUserManager(BaseUserManager):
    def create_user(self, **args):
        if not args["email"]:
            raise ValueError("E-mail cannot be empty")

        if not args["first"]:
            raise ValueError("Name cannot be empty")

        if not args["last"]:
            raise ValueError("last cannot be empty")

        if not args["password"] or len(args["password"]) < PASSWORD_LENGTH:
            raise ValueError("Password cannot be empty")

        if not args["phone"]:
            raise ValueError("Phone cannot be empty")

        if not args["gender"]:
            raise ValueError("gender cannot be empty")

        if not args["country"]:
            raise ValueError("country cannot be empty")

        email = self.normalize_email(args["email"])

        user = self.model(
            first=str(args["first"]).lower(),
            last=str(args["last"]).lower(),
            email=str(args["email"]).lower(),
            phone=str(args["phone"]).lower(),
            gender=str(args["gender"]).lower(),
            country=str(args["country"]).lower(),
            address=str(args["address"]).lower() if args["address"] else "",
        )

        user.set_password(args["password"])
        user.save(using=self._db)

        return user

    def create_superuser(self, **args):
        if not args["email"]:
            raise ValueError("E-mail cannot be empty")

        if not args["first"]:
            raise ValueError("Name cannot be empty")

        if not args["last"]:
            raise ValueError("last cannot be empty")

        if not args["password"] or len(args["password"]) < PASSWORD_LENGTH:
            raise ValueError("Password cannot be empty")

        if not args["phone"]:
            raise ValueError("Phone cannot be empty")

        if not args["gender"]:
            raise ValueError("gender cannot be empty")

        if not args["country"]:
            raise ValueError("country cannot be empty")

        superuser = self.create_user(**args)

        superuser.set_password(args["password"])
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)

        return superuser

    def create_staff_only(self, **args):
        staff = self.create_user(**args)
        staff.is_staff = True
        staff.save(using=self._db)

        return staff

    def create_super_admin(self, **args):
        super_admin = self.create_superuser(**args)
        super_admin.is_super_admin = True
        super_admin.save(using=self._db)

        return super_admin


class CblUser(AbstractBaseUser, PermissionsMixin):
    gender = (("male", "Male"), ("female", "Female"))
    country = (("egypt", "EGYPT"), ("usa", "USA"), ("germany", "Germany"))

    def get_countries(self):
        with open("countries") as target:
            pass

    email = models.EmailField(
        unique=True,
        max_length=250,
        verbose_name="user email",
        help_text="enter a valid user mail",
        error_messages={"invalid": "Cannot email be empty"},
    )
    first = models.CharField(
        max_length=250, verbose_name="first name", help_text="enter a valid first name"
    )
    last = models.CharField(
        max_length=250, verbose_name="last name", help_text="enter a valid last name"
    )
    phone = models.CharField(
        max_length=20, unique=True, help_text="enter a valid phone number"
    )
    gender = models.CharField(
        max_length=6, choices=gender, default="male", help_text="select a gender"
    )
    country = models.CharField(
        max_length=100, choices=country, help_text="select a country"
    )
    address = models.CharField(
        max_length=200, blank=True, help_text="enter a valid address"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    img = models.ImageField(
        _("user picture"),
        upload_to="storage/users/",
        blank=True,
        default="",
        null=False,
        height_field=None,
        width_field=None,
        max_length=None,
    )
    # token = models.CharField(max_length=300, blank=True)
    department = models.ForeignKey("department.Department", on_delete=models.DO_NOTHING)

    hu_id = models.CharField(max_length=30, blank=True)

    objects = CblUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first", "last", "gender", "phone", "country", "address"]

    def user_name(self) -> str:
        return self.first + " " + self.last

    def faculty(self):
        return str(self.department.faculty)

    def last_login_str(self):
        if self.last_login:
            return datetime.strftime(self.last_login, "%Y-%m-%d")
        return "-"

    def visits(self):
        _visits = []
        for visit in self.visit.all():
            _visits.append(
                {
                    "id": int(visit.id),
                    "name": str(visit),
                    "objectives": str(visit.objectives),
                    "from": str(visit.date),
                    "to": str(visit.to),
                    "img": str(visit.main_img),
                    "is_available": datetime.strftime(datetime.today(), "%Y-%m-%d")
                    < str(visit.to),
                }
            )
        return _visits

    def visits_no(self):
        return self.visit.count()


class BlockedStudents(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("blocked_students"), on_delete=models.DO_NOTHING)
    visit   = models.ForeignKey('visit.Visit', verbose_name=_("Visit"), on_delete=models.DO_NOTHING)
    reason  = models.TextField(_("reason for remove a student"), default='', blank=False)

    def __str__(self):
        return f'Blocked students for {str(self.visit)}'