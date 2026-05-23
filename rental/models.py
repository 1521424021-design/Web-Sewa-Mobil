from django.db import models
from django.contrib.auth.models import User

class PSUnit(models.Model):
    TIPE_CHOICES = [
        ('PS1', 'PlayStation 1'),
        ('PS2', 'PlayStation 2'),
        ('PS3', 'PlayStation 3'),
        ('PS4', 'PlayStation 4'),
        ('PS5', 'PlayStation 5'),
        ('PS6', 'PlayStation 6'),
    ]
    STATUS_CHOICES = [
        ('tersedia', 'Tersedia'),
        ('dipakai', 'Sedang Dimainkan'),
    ]

    nomor_ps = models.CharField(max_length=10, verbose_name="Nomor Unit PS")
    tipe_ps = models.CharField(max_length=10, choices=TIPE_CHOICES, verbose_name="Tipe PS")
    harga_per_jam = models.IntegerField(verbose_name="Harga per Jam (Rp)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tersedia')
    gambar_url = models.URLField(blank=True, null=True, help_text="URL gambar console dari internet")

    def __str__(self):
        return f"{self.tipe_ps} (Unit {self.nomor_ps})"

class PesananPS(models.Model):
    STATUS_BAYAR_CHOICES = [
        ('Belum Bayar', 'Belum Bayar'),
        ('Lunas', 'Lunas'),
    ]
    METODE_BAYAR_CHOICES = [
        ('Cash / Tunai', 'Cash / Tunai'),
        ('QRIS / Dana / Gopay', 'QRIS / Dana / Gopay'),
        ('Transfer Bank', 'Transfer Bank'),
    ]

    id_sewa = models.AutoField(primary_key=True, verbose_name="ID Sewa")
    ps_unit = models.ForeignKey(PSUnit, on_delete=models.CASCADE, related_name="booking_ps")
    nama_penyewa = models.CharField(max_length=100, verbose_name="Nama Penyewa")
    no_hp = models.CharField(max_length=15, verbose_name="Nomor HP/WhatsApp")
    tanggal_sewa = models.DateField(verbose_name="Tanggal Sewa")
    jam_mulai = models.TimeField(verbose_name="Jam Mulai")
    jam_selesai = models.TimeField(verbose_name="Jam Selesai", blank=True, null=True) # Dihitung otomatis di views
    lama_main = models.IntegerField(verbose_name="Lama Main (Jam)")
    metode_pembayaran = models.CharField(max_length=30, choices=METODE_BAYAR_CHOICES, default='Cash / Tunai', verbose_name="Metode Pembayaran")
    total_bayar = models.IntegerField(blank=True, null=True, verbose_name="Total Bayar")
    status_pembayaran = models.CharField(max_length=20, choices=STATUS_BAYAR_CHOICES, default='Belum Bayar', verbose_name="Status Pembayaran")

    def __str__(self):
        return f"INV-{self.id_sewa:04d} | {self.nama_penyewa}"

# Pastikan potongan kode ini ada di bagian paling bawah rental/models.py
class BukuTamuPS(models.Model):
    KATEGORI_CHOICES = [
        ('Kritik / Saran', 'Kritik / Saran'),
        ('Request Game Baru', 'Request Game Baru'),
        ('Cari Lawan Mabar', 'Cari Lawan Mabar'),
    ]

    nama = models.CharField(max_length=100, verbose_name="Nama Gamers")
    kategori = models.CharField(max_length=30, choices=KATEGORI_CHOICES, default='Kritik / Saran', verbose_name="Kategori Kiriman")
    pesan = models.TextField(verbose_name="Isi Pesan / Tantangan Mabar")
    nama_game_request = models.CharField(max_length=100, blank=True, null=True, verbose_name="Judul Game (Khusus Request Game)")
    jumlah_voting = models.IntegerField(default=0, verbose_name="Jumlah Vote Suka")
    
    # Fitur Pin dari Admin (Papan Pengumuman Turnamen)
    is_disematkan = models.BooleanField(default=False, verbose_name="Sematkan di Paling Atas (Pin Comment)")
    
    tanggal_kirim = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.kategori}] {self.nama}"

class ShiftOperator(models.Model):
    id_shift = models.AutoField(primary_key=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Operator")
    waktu_buka = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Buka Shift")
    waktu_tutup = models.DateTimeField(blank=True, null=True, verbose_name="Waktu Tutup Shift")
    modal_awal = models.IntegerField(verbose_name="Modal Awal Laci (Rp)")
    uang_fisik_akhir = models.IntegerField(blank=True, null=True, verbose_name="Uang Fisik Akhir di Laci (Rp)")
    total_pendapatan_sistem = models.IntegerField(default=0, verbose_name="Pendapatan via Sistem (Rp)")
    status = models.CharField(max_length=10, choices=[('Buka', 'Buka'), ('Tutup', 'Tutup')], default='Buka')

    def __str__(self):
        return f"Shift {self.operator.username} - {self.status} ({self.waktu_buka.strftime('%d/%m/%Y')})"