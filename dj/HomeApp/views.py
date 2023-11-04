from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from pyexpat.errors import messages

from .models import *


class BoshSahifaView(View):
    def get(self, request):
        data = {
            "guruhlar": QonGuruh.objects.annotate(jami=Count('donor'))
        }
        return render(request, 'bosh_sahifa.html', data)


class DonorlarView(View):
    def get(self, request, pk):
        qon_guruh = QonGuruh.objects.filter(id=pk).first()
        data = {
            "donorlar": Donor.objects.filter(qon_guruh=qon_guruh)
        }
        return render(request, "donorlar.html", data)


class DonorView(View):
    def get(self, request, pk):
        data = {
            'donor': Donor.objects.get(id=pk)
        }
        return render(request, 'donor.html', data)


class QonSorashView(View):
    def get(self, request):
        return render(request, "qon_sorash.html")

    def post(self, request):
        FIO = request.POST['FIO']
        email = request.POST['email']
        tel = request.POST['tel']
        vil = request.POST['vil']
        tuman = request.POST['tuman']
        manzil = request.POST['manzil']
        qon_guruh = request.POST['qon_guruh']
        sana = request.POST['sana']
        qon_sorash = QonOluvchi.objects.create(
            FIO=FIO,
            email=email,
            tel=tel,
            vil=vil,
            tuman=tuman,
            manzil=manzil,
            qon_guruh=QonGuruh.objects.get(nom=qon_guruh),
            sana=sana
        )
        qon_sorash.save()
        return render(request, "bosh_sahifa.html")


class BarchaQonOluvchilarView(View):
    def get(self, request):
        oluvchilar = QonOluvchi.objects.all()
        return render(request, "barcha_qon_oluvchilar.html", {"oluvchilar": oluvchilar})


class DonorBolishView(View):
    def get(self, request):
        return render(request, "donor_bolish.html")

    def post(self, request):
        username = request.POST['username']
        ism = request.POST['ism']
        fam = request.POST['fam']
        email = request.POST['email']
        tel = request.POST['tel']
        vil = request.POST['vil']
        tuman = request.POST['tuman']
        manzil = request.POST['manzil']
        jins = request.POST['jins']
        qon_guruh = request.POST['qon_guruh']
        t_sana = request.POST['t_sana']
        rasm = request.FILES['rasm']
        parol = request.POST['parol']
        parol_tasdiqlash = request.POST['parol_tasdiqlash']

        if parol != parol_tasdiqlash:
            messages.error(request, "Parollar mos kelmaydi.")
            return redirect('/login')

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=ism,
            last_name=fam,
            password=parol)
        donor = Donor.objects.create(
            donor=user,
            tel=tel,
            vil=vil,
            tuman=tuman,
            manzil=manzil,
            jins=jins,
            qon_guruh=QonGuruh.objects.get(nom=qon_guruh),
            t_sana=t_sana,
            rasm=rasm)
        user.save()
        donor.save()
        return render(request, "bosh_sahifa.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profil")
            else:
                return render(request, "login.html")
        return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def profil(request):
    return render(request, "profil.html", {'donor_profil': Donor.objects.get(donor=request.user)})


@login_required(login_url='/login')
def profil_tahrirlash(request):
    donor_profil = Donor.objects.get(donor=request.user)
    if request.method == "POST":
        email = request.POST['email']
        tel = request.POST['tel']
        vil = request.POST['vil']
        tuman = request.POST['tuman']
        manzil = request.POST['manzil']

        donor_profil.donor.email = email
        donor_profil.tel = tel
        donor_profil.vil = vil
        donor_profil.tuman = tuman
        donor_profil.manzil = manzil
        donor_profil.save()
        donor_profil.donor.save()

        try:
            rasm = request.FILES['rasm']
            donor_profil.rasm = rasm
            donor_profil.save()
        except:
            pass
        ogohlantirish = True
        return render(request, "profil_tahrirlash.html", {'alert': ogohlantirish})
    return render(request, "profil_tahrirlash.html", {'donor_profil': donor_profil})


@login_required(login_url='/login')
def status_belgilash(request):
    donor_profil = Donor.objects.get(donor=request.user)
    if donor_profil.topshirishga_tayyor:
        donor_profil.topshirishga_tayyor = False
        donor_profil.save()
    else:
        donor_profil.topshirishga_tayyor = True
        donor_profil.save()
    return redirect('/profil')