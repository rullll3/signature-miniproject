Mini Project: Signature Presence Detection

Program ini digunakan untuk mendeteksi apakah area tanda tangan Dekan pada ijazah terdapat tanda tangan atau tidak.

Proses pengolahan yang dilakukan:

Crop area tanda tangan pada citra.
Mengubah citra menjadi grayscale.
Melakukan global threshold dengan T = 180 dan Otsu threshold.
Membandingkan hasil kedua thresholding.
Menggunakan opening untuk mengurangi noise dan closing untuk menutup celah pada tanda tangan.
Menghitung jumlah piksel foreground dan foreground ratio.
Menentukan hasil berdasarkan aturan:
ratio >= 0.03 → SIGNATURE PRESENT
ratio < 0.03 → SIGNATURE ABSENT
Jika hasil Otsu tidak sesuai, program menggunakan global threshold sebagai fallback.

Program diuji menggunakan 9 citra, yaitu 5 citra dengan tanda tangan dan 4 citra tanpa tanda tangan. Hasil pengujian menunjukkan 9 dari 9 citra berhasil diklasifikasikan dengan benar.

Thresholding digunakan untuk memisahkan tanda tangan dari background sehingga area tanda tangan dapat dihitung. Threshold yang terlalu tinggi dapat membuat background ikut terdeteksi, sedangkan threshold terlalu rendah dapat membuat bagian tanda tangan hilang.

Cara Menjalankan

Install library: pip install -r requirements.txt

Jalankan program: python run.py
Hasilnya akan muncul di terminal dan tersimpan di folder outputs dalam bentuk results.csv dan comparison.png.