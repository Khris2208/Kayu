#!/usr/bin/env python3
"""
APLIKASI DETEKSI KESEHATAN MENTAL
====================================
Program untuk mendeteksi status kesehatan mental seseorang berdasarkan:
- Nama
- Usia
- Jenis Kelamin
- Gejala dan perasaan yang dialami

Fitur Utama:
✓ Input data responden
✓ Deteksi kondisi mental berdasarkan gejala
✓ Rekomendasi tindakan
✓ Riwayat pemeriksaan
✓ Data tersimpan dalam JSON
"""

import json
import os
from datetime import datetime

# File untuk menyimpan data pemeriksaan
DATA_FILE = 'pemeriksaan_mental.json'

# Database gejala dan kategori kesehatan mental
GEJALA_DATABASE = {
    'depresi': {
        'gejala': [
            'sedih berkelanjutan',
            'kehilangan minat',
            'mudah lelah',
            'sulit tidur',
            'merasa bersalah',
            'konsentrasi menurun',
            'nafsu makan berubah',
            'pemikiran negatif'
        ],
        'deskripsi': 'Depresi adalah gangguan mood yang ditandai dengan perasaan sedih mendalam dan kehilangan minat terhadap aktivitas.',
        'tingkat_risiko': 'Tinggi',
        'rekomendasi': [
            'Konsultasi dengan psikolog profesional',
            'Mulai terapi perilaku kognitif',
            'Jaga rutinitas tidur dan makan',
            'Lakukan aktivitas fisik ringan',
            'Berbagi perasaan dengan orang terdekat'
        ]
    },
    'kecemasan': {
        'gejala': [
            'khawatir berlebihan',
            'gelisah',
            'jantung berdebar',
            'keringat dingin',
            'sesak napas',
            'insomnia',
            'otot tegang',
            'sulit berkonsentrasi'
        ],
        'deskripsi': 'Gangguan kecemasan ditandai dengan rasa khawatir yang berlebihan dan tidak dapat dikontrol.',
        'tingkat_risiko': 'Sedang-Tinggi',
        'rekomendasi': [
            'Praktik teknik relaksasi dan pernapasan',
            'Konsultasi dengan profesional kesehatan mental',
            'Batasi kafein dan stimulan',
            'Lakukan meditasi atau mindfulness',
            'Olahraga teratur untuk mengurangi stres'
        ]
    },
    'stres': {
        'gejala': [
            'mudah marah',
            'kepala pusing',
            'otot tegang',
            'kelelahan ekstrem',
            'sulit fokus',
            'perubahan nafsu makan',
            'iritabilitas',
            'gangguan tidur'
        ],
        'deskripsi': 'Stres adalah respons tubuh terhadap tekanan atau tantangan yang dihadapi.',
        'tingkat_risiko': 'Sedang',
        'rekomendasi': [
            'Identifikasi sumber stres',
            'Atur waktu istirahat yang cukup',
            'Lakukan hobi yang menyenangkan',
            'Terhubung dengan keluarga dan teman',
            'Coba teknik manajemen stres seperti yoga'
        ]
    },
    'insomnia': {
        'gejala': [
            'sulit tidur',
            'sering terbangun di malam hari',
            'tidur tidak nyenyak',
            'bangun terlalu pagi',
            'kelelahan siang hari',
            'mood buruk',
            'konsentrasi menurun',
            'rasa kantuk tetapi tidak bisa tidur'
        ],
        'deskripsi': 'Insomnia adalah kesulitan untuk tidur atau mempertahankan tidur yang berkualitas.',
        'tingkat_risiko': 'Sedang',
        'rekomendasi': [
            'Buat rutinitas tidur yang konsisten',
            'Hindari layar sebelum tidur',
            'Batasi kafein setelah jam 2 sore',
            'Ciptakan lingkungan tidur yang nyaman dan gelap',
            'Konsultasi dokter jika berkelanjutan'
        ]
    },
    'bipolar': {
        'gejala': [
            'perubahan mood ekstrem',
            'energi tinggi berlebihan',
            'depresi dalam',
            'bicara cepat',
            'investasi uang besar',
            'kurang tidur tapi merasa bugar',
            'impulsif',
            'gangguan pikiran racing'
        ],
        'deskripsi': 'Gangguan bipolar ditandai dengan perubahan mood ekstrem antara manik dan depresi.',
        'tingkat_risiko': 'Sangat Tinggi',
        'rekomendasi': [
            'Segera konsultasi dengan psikiater',
            'Mungkin memerlukan obat-obatan',
            'Terapi berkelanjutan sangat penting',
            'Hindari pemicu stres',
            'Monitor perubahan mood secara ketat'
        ]
    },
    'sehat': {
        'gejala': [
            'mood stabil',
            'tidur berkualitas',
            'fokus dan konsentrasi baik',
            'energi cukup',
            'hubungan sosial positif',
            'minat dalam aktivitas',
            'tidak ada kekhawatiran berlebihan'
        ],
        'deskripsi': 'Kesehatan mental yang baik - terus jaga keseimbangan dan wellness Anda.',
        'tingkat_risiko': 'Rendah',
        'rekomendasi': [
            'Pertahankan rutinitas hidup sehat',
            'Lanjutkan aktivitas fisik',
            'Jaga hubungan sosial yang positif',
            'Lakukan self-care secara rutin',
            'Pemeriksaan berkala untuk pencegahan'
        ]
    }
}

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
    print('\n✓ Data pemeriksaan berhasil disimpan.')

