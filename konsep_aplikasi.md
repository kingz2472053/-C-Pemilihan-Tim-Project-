# Konsep Utama Aplikasi Pemilihan Tim Proyek (Branch & Bound)

Dokumen ini menjelaskan konsep dasar aplikasi dengan dua pendekatan: **Ringkasan Singkat** (untuk pemahaman cepat) dan **Penjelasan Detail** (untuk kebutuhan teknis mendalam).

---

## BAGIAN 1: RINGKASAN CEPAT (Sangat Singkat & Jelas)

### Apa itu Aplikasi ini?
Sebuah sistem untuk memilih **$k$ orang anggota tim** dari **$n$ pilihan kandidat** dengan **total biaya termurah**, tetapi **tidak boleh melebihi anggaran $B$**.

### Bagaimana Cara Kerjanya? (Analogi Belanja Pintar)
Bayangkan Anda ingin membeli **5 barang ($k=5$)** dengan uang maksimal **Rp 100 juta ($B=100\text{jt}$)**, dan ingin total belanjaan Anda **semurah mungkin**.

Daripada mencoba seluruh kombinasi acak barang yang melelahkan (**Brute Force**), kita memakai **Branch and Bound**:
1. **Urutkan barang dari yang termurah**: Kita susun semua barang di rak dari harga terendah ke tertinggi.
2. **Hitung Batas Bawah (Lower Bound)**: Sebelum mengambil keputusan lebih jauh, kita hitung: *"Jika saya lanjut memilih barang termurah yang tersisa, berapa minimal uang yang akan saya habiskan?"*
3. **Pangkas Pilihan (Pruning)**:
   - Jika estimasi harga termurah itu sudah **melebihi anggaran (Rp 100jt)**, jangan teruskan memilih kombinasi tersebut. **Pangkas!**
   - Jika estimasi harga termurah itu ternyata **lebih mahal dari kombinasi 5 barang termurah yang sudah kita temukan sebelumnya**, jangan teruskan. **Pangkas!**

Dengan cara ini, komputer tidak perlu memeriksa jutaan kombinasi tidak berguna, sehingga program berjalan **instan (di bawah 1 milidetik)**.

---

## BAGIAN 2: PENJELASAN TEKNIS MENDALAM (Detail & Komprehensif)

### 1. Formulasi Masalah Matematis
Secara formal, masalah seleksi tim proyek ini dimodelkan sebagai berikut:

* Diberikan himpunan kandidat $C = \{c_1, c_2, \dots, c_n\}$, di mana setiap kandidat memiliki indeks $i$ dan biaya $\text{cost}(c_i)$.
* Kita ingin menentukan subset biner $X = \{x_1, x_2, \dots, x_n\}$ dengan $x_i \in \{0, 1\}$.
  * $x_i = 1$ jika kandidat $c_i$ dipilih masuk ke dalam tim.
  * $x_i = 0$ jika kandidat $c_i$ tidak dipilih.

$$\text{Minimumkan } \sum_{i=1}^{n} \text{cost}(c_i) \cdot x_i$$

Dengan kendala (*Constraints*):
1. **Ukuran Tim**: $\sum_{i=1}^{n} x_i = k$ (tim harus beranggotakan tepat $k$ orang).
2. **Batas Anggaran**: $\sum_{i=1}^{n} \text{cost}(c_i) \cdot x_i \le B$ (total biaya tidak boleh melebihi budget $B$).

---

### 2. Struktur Data State Space Tree (`models.py`)
Pencarian dilakukan dengan menelusuri **Pohon Ruang Status (State Space Tree)** secara Depth-First Search (DFS).
* **Node Root**: Melambangkan kondisi awal saat belum ada kandidat yang dipilih (tim masih kosong).
* **Node Level $d$**: Melambangkan kondisi di mana kita telah memilih $d$ kandidat ke dalam tim.
* **Cabang (Edge)**: Melambangkan keputusan untuk menyertakan kandidat tertentu ke dalam tim pada level berikutnya.

