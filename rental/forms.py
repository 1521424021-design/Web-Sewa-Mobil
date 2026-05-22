from django import forms
from .models import BukuTamu, Pesanan

class BukuTamuForm(forms.ModelForm):
    class Meta:
        model = BukuTamu
        fields = ['nama', 'email', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap Anda'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'alamat@email.com'}),
            'pesan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tulis ulasan Anda...'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama_penyewa', 'nomor_hp', 'tanggal_mulai', 'tanggal_selesai']
        widgets = {
            'nama_penyewa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama sesuai KTP'}),
            'nomor_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 08123456789'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }