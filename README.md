# Smart-Cargo-and-Order-Management-System

## İçerik Tablosu
- [Hakkında](#hakkında)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
  - [Kaydol / Giriş Yap](#kaydol--giriş-yap)
  - [Müşteri Menüsü](#müşteri-menüsü)
  - [Yönetici Menüsü](#yönetici-menüsü)
- [Kullanılan Tasarım Desenleri](#kullanılan-tasarım-desenleri)
- [Dosya Yapısı](#dosya-yapısı)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Hakkında
Bu proje, çeşitli Nesne Yönelimli Programlama (OOP) prensiplerini ve tasarım desenlerini kullanarak geliştirilmiş bir e-ticaret uygulamasıdır. Kullanıcıların ürünlere göz atabildiği, sepete ekleyebildiği, sipariş verebildiği ve sipariş durumlarını takip edebildiği temel bir çevrimiçi mağaza simülasyonu sunar. Yöneticiler ise ürün yönetimi ve sipariş denetimi gibi ek işlevlere sahiptir. Uygulama, kullanıcı ve ürün verileri için SQLite veritabanlarıyla etkileşim kurar.

## Özellikler
-   **Kullanıcı Kimlik Doğrulama:**
    -   Yeni kullanıcı kaydı (Kaydol)
    -   Mevcut kullanıcı girişi (Giriş Yap)
    -   Rol tabanlı erişim (Müşteri ve Yönetici)
-   **Ürün Yönetimi (Yönetici Rolü):**
    -   Yeni ürün ekleme (Kitaplar, Elektronik)
    -   Tüm ürünleri listeleme
    -   Kategoriye göre ürünleri listeleme
    -   Ürün stoğunu güncelleme
    -   Ürün stok bilgisini alma
-   **Alışveriş Sepeti (Müşteri Rolü):**
    -   Ürünleri sepete ekleme
    -   Sepet içeriğini görüntüleme
    -   Sepetin boş olup olmadığını kontrol etme
    -   Sepeti temizleme
    -   Sepetteki toplam ürün sayısını alma
-   **Sipariş Yönetimi:**
    -   Sepetten yeni sipariş oluşturma
    -   Sipariş geçmişini görüntüleme
    -   Sipariş durumunu güncelleme (Yönetici)
    -   Otomatik bildirim için Observer deseni kullanılarak sipariş durumu değişiklikleri için bildirimler
-   **Bildirimler:**
    -   E-posta ve SMS bildirim simülasyonu
    -   Sipariş durumu bildirimleri için Observer deseni
-   **Veritabanı Entegrasyonu:**
    -   Kullanıcı ve ürün verilerini depolamak için SQLite kullanır.
-   **Hata Yönetimi:**
    -   Veritabanı işlemleri ve kullanıcı girişleri için temel hata yönetimi.

## Kurulum

Projeyi kurmak için aşağıdaki adımları izleyin:

1.  **Depoyu klonlayın:**
    ```bash
    git clone <depo_url'si>
    cd OOP-Store
    ```


3.  **Bağımlılıkları yükleyin:**
    Bu proje öncelikli olarak Python'ın yerleşik modülü olan `sqlite3`'ü kullanır. Çekirdek işlevsellik için başka harici kütüphaneler zorunlu değildir.

4.  **Veritabanlarını başlatın:**
    Uygulama, ilk çalıştırmada `users.db` ve `store.db` dosyalarını otomatik olarak oluşturacaktır.
    -   `users.db`: Kullanıcı kimlik doğrulama bilgilerini (kullanıcı adı, parola, rol) depolar.
    -   `store.db`: Ürün bilgilerini (ID, ad, kategori, stok, fiyat, yazar, yayınevi, garanti) depolar.

## Kullanım

Uygulamayı çalıştırmak için `main.py` dosyasını çalıştırın:

```bash
python main.py