Setiap node diwakili oleh struktur data [BBNode](file:///c:/Semester%204/Strago/Tubes/-C-Pemilihan-Tim-Project--main/-C-Pemilihan-Tim-Project--main/Progress%20minggu%203/models.py#L17) yang menyimpan:
* `selected`: Daftar indeks kandidat yang telah dipilih.
* `total_cost`: Total biaya riil dari kandidat yang telah dipilih di node tersebut.
* `lower_bound`: Estimasi biaya minimum teoretis jika kita melanjutkan pencarian dari node tersebut.

---

### 3. Logika Branch and Bound (`algorithm.py`)

#### A. Efek Pengurutan Biaya (Ascending Sorting)
Pada tahap inisialisasi, kandidat diurutkan:
$$\text{cost}(c_1) \le \text{cost}(c_2) \le \dots \le \text{cost}(c_n)$$
Pengurutan ini sangat penting karena:
1. Memastikan pencarian DFS menemukan solusi dengan biaya rendah terlebih dahulu di awal pencarian, sehingga nilai variabel global `best_cost` cepat mengecil.
2. Membantu memberikan estimasi nilai *Lower Bound* yang valid karena sisa kandidat di sebelah kanan selalu memiliki harga yang lebih mahal atau sama dengan kandidat saat ini.

#### B. Rumus Perhitungan Batas Bawah (Lower Bound)
Ketika program berada pada suatu node dengan daftar kandidat terpilih `selected` dan level pencarian saat ini adalah `level`, jumlah slot tim yang masih kosong adalah:
$$\text{needed} = k - |\text{selected}|$$

Jika $\text{needed} > 0$, batas bawah teoretis ($LB$) dihitung dengan menjumlahkan total biaya saat ini ditambah biaya dari $\text{needed}$ kandidat termurah yang masih tersedia di sisa pool:
$$LB = \sum_{j \in \text{selected}} \text{cost}(c_j) + \sum_{p=1}^{\text{needed}} \text{cost}(c_{\text{indeks\_termurah} + p - 1)}$$

**Contoh Kasus**:
* Kita ingin membuat tim berukuran $k=3$.
* Pool kandidat setelah diurutkan: $A (10\text{jt}), B (20\text{jt}), C (30\text{jt}), D (40\text{jt}), E (50\text{jt})$.
* Di node saat ini, kita sudah memilih kandidat **B** (biaya riil = 20jt). Kita butuh **2** orang lagi ($\text{needed} = 2$) dari pilihan yang tersisa yaitu $\{C, D, E\}$.
* Kandidat termurah yang tersisa adalah $C$ dan $D$. Maka:
  $$LB = 20\text{jt} + (\text{biaya } C + \text{biaya } D) = 20\text{jt} + (30\text{jt} + 40\text{jt}) = 90\text{jt}$$
* Artinya, solusi terbaik apa pun yang ditelusuri dari cabang ini **tidak akan pernah lebih murah dari Rp 90 juta**.

#### C. Aturan Pemangkasan Cabang (Pruning Rules)
Selama penelusuran DFS, sebuah cabang node akan dipangkas jika:
1. **Constraint Feasibility (Sisa Slot)**: Sisa kandidat di pool tidak mencukupi untuk memenuhi target tim $k$.
   $$\text{sisa\_kandidat} < \text{needed}$$
2. **Constraint Budget**: Batas bawah biaya lebih besar dari anggaran yang dimiliki.
   $$LB > B$$
3. **Optimality (Bound Check)**: Batas bawah biaya sudah lebih besar atau sama dengan biaya tim terbaik yang telah ditemukan sebelumnya.
   $$LB \ge \text{best\_cost}$$

Dengan menerapkan ketiga aturan pemangkasan ini, algoritma dapat menghindari eksplorasi miliaran kombinasi tidak layak, menyusutkan ukuran pohon keputusan, dan menyelesaikan optimasi secara instan.
