from django.db import models

class Mobil(models.Model):
    STATUS_CHOICES = [
        ('tersedia', 'Tersedia'),
        ('disewa', 'Sedang Disewa'),
    ]

    nama_mobil = models.CharField(max_length=100, verbose_name="Nama Mobil")
    merek = models.CharField(max_length=50)
    harga_per_hari = models.IntegerField(verbose_name="Harga per Hari (Rp)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tersedia')
    deskripsi = models.TextField(blank=True, null=True)
    gambar_url = models.URLField(blank=True, null=True, help_text="Masukkan URL foto mobil dari internet")

    def __str__(self):
        return f"{self.merek} {self.nama_mobil}"

class Pesanan(models.Model):
    # Menghubungkan pesanan dengan mobil yang dipilih
    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE, related_name="pesanan")
    nama_penyewa = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    nomor_hp = models.CharField(max_length=15, verbose_name="Nomor WhatsApp")
    tanggal_mulai = models.DateField(verbose_name="Tanggal Mulai Sewa")
    tanggal_selesai = models.DateField(verbose_name="Tanggal Selesai Sewa")
    total_harga = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Sewa {self.mobil.nama_mobil} oleh {self.nama_penyewa}"

class BukuTamu(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    pesan = models.TextField(verbose_name="Ulasan / Feedback")
    tanggal_kirim = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pesan dari {self.nama}"