def hitung_gejala(gejala_input, kategori):
    """Menghitung kecocokan gejala dengan kategori"""
    gejala_kategori = GEJALA_DATABASE[kategori]['gejala']
    kecocokan = sum(1 for g in gejala_input if g.lower() in gejala_kategori)
    persentase = (kecocokan / len(gejala_kategori)) * 100 if gejala_kategori else 0
    return persentase, kecocokan

def deteksi_mental(gejala_input):
    """Mendeteksi kondisi mental berdasarkan gejala yang diberikan"""
    hasil_deteksi = {}
    
    for kategori in GEJALA_DATABASE:
        persentase, jumlah = hitung_gejala(gejala_input, kategori)
        hasil_deteksi[kategori] = {
            'persentase': persentase,
            'jumlah_kecocokan': jumlah
        }
    
    # Mengurutkan berdasarkan persentase tertinggi
    hasil_terurut = sorted(hasil_deteksi.items(), key=lambda x: x[1]['persentase'], reverse=True)
    return hasil_terurut[0][0], hasil_terurut

def input_gejala():
    """Input gejala dari pengguna"""
    print('\n' + '='*60)
    print('MASUKKAN GEJALA YANG ANDA RASAKAN')
    print('='*60)
    print('\nContoh gejala: sedih berkelanjutan, kehilangan minat, mudah lelah')
    print('(Ketik "selesai" untuk mengakhiri input gejala)\n')
    
    gejala_list = []
    nomor = 1
    
    while True:
        gejala = input(f'Gejala {nomor}: ').strip()
        
        if gejala.lower() == 'selesai':
            break
        
        if gejala:
            gejala_list.append(gejala)
            nomor += 1
        else:
            print('⚠ Silakan masukkan gejala yang valid.')
    
    return gejala_list

