# LAPORAN PROGRESS REPORT - MINGGU 1
## PROYEK TUGAS BESAR ALGORITMA DAN PEMROGRAMAN

---

### I. IDENTITAS MAHASISWA DAN PROYEK
* Nama Anggota:
  1. Julius Santoso Setiawan (NRP: 2472051)
  2. Francisco Valentino (NRP: 2472040)
  3. Teofilus Juan Puapadang (NRP: 2472053)
* Topik Proyek: Pemilihan Tim Proyek dengan Algoritma Branch and Bound
* Bahasa Pemrograman: Python 3

---

### II. RINGKASAN TOPIK
Proyek ini bertujuan untuk membangun aplikasi pemilihan tim proyek optimal dengan menyeleksi kombinasi k kandidat dari pool n kandidat (n >= 12, 5 <= k <= 10) sedemikian rupa sehingga total biaya minimum dan tidak melebihi anggaran B. Solusi optimal dicapai dengan menerapkan metode Branch and Bound melalui penelusuran Depth-First Search yang diperkuat dengan teknik pemangkasan cabang (pruning) menggunakan perhitungan batas bawah (lower bound) biaya.

---

### III. YANG SUDAH DIKERJAKAN
Seluruh komponen dasar algoritma dan model data untuk Minggu 1 telah selesai dikerjakan dengan rincian sebagai berikut:

1. Pembuatan Model Data
   * Deskripsi: Merancang model Candidate untuk representasi peserta, BBNode untuk simpul pohon keputusan B&B, dan SolveResult sebagai objek penampung hasil pencarian.
   * Berkas Kode: [models.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/models.py)
   * Status: Selesai

2. Implementasi Algoritma Branch and Bound
   * Deskripsi: Menyusun kelas BranchAndBound dengan penelusuran DFS dan evaluasi batas bawah dinamis (biaya tim saat ini ditambah akumulasi biaya minimum kandidat yang tersisa) untuk memangkas cabang non-optimal. Algoritma juga dilengkapi dengan kemampuan merelaksasi kondisi pemangkasan (menggunakan batas ketat, lb > best_cost) agar mampu menemukan seluruh kombinasi tim optimal yang berbiaya setara.
   * Berkas Kode: [algorithm.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/algorithm.py)
   * Status: Selesai

3. Fitur Pencarian Tim Alternatif Optimal
   * Deskripsi: Mengimplementasikan fungsionalitas pencarian seluruh kombinasi tim yang memiliki biaya minimum yang sama (solusi alternatif setara). Fitur ini memungkinkan pengguna untuk melihat semua opsi tim yang tersedia pada titik biaya optimal, bukan hanya satu solusi tunggal. Diimplementasikan melalui metode get_alternative_teams pada kelas BranchAndBound.
   * Berkas Kode: [algorithm.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/algorithm.py), [main_minggu1.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/main_minggu1.py)
   * Status: Selesai

4. Fitur Pelacak Pohon Pencarian B&B Berbasis Teks (ASCII Tree Tracer)
   * Deskripsi: Membuat fungsi visualisasi pohon pencarian Branch and Bound dalam format teks ASCII terstruktur di terminal. Setiap simpul pada pohon menampilkan label tim yang dipilih, akumulasi biaya saat ini, nilai batas bawah (Lower Bound), serta status simpul (AKTIF, DIPANGKAS, atau SOLUSI OPTIMAL). Fitur ini membuktikan secara visual bahwa proses penelusuran dan pemangkasan cabang berjalan sesuai dengan logika algoritma.
   * Berkas Kode: [main_minggu1.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/main_minggu1.py)
   * Status: Selesai

5. Pengujian Unit (Unit Testing)
   * Deskripsi: Membuat skrip testing otomatis yang mencakup 6 skenario pengujian guna memvalidasi akurasi perhitungan optimal, penanganan kasus tanpa solusi valid, pengujian anggaran ketat, performa efisiensi pemangkasan node, serta verifikasi deteksi tim alternatif optimal.
   * Berkas Kode: [test_algorithm.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/test_algorithm.py)
   * Status: Selesai

6. Demo Aplikasi Awal
   * Deskripsi: Membuat berkas eksekusi demo yang menyimulasikan pemilihan 5 orang dari pool 12 kandidat dengan batas anggaran Rp 100.000.000, menampilkan tim terpilih, ringkasan proses B&B, daftar tim alternatif optimal, dan visualisasi pohon pencarian ASCII secara otomatis melalui terminal.
   * Berkas Kode: [main_minggu1.py](file:///c:/Semester%204/Strago/Tubes/Tubes%20M1/main_minggu1.py)
   * Status: Selesai

Persentase Kemajuan Proyek pada Minggu 1: 25% dari total keseluruhan proyek.

---

### IV. YANG AKAN DIKERJAKAN
Untuk kelanjutan pengerjaan pada Minggu 2, fokus pengembangan diarahkan pada pembuatan antarmuka pengguna interaktif dan penyimpanan data kandidat dengan rincian prioritas sebagai berikut:

1. Perancangan Antarmuka Pengguna CLI
   * Deskripsi: Membangun terminal antarmuka pengguna berbasis teks (CLI) yang informatif dan terstruktur dengan menggunakan pustaka Rich.
   * Prioritas: Tinggi
   * Estimasi Waktu: 4 Hari

2. Pembuatan Fitur Validasi Masukan
   * Deskripsi: Menyusun modul penangan masukan pengguna untuk mencegah kesalahan pengisian tipe data dan rentang nilai parameter (n, k, B).
   * Prioritas: Tinggi
   * Estimasi Waktu: 2 Hari

3. Pembuatan Fitur Manajemen Data JSON
   * Deskripsi: Mengimplementasikan modul untuk menyimpan pool data kandidat ke berkas eksternal berformat JSON dan memuatnya kembali secara dinamis.
   * Prioritas: Sedang
   * Estimasi Waktu: 3 Hari

---

### V. PANDUAN PENGOPERASIAN APLIKASI
Berkas program Minggu 1 dapat dijalankan secara langsung melalui terminal dengan mengikuti langkah-langkah berikut:

1. Pastikan Anda berada di direktori Tubes M1:
   ```bash
   cd "c:\Semester 4\Strago\Tubes\Tubes M1"
   ```

2. Jalankan program demo utama:
   ```bash
   python main_minggu1.py
   ```
