# Smart-Cargo-and-Order-Management-System

## Hakkında
Bu proje, çeşitli Nesne Yönelimli Programlama (OOP) prensiplerini ve tasarım desenlerini kullanarak geliştirilmiş akıllı kargo ve sipariş yönetim sistemi uygulamasıdır. Kullanıcıların ürünlere göz atabildiği, sepete ekleyebildiği, sipariş verebildiği ve sipariş durumlarını takip edebildiği temel bir çevrimiçi mağaza simülasyonu sunar. Yöneticiler ise ürün yönetimi ve sipariş denetimi gibi ek işlevlere sahiptir. Uygulama, kullanıcı ve ürün verileri için SQLite veritabanlarıyla etkileşim kurar.

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
-   **Alışveriş (Müşteri Rolü):**
    -   Ürünleri görüntüleme
    -   Kategorilere göre ürünleri görüntüleme
    -   Sipariş oluşturma
    -   Sipariş durumunu görüntüleme
-   **Sipariş Yönetimi:**
    -   Sipariş geçmişini görüntüleme
    -   Sipariş durumunu güncelleme (Yönetici)
    -   Otomatik bildirim için Observer deseni kullanılarak sipariş durumu değişiklikleri için bildirimler
-   **Bildirimler:**
    -   E-posta ve SMS bildirim simülasyonu
    -   Sipariş durumu bildirimleri için Observer deseni
-   **Veritabanı Entegrasyonu:**
    -   Kullanıcı, ürün ve sipariş verilerini depolamak için SQLite kullanır.
-   **Hata Yönetimi:**
    -   Veritabanı işlemleri ve kullanıcı girişleri için temel hata yönetimi.

## Kurulum

Projeyi kurmak için aşağıdaki adımları izleyin:

1.  **Repository'i klonlayın:**
    ```bash
    git clone https://github.com/hakankocakk/Smart-Cargo-and-Order-Management-System
    ```


3.  **Bağımlılıkları yükleyin:**
    Bu proje öncelikli olarak Python'ın yerleşik modülü olan `sqlite3`'ü kullanır. Çekirdek işlevsellik için başka harici kütüphaneler zorunlu değildir.

4.  **Veritabanlarını başlatın:**
    Uygulama, ilk çalıştırmada `orders.db` ve `store.db` dosyalarını otomatik olarak oluşturacaktır.
    -   `users.db`: Kullanıcı kimlik doğrulama bilgilerini depolar.
    -   `orders.db`: Sipariş bilgilerini depolar.
    -   `store.db`: Ürün bilgilerini depolar.

## Kullanım

Uygulamayı çalıştırmak için `main.py` dosyasını çalıştırın:

```bash
python main.py
```
