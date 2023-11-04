from django.db import models

from django.db import models
from django.contrib.auth.models import User


class QonGuruh(models.Model):
    nom = models.CharField(max_length=5)

    def __str__(self):
        return self.nom


class QonOluvchi(models.Model):
    FIO = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    vil = models.CharField(max_length=200, blank=True)
    tuman = models.CharField(max_length=300, blank=True)
    manzil = models.CharField(max_length=500, blank=True)
    qon_guruh = models.ForeignKey(QonGuruh, on_delete=models.CASCADE)
    sana = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.FIO


class Donor(models.Model):
    donor = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    t_sana = models.DateField(blank=True)
    tel = models.CharField(max_length=20)
    vil = models.CharField(max_length=100)
    tuman = models.CharField(max_length=100)
    manzil = models.TextField(max_length=500, blank=True)
    qon_guruh = models.ForeignKey(QonGuruh, on_delete=models.CASCADE)
    jins = models.CharField(max_length=10, choices=[
        ("Erkak", "Erkak"),
        ("Ayol", "Ayol"),
    ])
    rasm = models.ImageField(upload_to="", blank=True)
    topshirishga_tayyor = models.BooleanField(default=True)

    def __str__(self):
        return str(self.qon_guruh)

