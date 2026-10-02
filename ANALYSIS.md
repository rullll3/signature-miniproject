# Analisis Mini Project

## 1. Crop dan grayscale

ROI tanda tangan Dekan menggunakan koordinat:

```text
x1=950, y1=770, x2=1350, y2=875
```

Ukuran ROI = `400 x 105` piksel.

ROI kemudian dikonversi dari RGB/BGR ke grayscale agar proses thresholding
bekerja pada satu kanal intensitas.

## 2. Perbandingan thresholding

### Global threshold

Digunakan nilai tetap `T=180`.

Kelebihan: sederhana dan cepat.

Kekurangan: sensitif terhadap perubahan pencahayaan. Pada salah satu citra
yang jauh lebih gelap, background ikut terdeteksi sebagai foreground dalam
jumlah sangat besar.

### Otsu threshold

Otsu menentukan nilai threshold otomatis dari histogram grayscale. Pada citra
dengan pencahayaan yang berbeda-beda, metode ini lebih adaptif daripada nilai
global tetap.

Contoh threshold Otsu pada data yang diuji berada sekitar `126-202` untuk
citra bertanda tangan.

## 3. Morphology

Urutan yang digunakan:

```text
threshold -> opening -> closing
```

- Opening menghilangkan noise kecil/komponen kecil.
- Closing menutup celah kecil pada goresan sehingga bentuk tanda tangan lebih
  utuh.

Kernel yang digunakan adalah elliptical `3x3`.

## 4. Karakteristik area

Karakteristik utama yang dihitung adalah:

```text
foreground_pixels = jumlah piksel bernilai 255
foreground_ratio = foreground_pixels / jumlah seluruh piksel ROI
```

Pada contoh citra bertanda tangan, rasio foreground setelah Otsu + morphology
berada sekitar 0.09-0.13.

Aturan sederhana:

```text
foreground_ratio >= 0.03 -> SIGNATURE PRESENT
foreground_ratio <  0.03 -> SIGNATURE ABSENT
```

Nilai `0.03` dipilih sebagai threshold eksperimen untuk ROI yang digunakan.
Jika ukuran crop, kualitas scanner, atau jenis dokumen berubah, nilai ini perlu
dikaji ulang.

## 5. Masalah Otsu pada ROI kosong

Pada ROI yang hampir seragam, Otsu dapat menghasilkan threshold sangat tinggi.
Jika binary inverse digunakan, background yang seragam dapat salah dianggap
sebagai foreground.

Karena itu implementasi memakai pemeriksaan kewajaran hasil Otsu. Jika threshold
Otsu terlalu tinggi atau foreground hasil Otsu terlalu besar, program memakai
global threshold sebagai fallback.

Ini penting karena "tidak ada tanda tangan" tidak selalu berarti histogram
memiliki dua kelompok intensitas yang jelas.

## 6. Jawaban pertanyaan analisis

### Mengapa thresholding diperlukan sebelum analisis keberadaan tanda tangan?

Karena jumlah piksel tinta dan bentuk tanda tangan lebih mudah dianalisis pada
citra biner. Thresholding memisahkan piksel gelap yang merepresentasikan tinta
dari background kertas yang relatif terang. Hasilnya dapat dihitung secara
kuantitatif menggunakan foreground pixel count atau foreground ratio.

### Apa masalah jika threshold terlalu tinggi?

Background, bayangan, tekstur kertas, atau noise dapat ikut menjadi foreground.
Akibatnya area foreground membesar dan sistem dapat memberikan false positive.

### Apa masalah jika threshold terlalu rendah?

Goresan tanda tangan yang tipis/abu-abu dapat hilang. Area foreground menjadi
terlalu kecil sehingga sistem dapat memberikan false negative.

## 7. Pengujian

Dataset contoh:

| Kelas | Jumlah | Sumber |
|---|---:|---|
| SIGNATURE PRESENT | 5 | citra yang diberikan |
| SIGNATURE ABSENT | 4 | negative sample sintetis |

Negative sample sintetis dibuat dengan menutupi ROI tanda tangan. Untuk laporan
akademik, jelaskan hal ini secara eksplisit dan, jika memungkinkan, tambahkan
beberapa scan asli tanpa tanda tangan sebelum menyatakan performa final sistem.

## 8. Tabel hasil pengujian

| file          | expected          | prediction        |   otsu_threshold |   global_foreground |   otsu_foreground |   selected_foreground |   selected_ratio |
|:--------------|:------------------|:------------------|-----------------:|--------------------:|------------------:|----------------------:|-----------------:|
| absent_1.jpg  | SIGNATURE ABSENT  | SIGNATURE ABSENT  |              247 |                   0 |             41495 |                     0 |           0      |
| absent_2.jpg  | SIGNATURE ABSENT  | SIGNATURE ABSENT  |              244 |                   0 |             41499 |                     0 |           0      |
| absent_3.jpg  | SIGNATURE ABSENT  | SIGNATURE ABSENT  |              247 |                   0 |             41395 |                     0 |           0      |
| absent_4.jpg  | SIGNATURE ABSENT  | SIGNATURE ABSENT  |              190 |                   0 |             41494 |                     0 |           0      |
| present_1.jpg | SIGNATURE PRESENT | SIGNATURE PRESENT |              165 |                4340 |              3771 |                  3771 |           0.0898 |
| present_2.jpg | SIGNATURE PRESENT | SIGNATURE PRESENT |              195 |                4519 |              5608 |                  5608 |           0.1335 |
| present_3.jpg | SIGNATURE PRESENT | SIGNATURE PRESENT |              126 |               42000 |              3862 |                  3862 |           0.092  |
| present_4.jpg | SIGNATURE PRESENT | SIGNATURE PRESENT |              170 |                4234 |              3775 |                  3775 |           0.0899 |
| present_5.jpg | SIGNATURE PRESENT | SIGNATURE PRESENT |              145 |                7292 |              4228 |                  4228 |           0.1007 |

Pada dataset contoh ini seluruh 9 sampel diklasifikasikan dengan benar (100%). Angka tersebut berlaku hanya untuk dataset mini yang digunakan dan tidak merepresentasikan performa pada dokumen dengan layout, pencahayaan, atau kualitas scan yang berbeda.
