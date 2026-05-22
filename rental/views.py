from django.shortcuts import render, redirect, get_object_or_404
from .models import Mobil, BukuTamu, Pesanan
from .forms import BukuTamuForm, BookingForm
from datetime import datetime

def katalog_mobil(request):
    armada = Mobil.objects.all()
    return render(request, 'rental/mobil_list.html', {'armada': armada})

def proses_booking(request, mobil_id):
    mobil = get_object_or_404(Mobil, id=mobil_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.mobil = mobil
            
            # Hitung otomatis total harga berdasarkan durasi hari
            d1 = datetime.strptime(request.POST['tanggal_mulai'], "%Y-%m-%d")
            d2 = datetime.strptime(request.POST['tanggal_selesai'], "%Y-%m-%d")
            durasi_hari = (d2 - d1).days
            
            if durasi_hari <= 0:
                durasi_hari = 1 # Minimal sewa 1 hari
                
            pesanan.total_harga = durasi_hari * mobil.harga_per_hari
            pesanan.save()
            
            # Ubah status mobil menjadi disewa
            mobil.status = 'disewa'
            mobil.save()
            
            return render(request, 'rental/booking_sukses.html', {'pesanan': pesanan})
    else:
        form = BookingForm()
        
    return render(request, 'rental/booking_form.html', {'form': form, 'mobil': mobil})

def digital_guestbook(request):
    if request.method == "POST":
        form = BukuTamuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guestbook')
    else:
        form = BukuTamuForm()

    ulasan = BukuTamu.objects.all().order_by('-tanggal_kirim')
    return render(request, 'rental/buku_tamu.html', {'form': form, 'semua_ulasan': ulasan})