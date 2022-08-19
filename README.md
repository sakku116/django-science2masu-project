# django-science2masu-app

Sebuah aplikasi django untuk profil kelas mipa2 alumni 2022 sebagai kenangan dari kelas kami di Madrasah Silahul Ulum.

## Deployment
Web app ini telah dikonfigurasi untuk dideploy menggunakan heroku.
dan membutuhkan beberapa file untuk konfigurasi deploy ke heroku seperti
[runtime.txt](/runtime.txt), [Procfile](/Procfile), [requirements.txt](/requirements.txt).
Dan juga beberapa library python seperti '*django-heroku*', dan mungkin masih ada library yang dibutuhkan lainnya yang dibutuhkan untuk deploy di heroku.

## Struktur App
- **science2masu** (base direktori / direktori ini)
    - **root app** (folder '[./root_app](./root_app)')

        *lihat file [.root_app/urls.py](.root_app/urls.py) untuk melihat routing.*

    - **api app** (folder '[./api_app](./api_app)')

        *lihat file [.api_app/urls.py](.api_app/urls.py) untuk melihat routing.*

## Environment variables
Sebagai privasi (terutama untuk membuat repositori ini menjadi publik), proyek ini menggunakan '*environment variables*'

variabel variable tersebut terdiri dari
```
PRODUCTION=([1] or [0]. default = [0] (tidak di lingkungan production))

# timezone
TZ=(e.g: [Asia/Jakarta])

# tentukan database yang digunakan (local e.g: sqlite3, remote e.g: railway, heroku db)
USE_DATABASE=([local] or [remote]. default = [remote])

# konfigurasi reguler untuk koneksi ke database
DATABASE_CONN_URL=

# variable heroku default untuk koneksi db add-ons pada heroku.
# heroku akan mereset kredensial add-on db tersebut secara berkala.
# tetapi karena add-ons tersebut merupakan bagian dari heroku-app ini (science2masu),
# maka heroku akan memperbarui value dari variabel berikut secara otomatis pada lingkungan deployment (heroku)
# dan perlu memperbarui secara manual pada lingkungan local.
HEROKU_POSTGRESQL_ROSE_URL=(db_auth)

# untuk mengambil file pribadi dari repositori github pribadi
GITHUB_TOKEN=(token generated from github)
GITHUB_PRIVATE_REPO=(username/repo)
GITHUB_LETTER_PATH=(path/to/file.txt)
GITHUB_LETTER_INTRO_PATH=(path/to/file.txt)

# konfigurasi email untuk mengirim notifikasi ke developer saat crushnya log in :D
EMAIL_HOST_USER=(pengirim)
EMAIL_HOST_PASSWORD=(password google apps dari email pengirim)

# karena variabel di django nya mengandung 'secret' maka sebaiknya saya membuatnya pribadi :)
DJANGO_SECRET_KEY=(django required key)

API_KEY=(api authentication)
```

>'*env vars* dapat dideklarasi menggunakan file '*.env*' pada direktori dasar (base dir) untuk deploy di local machine dan untuk mengaksesnya, dapat menggunakan library seperti '*python-dotenv*'.

## Assets
Aplikasi ini menggunakan [statically.io](statically.io) dan [imgix.com](imgix.com) untuk serving asset global terutama file gambar, dan menggunakan repositori publik untuk sumber assetnya. Kunjungi repository [science2masu-static-files](https://github.com/sakku116/science2masu-static-files) (*repository tersebut hanya mengandung **file static global**, bukan untuk file static untuk app tertentu seperti 'static/otherApp'*)

Pola url statically.io:
```
https://cdn.statically.io/gh/:user/:repo/:branch/:path/:file
```
Pola url imgix.com:
```
https://sources-name.imgix.net/:path/:file

(imgix menggunakan konfigurasi untuk koneksi ke sumber assetnya)
```

### Contoh:

'https://cdn.statically.io/gh/sakku116/science2masu-static-files/main/static/images/gallery/others/dev-gitar.png'

Url sebenarnya adalah:

'https://raw.githubusercontent.com/sakku116/science2masu-static-files/main/static/images/gallery/others/dev-gitar.png'

> struktur direktori antara direktori [./static](./static) pada proyek ini dan direktori static dari penyedia file static (imgix.com, statically.io) harus sama, karena file .txt yang mengandung daftar dari url gambar tersimpan di path tersebut pada proyek ini. Sebagai contoh: server penyedia file static external menyimpan gambar1.png dan gambar2.png pada path `static/images`. Maka dari itu url dari file tersebut tersimpan pada file txt pada path `static/images` di proyek ini. Dan kemudian, url url file tersebut akan di konversi ke url *statically.io* atau *imgix.com* (jika dibutuhkan) ketika django merender file html dan mengirimnya melalui django-context untuk halaman yang membutuhkan daftar dari url url dari file tersebut seperti halaman 'index' yang menampilkan foto foto gallery secara static. 

>*Kunjungi [./static/images](./static/images) untuk melihat file `img_url_list.txt`. Saya juga telah membuat script python untuk megenerasi daftar url ke dalam file tersebut secara otomatis (lihat [./utils](./utils))*

## Terimakasih Untuk
* Fitria Noviastuti
    
    Yang telah memberikan beberapa ide dan saran untuk membangun web app ini.

* Sofia Maulidinni'mah
    
    Untuk beberapa file asset.

* Muhammad Hasan Aly

    Untuk beberapa file asset.

* Ahmad Irfanuddin

    Untuk beberapa file asset.

* Dan semua teman teman kelas saya.

    Yang telah membangung kenangan kami semua dan memotivasi saya untuk membuat web app ini.