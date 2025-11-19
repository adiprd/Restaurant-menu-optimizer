# AI RESTAURANT MENU OPTIMIZER

Aplikasi AI untuk analisis dan optimasi menu restoran berbasis data penjualan dan preferensi customer.

## Fitur Utama

- **Bestseller Identification** - Identifikasi menu paling menguntungkan
- **Underperformer Analysis** - Deteksi menu yang kurang perform
- **Pricing Optimization** - Saran penyesuaian harga berbasis AI
- **Menu Recommendations** - Rekomendasi menu baru berdasarkan trend
- **Demand Prediction** - Prediksi permintaan untuk manajemen inventory
- **Customer Preference Analysis** - Analisis rating dan feedback pelanggan

## Data yang Digunakan

Aplikasi menggunakan sample data yang mencakup:
- **150+ menu items** dengan kategori dan harga
- **5,000+ transaksi penjualan** dalam 6 bulan terakhir
- **Customer feedback** dan rating
- **Data inventory** dan cost structure

## Instalasi

1. **Jalankan aplikasi generator** untuk membuat project
2. **Masuk ke direktori** yang dibuat:
   ```bash
   cd restaurant_menu_optimizer
   ```

3. **Jalankan aplikasi**:
   ```bash
   python run.py
   ```

4. **Akses aplikasi**:
   Buka browser dan kunjungi: http://localhost:5000

## Cara Penggunaan

1. **Launch Dashboard** dari halaman home
2. **Analisis Overview** untuk melihat performance keseluruhan
3. **Check Pricing Suggestions** untuk optimasi harga
4. **Explore Menu Recommendations** untuk ide menu baru
5. **Review Demand Predictions** untuk planning inventory

## Arsitektur Teknis

- **Backend**: Flask
- **Data Analysis**: Pandas, NumPy, Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Data Generation**: Faker
- **Reporting**: Excel export

## Struktur Data

### Menu Items
- item_id, item_name, category, cost_price, selling_price

### Sales Transactions  
- transaction_id, date, menu_item_id, quantity, total_price

### Customer Feedback
- feedback_id, menu_item_id, rating, feedback_text, date

### Inventory
- item_id, current_stock, reorder_level, supplier

## Algorithms Used

1. **Profitability Scoring** - Kombinasi revenue, volume, dan margin
2. **Price Elasticity Modeling** - Analisis sensitivitas harga
3. **Demand Forecasting** - Pattern analysis berdasarkan historical data
4. **Market Gap Analysis** - Identifikasi opportunities dalam menu

## Deployment

Untuk deployment production:

1. Set `debug=False` dalam app.run()
2. Gunakan production WSGI server (Gunicorn)
3. Setup database sesungguhnya (MySQL/PostgreSQL)
4. Implementasi authentication untuk multi-user

## License

MIT License - bebas digunakan untuk project komersial dan non-komersial.

## Kontribusi

Silakan fork dan submit pull request untuk improvements.
