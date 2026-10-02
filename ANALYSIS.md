Analisis
1. Alasan menggunakan thresholding

Thresholding digunakan untuk memisahkan bagian tanda tangan dari latar belakang kertas. Setelah gambar diubah menjadi grayscale, nilai piksel menjadi lebih sederhana sehingga bagian yang gelap seperti goresan tanda tangan dapat dibedakan dari bagian kertas yang lebih terang.

Hasil threshold kemudian dapat digunakan untuk menghitung jumlah piksel foreground. Nilai tersebut menjadi dasar untuk menentukan apakah pada area yang diperiksa terdapat tanda tangan atau tidak.

2. Perbandingan Global Threshold dan Otsu

Pada Global Threshold, nilai batas ditentukan secara langsung menggunakan nilai tetap, yaitu 180. Piksel dengan intensitas di bawah batas tersebut dianggap sebagai foreground.

Sedangkan pada metode Otsu, nilai threshold ditentukan secara otomatis berdasarkan distribusi intensitas pada gambar. Metode ini digunakan agar batas antara foreground dan background dapat menyesuaikan dengan kondisi gambar.

Dari hasil pengujian, metode Otsu dapat menghasilkan pemisahan tanda tangan dengan baik pada gambar yang memiliki tanda tangan. Untuk kondisi tertentu ketika hasil Otsu menghasilkan jumlah foreground yang tidak sesuai, program menggunakan Global Threshold sebagai fallback.

3. Morphological Operation

Setelah proses thresholding, dilakukan operasi morphology berupa opening dan closing.

Opening digunakan untuk mengurangi titik-titik kecil atau noise yang masih muncul setelah thresholding. Setelah itu, closing digunakan untuk membantu menyambungkan bagian foreground yang memiliki celah kecil.

Dengan proses tersebut, hasil segmentasi menjadi lebih bersih dan bentuk goresan tanda tangan lebih mudah digunakan untuk proses perhitungan.

4. Analisis Foreground Ratio

Program menghitung persentase piksel foreground terhadap seluruh piksel pada area tanda tangan menggunakan rumus:

Foreground Ratio = jumlah piksel foreground / jumlah seluruh piksel

Jika nilai ratio memenuhi batas yang telah ditentukan, yaitu 0,03, maka gambar dikategorikan sebagai:

SIGNATURE PRESENT

Jika nilainya berada di bawah batas tersebut, maka dikategorikan sebagai:

SIGNATURE ABSENT

Pada data pengujian, gambar yang memiliki tanda tangan menghasilkan ratio sekitar 0,0872 sampai 0,1358, sedangkan gambar tanpa tanda tangan menghasilkan ratio 0,0000.

5. Pengaruh Nilai Threshold

Jika nilai threshold terlalu tinggi, lebih banyak bagian background dapat ikut dianggap sebagai foreground. Hal ini dapat membuat jumlah piksel foreground menjadi terlalu besar dan berpotensi menyebabkan gambar tanpa tanda tangan dianggap memiliki tanda tangan.

Sebaliknya, jika nilai threshold terlalu rendah, goresan tanda tangan yang tipis atau kurang gelap dapat tidak terdeteksi. Akibatnya jumlah foreground menjadi terlalu sedikit dan gambar yang sebenarnya memiliki tanda tangan dapat dianggap tidak memiliki tanda tangan.

Oleh karena itu, pemilihan threshold berpengaruh terhadap hasil segmentasi dan keputusan akhir sistem.

6. Hasil Pengujian

Pengujian dilakukan menggunakan 18 gambar, terdiri dari 9 gambar dengan tanda tangan dan 9 gambar tanpa tanda tangan.

Hasil pengujian menunjukkan:

9 gambar SIGNATURE PRESENT berhasil dikenali sebagai SIGNATURE PRESENT.
9 gambar SIGNATURE ABSENT berhasil dikenali sebagai SIGNATURE ABSENT.
Jumlah prediksi benar: 18 dari 18 gambar.
Accuracy: 100%.
7. Kesimpulan Analisis

Berdasarkan hasil pengujian, kombinasi grayscale, thresholding, morphology, dan perhitungan foreground ratio dapat digunakan untuk mendeteksi keberadaan tanda tangan pada area yang telah ditentukan. Perbandingan Global Threshold dan Otsu juga membantu memilih hasil segmentasi yang sesuai dengan kondisi gambar. Pada dataset yang digunakan, seluruh gambar berhasil diklasifikasikan dengan benar.