def tampilkan_hasil_deteksi(nama, usia, jenis_kelamin, gejala, kategori_utama):
    """Menampilkan hasil deteksi kesehatan mental"""
    data_kategori = GEJALA_DATABASE[kategori_utama]
    
    print('\n' + '='*70)
    print('HASIL DETEKSI KESEHATAN MENTAL')
    print('='*70)
    
    print(f'\n📋 DATA RESPONDEN:')
    print(f'   Nama              : {nama}')
    print(f'   Usia              : {usia} tahun')
    print(f'   Jenis Kelamin     : {jenis_kelamin}')
    print(f'   Tanggal Pemeriksaan: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    print(f'\n🔍 ANALISIS GEJALA:')
    print(f'   Total gejala yang dilaporkan: {len(gejala)}')
    print(f'   Gejala:')
    for i, g in enumerate(gejala, 1):
        print(f'      {i}. {g}')
    
    print(f'\n⚠️  HASIL DETEKSI:')
    print(f'   Kategori Utama    : {kategori_utama.upper()}')
    print(f'   Deskripsi         : {data_kategori["deskripsi"]}')
    print(f'   Tingkat Risiko    : {data_kategori["tingkat_risiko"]}')
    
    print(f'\n💡 REKOMENDASI TINDAKAN:')
    for i, rekomendasi in enumerate(data_kategori['rekomendasi'], 1):
        print(f'   {i}. {rekomendasi}')
    
    print(f'\n📊 DETAIL ANALISIS KATEGORI:')
    _, hasil_terurut = deteksi_mental(gejala)
    for kategori, data in hasil_terurut[:3]:
        print(f'   • {kategori.upper():15} : {data["persentase"]:.1f}% ({data["jumlah_kecocokan"]} kecocokan)')
    
    print('\n' + '='*70)
    print('⚠️  DISCLAIMER: Program ini bersifat informatif saja.')
    print('Untuk diagnosis akurat, silakan konsultasi dengan profesional kesehatan mental.')
    print('='*70)

def tambah_pemeriksaan():
    """Menambahkan pemeriksaan baru"""
    print('\n' + '='*60)
    print('PEMERIKSAAN KESEHATAN MENTAL BARU')
    print('='*60)
    
    # Input data pribadi
    nama = input('\nNama Lengkap                : ').strip()
    if not nama:
        print('⚠ Nama tidak boleh kosong.')
        return
    
    try:
        usia = int(input('Usia (tahun)              : ').strip())
        if usia < 0 or usia > 150:
            print('⚠ Usia tidak valid. Silakan masukkan usia antara 0-150.')
            return
    except ValueError:
        print('⚠ Usia harus berupa angka.')
        return
    
    print('Jenis Kelamin             : ')
    print('  1. Laki-laki')
    print('  2. Perempuan')
    pilihan_jk = input('Pilih (1/2): ').strip()
    
    jenis_kelamin = 'Laki-laki' if pilihan_jk == '1' else 'Perempuan'
    if pilihan_jk not in ['1', '2']:
        print('⚠ Pilihan tidak valid.')
        return
    
    # Input gejala
    gejala = input_gejala()
    
    if not gejala:
        print('⚠ Gejala tidak boleh kosong.')
        return
    
    # Deteksi kondisi mental
    kategori_utama, hasil_deteksi = deteksi_mental(gejala)
    
    # Tampilkan hasil
    tampilkan_hasil_deteksi(nama, usia, jenis_kelamin, gejala, kategori_utama)
    
    # Simpan data
    data = load_data()
    pemeriksaan_baru = {
        'id': len(data) + 1,
        'nama': nama,
        'usia': usia,
        'jenis_kelamin': jenis_kelamin,
        'gejala': gejala,
        'kategori_utama': kategori_utama,
        'tanggal_pemeriksaan': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    data.append(pemeriksaan_baru)
    save_data(data)

def lihat_riwayat():
    """Melihat riwayat pemeriksaan"""
    data = load_data()
    
    if not data:
        print('\n⚠ Belum ada riwayat pemeriksaan.')
        return
    
    print('\n' + '='*80)
    print('RIWAYAT PEMERIKSAAN KESEHATAN MENTAL')
    print('='*80)
    
    for pemeriksaan in data:
        print(f'\nID: {pemeriksaan["id"]}')
        print(f'├─ Nama              : {pemeriksaan["nama"]}')
        print(f'├─ Usia              : {pemeriksaan["usia"]} tahun')
        print(f'├─ Jenis Kelamin     : {pemeriksaan["jenis_kelamin"]}')
        print(f'├─ Kategori          : {pemeriksaan["kategori_utama"].upper()}')
        print(f'├─ Tanggal           : {pemeriksaan["tanggal_pemeriksaan"]}')
        print(f'└─ Gejala ({len(pemeriksaan["gejala"])}) :')
        for gejala in pemeriksaan['gejala']:
            print(f'   • {gejala}')
        print('-' * 80)

def cari_pemeriksaan():
    """Mencari pemeriksaan berdasarkan nama"""
    nama = input('\nCari berdasarkan nama: ').strip().lower()
    data = load_data()
    
    hasil = [p for p in data if nama in p['nama'].lower()]
    
    if not hasil:
        print(f'\n⚠ Tidak ada pemeriksaan untuk "{nama}".')
        return
    
    print(f'\n✓ Ditemukan {len(hasil)} hasil:')
    print('='*80)
    
    for pemeriksaan in hasil:
        print(f'\nID: {pemeriksaan["id"]}')
        print(f'├─ Nama              : {pemeriksaan["nama"]}')
        print(f'├─ Usia              : {pemeriksaan["usia"]} tahun')
        print(f'├─ Jenis Kelamin     : {pemeriksaan["jenis_kelamin"]}')
        print(f'├─ Kategori          : {pemeriksaan["kategori_utama"].upper()}')
        print(f'├─ Tanggal           : {pemeriksaan["tanggal_pemeriksaan"]}')
        print(f'└─ Gejala ({len(pemeriksaan["gejala"])}) :')
        for gejala in pemeriksaan['gejala']:
            print(f'   • {gejala}')
        print('-' * 80)

def hapus_pemeriksaan():
    """Menghapus pemeriksaan berdasarkan ID"""
    lihat_riwayat()
    
    try:
        id_hapus = int(input('\nMasukkan ID pemeriksaan yang ingin dihapus: ').strip())
        data = load_data()
        
        pemeriksaan = next((p for p in data if p['id'] == id_hapus), None)
        if not pemeriksaan:
            print('⚠ ID tidak ditemukan.')
            return
        
        konfirmasi = input(f'Yakin hapus pemeriksaan "{pemeriksaan["nama"]}"? (y/n): ').lower()
        if konfirmasi == 'y':
            data = [p for p in data if p['id'] != id_hapus]
            save_data(data)
            print('✓ Pemeriksaan berhasil dihapus.')
        else:
            print('✗ Penghapusan dibatalkan.')
    
    except ValueError:
        print('⚠ ID harus berupa angka.')

def menu_utama():
    """Menampilkan menu utama"""
    while True:
        print('\n' + '='*60)
        print('APLIKASI DETEKSI KESEHATAN MENTAL')
        print('='*60)
        print('\n1. Pemeriksaan Kesehatan Mental Baru')
        print('2. Lihat Riwayat Pemeriksaan')
        print('3. Cari Pemeriksaan')
        print('4. Hapus Pemeriksaan')
        print('5. Keluar')
        print('='*60)
        
        pilihan = input('\nPilih menu (1-5): ').strip()
        
        if pilihan == '1':
            tambah_pemeriksaan()
        elif pilihan == '2':
            lihat_riwayat()
        elif pilihan == '3':
            cari_pemeriksaan()
        elif pilihan == '4':
            hapus_pemeriksaan()
        elif pilihan == '5':
            print('\n👋 Terima kasih telah menggunakan aplikasi ini.')
            print('Semoga Anda selalu menjaga kesehatan mental!')
            break
        else:
            print('\n⚠ Pilihan tidak valid. Silakan pilih 1-5.')

if __name__ == '__main__':
    menu_utama()
