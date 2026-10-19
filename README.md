# Studi Kasus: Dashboard Berbasis User Persona + Audit Kontras WCAG

Berdasarkan kuliah umum **"Human-Computer Interaction & Data Visualization"** oleh **Dr. Arafat Febriandirza** (BRIN).

Satu dataset penjualan **sintetis** (4 kategori x 3 wilayah x 12 bulan) disajikan dalam **tiga tampilan berbeda**
untuk tiga persona, sehingga terlihat bagaimana kebutuhan pengguna membentuk keputusan desain.

## Hubungan dengan materi

| Poin materi | Implementasi |
|---|---|
| User-Centered Design ("pengguna bukanlah Anda") | Tiga persona dengan tujuan, kendala, dan skenario berbeda |
| User Persona | Kartu persona di tiap tampilan (**asumsi**, bukan riset empiris) |
| 5 prinsip: visibility, feedback, constraints, consistency, affordance | Kartu "Kenapa tampilan ini dirancang begini?" memetakan tiap keputusan ke prinsipnya |
| Beban kognitif dan preattentive attributes | Tampilan manajer: 1 kontrol, 3 angka kunci, 1 grafik, peringatan berwarna |
| Gestalt (proximity, enclosure) | Label seri di ujung garis; elemen dikelompokkan dalam kartu |
| Visualisasi interaktif, filter real-time | Tampilan analis: filter kategori/wilayah memperbarui grafik, kartu, dan tabel seketika |
| Aksesibilitas WCAG (POUR) | Tampilan pengguna tua: teks besar, kontras tinggi, tombol besar, bahasa sederhana |
| Etika desain: hindari manipulasi skala | Semua sumbu dimulai dari nol |

## Audit kontras

`persona_dashboard.py` menghitung rasio kontras palet dengan rumus WCAG 2.x. Hasil: semua teks lolos AA, kebanyakan AAA.
Isi batang berwarna terang **gagal 3:1** terhadap latar putih, sehingga setiap batang diberi garis tepi hitam dan label langsung
agar informasi tidak hanya bergantung pada warna.

## Cara menjalankan

```bash
python persona_dashboard.py    
```

link index.html  https://krbara.github.io/studi-kasus-persona-dashboard/

## Catatan penting

- **Persona adalah asumsi awal.** Materi menekankan persona dari riset empiris, jadi langkah berikutnya adalah
  validasi lewat wawancara atau survei pengguna.
- Audit otomatis hanya memeriksa kontras warna, bukan seluruh aspek aksesibilitas. Uji dengan pengguna dan pembaca layar tetap perlu.
- Data sintetis; pola penurunan "Camilan" sengaja ditanam agar ada cerita yang bisa disorot.
- Belum ada evaluasi dengan pengguna nyata (tahap evaluasi pada siklus desain interaksi).
