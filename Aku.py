#!/usr/bin/env python3
"""
APLIKASI MANAJEMEN KEUANGAN
============================
Program untuk mencatat dan mengelola keuangan dengan fitur:
- Nomor transaksi otomatis
- Hari transaksi
- Pemasukan
- Pengeluaran
- Keterangan (opsional)

Fitur Utama:
✓ Tambah transaksi baru
✓ Lihat semua transaksi
✓ Cari berdasarkan hari
✓ Edit transaksi
✓ Hapus transaksi
✓ Laporan keuangan lengkap
✓ Data tersimpan otomatis dalam JSON
"""

import json
from datetime import datetime
import os

# File untuk menyimpan data keuangan
DATA_FILE = 'keuangan_data.json'

def load_data():
    """Memuat data dari file JSON"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return []

def save_data(data):
    """Menyimpan data ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('✓ Data berhasil disimpan.')

def get_next_nomor():
    """Mendapatkan nomor transaksi berikutnya"""
    data = load_data()
    if not data:
        return 1
    try:
        nomorlist = [t['nomor'] for t in data]
        return max(nomorlist) + 1
    except (ValueError, KeyError):
        return len(data) + 1

def add_entry(hari, pemasukkan, pengeluaran, keterangan=""):
    """Menambah entri keuangan baru"""
    data = load_data()
    nomor = get_next_nomor()
    
    entry = {
        'nomor': nomor,
        'hari': hari,
        'pemasukkan': pemasukkan,
        'pengeluaran': pengeluaran,
        'keterangan': keterangan,
        'tanggal_input': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data.append(entry)
    save_data(data)
    print(f'✓ Entri nomor {nomor} berhasil ditambahkan.')

def list_entries():
    """Menampilkan daftar semua entri dalam format tabel"""
    data = load_data()
    
    if not data:
        print('\n📊 Belum ada data keuangan.\n')
        return
    
    print('\n' + '='*110)
    print(f"{'No':<5} {'Hari':<15} {'Pemasukan':<15} {'Pengeluaran':<15} {'Keterangan':<30} {'Tanggal Input':<20}")
    print('='*110)
    
    total_pemasukkan = 0
    total_pengeluaran = 0
    
    for entry in data:
        nomor = entry['nomor']
        hari = entry['hari']
        pemasukkan = entry['pemasukkan']
        pengeluaran = entry['pengeluaran']
        keterangan = entry.get('keterangan', '')[:28]
        tanggal = entry.get('tanggal_input', '')
        
        print(f"{nomor:<5} {hari:<15} Rp{pemasukkan:>12,} Rp{pengeluaran:>12,} {keterangan:<30} {tanggal:<20}")
        
        total_pemasukkan += pemasukkan
        total_pengeluaran += pengeluaran
    
    print('='*110)
    saldo = total_pemasukkan - total_pengeluaran
    print(f"Total Pemasukan   : Rp{total_pemasukkan:,}")
    print(f"Total Pengeluaran : Rp{total_pengeluaran:,}")
    print(f"Saldo Akhir       : Rp{saldo:,}\n")

def search_by_hari(hari):
    """Mencari entri berdasarkan hari"""
    data = load_data()
    results = [e for e in data if e['hari'].lower() == hari.lower()]
    
    if not results:
        print(f"\n❌ Tidak ada transaksi pada hari {hari}.\n")
        return
    
    print(f"\n📅 Transaksi pada {hari}:")
    print('-'*100)
    print(f"{'No':<5} {'Pemasukan':<15} {'Pengeluaran':<15} {'Keterangan':<50}")
    print('-'*100)
    
    total_pemasukkan = 0
    total_pengeluaran = 0
    
    for entry in results:
        nomor = entry['nomor']
        pemasukkan = entry['pemasukkan']
        pengeluaran = entry['pengeluaran']
        keterangan = entry.get('keterangan', '')[:48]
        
        print(f"{nomor:<5} Rp{pemasukkan:>12,} Rp{pengeluaran:>12,} {keterangan:<50}")
        total_pemasukkan += pemasukkan
        total_pengeluaran += pengeluaran
    
    print('-'*100)
    print(f"Total Pemasukan   : Rp{total_pemasukkan:,}")
    print(f"Total Pengeluaran : Rp{total_pengeluaran:,}")
    print(f"Saldo             : Rp{total_pemasukkan - total_pengeluaran:,}\n")

def delete_entry(nomor):
    """Menghapus entri berdasarkan nomor"""
    data = load_data()
    original_length = len(data)
    data = [e for e in data if e['nomor'] != nomor]
    
    if len(data) == original_length:
        print(f"\n❌ Entri nomor {nomor} tidak ditemukan.\n")
    else:
        save_data(data)
        print(f"\n✓ Entri nomor {nomor} berhasil dihapus.\n")

def edit_entry(nomor):
    """Mengedit entri berdasarkan nomor"""
    data = load_data()
    
    entry = next((e for e in data if e['nomor'] == nomor), None)
    if not entry:
        print(f"\n❌ Entri nomor {nomor} tidak ditemukan.\n")
        return
    
    print(f"\n📝 Edit Entri Nomor {nomor}")
    print(f"Data Lama: Hari={entry['hari']}, Pemasukan=Rp{entry['pemasukkan']:,}, Pengeluaran=Rp{entry['pengeluaran']:,}")
    
    try:
        hari_baru = input("Hari baru (tekan Enter untuk skip): ").strip()
        if hari_baru:
            entry['hari'] = hari_baru
        
        pemasukkan_str = input("Pemasukan baru (tekan Enter untuk skip): ").strip()
        if pemasukkan_str:
            entry['pemasukkan'] = int(pemasukkan_str)
        
        pengeluaran_str = input("Pengeluaran baru (tekan Enter untuk skip): ").strip()
        if pengeluaran_str:
            entry['pengeluaran'] = int(pengeluaran_str)
        
        keterangan = input("Keterangan baru (tekan Enter untuk skip): ").strip()
        if keterangan:
            entry['keterangan'] = keterangan
        
        entry['tanggal_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(data)
        print("✓ Entri berhasil diperbarui.\n")
    except ValueError:
        print("❌ Input tidak valid. Gunakan angka untuk pemasukan dan pengeluaran.\n")

def format_rupiah(angka):
    """Format angka menjadi format Rupiah"""
    return f"Rp{angka:,}".replace(',', '.')

def main_menu():
    """Menu utama aplikasi"""
    while True:
        print("\n" + "="*60)
        print("💰 APLIKASI MANAJEMEN KEUANGAN 💰".center(60))
        print("="*60)
        print("1. Tambah Transaksi")
        print("2. Lihat Semua Transaksi")
        print("3. Cari Transaksi Berdasarkan Hari")
        print("4. Edit Transaksi")
        print("5. Hapus Transaksi")
        print("6. Lihat Laporan Keuangan")
        print("7. Keluar")
        print("="*60)
        
        choice = input("Pilih menu (1-7): ").strip()
        
        if choice == '1':
            try:
                print("\n📋 TAMBAH TRANSAKSI BARU")
                hari = input("Masukkan hari (Senin, Selasa, dst): ").strip()
                if not hari:
                    hari = datetime.now().strftime("%A")
                
                pemasukkan = int(input("Masukkan jumlah pemasukan (Rp): "))
                pengeluaran = int(input("Masukkan jumlah pengeluaran (Rp): "))
                keterangan = input("Masukkan keterangan (opsional): ").strip()
                
                if pemasukkan < 0 or pengeluaran < 0:
                    print("❌ Nilai tidak boleh negatif.\n")
                else:
                    add_entry(hari, pemasukkan, pengeluaran, keterangan)
            except ValueError:
                print("❌ Input tidak valid. Gunakan angka untuk pemasukan dan pengeluaran.\n")
        
        elif choice == '2':
            list_entries()
        
        elif choice == '3':
            hari = input("\nMasukkan hari yang dicari: ").strip()
            if hari:
                search_by_hari(hari)
        
        elif choice == '4':
            try:
                nomor = int(input("\nMasukkan nomor transaksi yang ingin diedit: "))
                edit_entry(nomor)
            except ValueError:
                print("❌ Input tidak valid. Gunakan angka untuk nomor.\n")
        
        elif choice == '5':
            try:
                nomor = int(input("\nMasukkan nomor transaksi yang ingin dihapus: "))
                delete_entry(nomor)
            except ValueError:
                print("❌ Input tidak valid. Gunakan angka untuk nomor.\n")
        
        elif choice == '6':
            list_entries()
        
        elif choice == '7':
            print("\n👋 Terima kasih telah menggunakan Aplikasi Manajemen Keuangan!")
            print("Data telah tersimpan di 'keuangan_data.json'\n")
            break
        
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.\n")

if __name__ == '__main__':
    main_menu()