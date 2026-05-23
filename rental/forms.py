from django import forms
from .models import BukuTamuPS, PesananPS
import datetime

from django import forms
from .models import BukuTamuPS
from .models import ShiftOperator

class BukuTamuForm(forms.ModelForm):
    class Meta:
        model = BukuTamuPS
        fields = ['nama', 'kategori', 'nama_game_request', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama panggilan/ID Gamers...'}),
            'kategori': forms.Select(attrs={'class': 'form-select', 'id': 'id_kategori_bukutamu'}),
            'nama_game_request': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: GTA VI, FIFA 2027 (Kosongkan jika bukan request)'}),
            'pesan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tulis kritik, ajakan mabar + No HP, atau info turnamen...'}),
        }

class BookingPSForm(forms.ModelForm):
    class Meta:
        model = PesananPS
        # jam_selesai dihapus dari form agar dihitung otomatis oleh sistem backend
        fields = ['nama_penyewa', 'no_hp', 'tanggal_sewa', 'jam_mulai', 'lama_main', 'metode_pembayaran']
        widgets = {
            'nama_penyewa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap player'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 081234xxxx'}),
            'tanggal_sewa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jam_mulai': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'lama_main': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Durasi main (Jam)'}),
            'metode_pembayaran': forms.Select(attrs={'class': 'form-select'}),
        }

class BukaShiftForm(forms.ModelForm):
    class Meta:
        model = ShiftOperator
        fields = ['modal_awal']
        widgets = {
            'modal_awal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan saldo awal laci kasir (Rp)...'}),
        }

class TutupShiftForm(forms.ModelForm):
    class Meta:
        model = ShiftOperator
        fields = ['uang_fisik_akhir']
        widgets = {
            'uang_fisik_akhir': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hitung uang fisik di laci saat ini (Rp)...'}),
        }