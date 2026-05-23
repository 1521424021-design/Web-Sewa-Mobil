from django.shortcuts import render, redirect, get_object_or_404
from .models import PSUnit, PesananPS, BukuTamuPS
from .forms import BukuTamuForm, BookingPSForm
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from .models import PSUnit, PesananPS, ShiftOperator
from .forms import BukaShiftForm, TutupShiftForm
import json

def katalog_ps(request):
    daftar_ps = PSUnit.objects.all()
    
    # Ambil data pesanan aktif terakhir untuk setiap unit PS yang sedang digunakan
    for ps in daftar_ps:
        if ps.status == 'dipakai':
            # Cari pesanan terbaru yang belum lunas atau yang statusnya sedang berjalan hari ini
            pesanan_aktif = PesananPS.objects.filter(ps_unit=ps).order_by('-id_sewa').first()
            if pesanan_aktif and pesanan_aktif.jam_selesai:
                # Gabungkan tanggal sewa dan jam selesai menjadi format ISO standar untuk JavaScript
                datetime_selesai = datetime.combine(pesanan_aktif.tanggal_sewa, pesanan_aktif.jam_selesai)
                ps.waktu_selesai_iso = datetime_selesai.isoformat()
            else:
                ps.waktu_selesai_iso = ""
        else:
            ps.waktu_selesai_iso = ""

    return render(request, 'rental/mobil_list.html', {'daftar_ps': daftar_ps})

def proses_booking_ps(request, ps_id):
    ps = get_object_or_404(PSUnit, id=ps_id)
    if request.method == "POST":
        form = BookingPSForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.ps_unit = ps
            
            # 1. LOGIKA MATEMATIKA: Hitung Total Bayar
            durasi = int(form.cleaned_data['lama_main'])
            pesanan.total_bayar = durasi * ps.harga_per_jam
            
            # 2. LOGIKA WAKTU: Hitung Jam Selesai Otomatis
            waktu_mulai = form.cleaned_data['jam_mulai']
            tgl = form.cleaned_data['tanggal_sewa']
            
            # Gabungkan tgl dan jam ke format datetime untuk manipulasi waktu timedelta
            datetime_gabung = datetime.combine(tgl, waktu_mulai)
            datetime_selesai = datetime_gabung + timedelta(hours=durasi)
            
            # Masukkan hasil kalkulasi jam ke database
            pesanan.jam_selesai = datetime_selesai.time()
            pesanan.save()
            
            # Update status PS di rental monitor
            ps.status = 'dipakai'
            ps.save()
            
            return render(request, 'rental/booking_sukses.html', {'pesanan': pesanan})
    else:
        # Isi default tanggal hari ini agar form lebih rapi
        form = BookingPSForm(initial={'tanggal_sewa': datetime.now().date(), 'jam_mulai': datetime.now().strftime('%H:%M')})
        
    return render(request, 'rental/booking_form.html', {'form': form, 'ps': ps})

def digital_guestbook_ps(request):
    if request.method == "POST":
        form = BukuTamuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guestbook')
    else:
        form = BukuTamuForm()

    # Urutan Pintar: Komentar yang di-pin (True) tampil pertama, baru disusul komentar terbaru
    ulasan = BukuTamuPS.objects.all().order_by('-is_disematkan', '-tanggal_kirim')
    return render(request, 'rental/buku_tamu.html', {'form': form, 'semua_ulasan': ulasan})

# Fungsi Baru untuk menghitung Vote Suka Game Request
def vote_game_request(request, ulasan_id):
    ulasan = get_object_or_404(BukuTamuPS, id=ulasan_id)
    ulasan.jumlah_voting += 1
    ulasan.save()
    return redirect('guestbook')

@login_required
def dashboard_owner(request):
    # 1. AMBIL DATA TRANSAKSI YANG SUDAH LUNAS
    transaksi_lunas = PesananPS.objects.filter(status_pembayaran='Lunas').order_by('tanggal_sewa')

    # Kamus (Dictionary) untuk menampung hitungan Python
    hitung_harian = {}
    hitung_bulanan = {}

    # Olah data tanggal menggunakan logika Python murni (Bebas dari Bug SQLite)
    for t in transaksi_lunas:
        if t.total_bayar:
            # Format Harian (Contoh: "24 May")
            str_hari = t.tanggal_sewa.strftime('%d %b')
            hitung_harian[str_hari] = hitung_harian.get(str_hari, 0) + t.total_bayar

            # Format Bulanan (Contoh: "May 2026")
            str_bulan = t.tanggal_sewa.strftime('%B %Y')
            hitung_bulanan[str_bulan] = hitung_bulanan.get(str_bulan, 0) + t.total_bayar

    # Pecah hasil kamus ke dalam bentuk List untuk dikirim ke Chart.js
    # Ambil maksimal 7 hari terakhir agar grafik tidak kepenuhan
    label_hari = list(hitung_harian.keys())[-7:]
    data_hari = list(hitung_harian.values())[-7:]

    label_bulan = list(hitung_bulanan.keys())
    data_bulan = list(hitung_bulanan.values())

    # 2. LOGIKA MANAJEMEN SHIFT OPERATOR KASIR (Tetap sama seperti kemarin)
    shift_aktif = ShiftOperator.objects.filter(operator=request.user, status='Buka').first()
    
    form_buka = BukaShiftForm()
    form_tutup = TutupShiftForm()

    if request.method == "POST":
        if "aksi_buka" in request.POST:
            form = BukaShiftForm(request.POST)
            if form.is_valid():
                shift = form.save(commit=False)
                shift.operator = request.user
                shift.status = 'Buka'
                shift.save()
                return redirect('dashboard_owner')
                
        elif "aksi_tutup" in request.POST and shift_aktif:
            form = TutupShiftForm(request.POST)
            if form.is_valid():
                # Hitung pendapatan selama operator memegang laci shift ini
                total_sistem = PesananPS.objects.filter(
                    status_pembayaran='Lunas',
                    tanggal_sewa__gte=shift_aktif.waktu_buka.date()
                ).aggregate(total=Sum('total_bayar'))['total'] or 0
                
                shift_aktif.uang_fisik_akhir = form.cleaned_data['uang_fisik_akhir']
                shift_aktif.total_pendapatan_sistem = total_sistem
                shift_aktif.waktu_tutup = timezone.now()
                shift_aktif.status = 'Tutup'
                shift_aktif.save()
                return redirect('dashboard_owner')

    # Hitung total omset kumulatif
    total_omset = transaksi_lunas.aggregate(total=Sum('total_bayar'))['total'] or 0
    riwayat_shift = ShiftOperator.objects.all().order_by('-waktu_buka')[:5]

    context = {
        'label_hari': json.dumps(label_hari),
        'data_hari': json.dumps(data_hari),
        'label_bulan': json.dumps(label_bulan),
        'data_bulan': json.dumps(data_bulan),
        'shift_aktif': shift_aktif,
        'form_buka': form_buka,
        'form_tutup': form_tutup,
        'total_omset': total_omset,
        'riwayat_shift': riwayat_shift,
    }
    return render(request, 'rental/dashboard_owner.html', context)