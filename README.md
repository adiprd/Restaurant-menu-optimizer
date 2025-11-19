# Restaurant Menu Optimizer - AI-Powered Analytics Platform

## Overview

Restaurant Menu Optimizer adalah aplikasi web canggih yang menggunakan artificial intelligence untuk menganalisis dan mengoptimalkan menu restoran. Platform ini memberikan wawasan berbasis data untuk meningkatkan profitabilitas, mengoptimalkan harga, dan mengidentifikasi peluang menu baru.

## Struktur Folder

```
restaurant_menu_optimizer/
├── app.py                          # Aplikasi Flask utama
├── requirements.txt                # Dependencies Python
├── run.py                         # Script startup otomatis
├── README.md                      # Dokumentasi
├── data/
│   └── restaurant_data.xlsx       # Dataset sample (menu, penjualan, feedback, inventory)
├── templates/
│   ├── index.html                 # Halaman landing page
│   ├── dashboard.html             # Dashboard analisis utama
│   └── error.html                 # Halaman error
└── static/
    ├── css/                       # Stylesheet (kosong - menggunakan inline CSS)
    ├── js/                        # JavaScript (kosong - menggunakan inline JS)
    └── images/                    # Asset gambar (kosong)
```

## Dataset yang Tersedia

### 1. Menu Items (`menu_items`)
- **150+ item menu** dengan berbagai kategori
- **Struktur data**: item_id, item_name, category, cost_price, selling_price, preparation_time
- **Kategori**: Appetizer, Main Course, Dessert, Beverage, Side Dish

### 2. Sales Transactions (`sales_transactions`)
- **5,000+ transaksi penjualan** dalam 6 bulan terakhir
- **Struktur data**: transaction_id, date, menu_item_id, quantity, total_price
- **Data real-time** dengan pola musiman dan trend

### 3. Customer Feedback (`customer_feedback`)
- **2,000+ review pelanggan** dengan rating
- **Struktur data**: feedback_id, menu_item_id, rating, feedback_text, date
- **Analisis sentimen** dan preferensi customer

### 4. Inventory Data (`inventory`)
- **Data stok dan supplier** untuk semua item
- **Struktur data**: item_id, current_stock, reorder_level, supplier, last_restock
- **Manajemen inventory** dan prediksi demand

## Fitur Analisis AI

### 1. Bestseller Identification
- Identifikasi otomatis menu paling populer
- Kategorisasi: Bestseller, Average, Underperformer
- Analisis berdasarkan revenue, volume penjualan, dan profit margin

### 2. Pricing Optimization
- Saran penyesuaian harga berbasis AI
- Analisis price elasticity
- Rekomendasi: Increase Price, Decrease Price, Maintain, Review Recipe Cost

### 3. Profitability Scoring
- Skor profitabilitas komprehensif (0-1 scale)
- Kombinasi metrics: revenue score, volume score, margin score
- Bobot yang dapat dikustomisasi

### 4. Menu Gap Analysis
- Identifikasi peluang menu baru
- Analisis celah harga dalam kategori
- Rekomendasi berdasarkan trend dan preferensi

### 5. Demand Prediction
- Prediksi permintaan harian
- Pola berdasarkan hari dalam minggu
- Confidence level untuk planning inventory

### 6. Customer Preference Analysis
- Analisis rating dan feedback
- Identifikasi menu dengan rating tinggi tapi penjualan rendah
- Insights untuk improvement menu

## Teknologi & Dependencies

### Backend Framework
- **Flask 2.3.3** - Web framework ringan dan powerful
- **Werkzeug 2.3.7** - WSGI utilities

### Data Analysis & AI
- **pandas 2.1.4** - Data manipulation dan analysis
- **numpy 1.26.0** - Komputasi numerik
- **scikit-learn 1.3.2** - Machine learning algorithms
- **matplotlib 3.8.2** - Visualisasi data static
- **seaborn 0.13.0** - Statistical data visualization
- **plotly 5.17.0** - Interactive visualizations

### Data Processing
- **openpyxl 3.1.2** - Excel file handling
- **faker 21.0.0** - Data generation untuk development

### Frontend
- **HTML5/CSS3** - Responsive design dengan tema coklat
- **Vanilla JavaScript** - Client-side interactions
- **Font Awesome 6.0.0** - Ikon UI
- **Plotly.js** - Interactive charts
- **Google Fonts (Inter)** - Typography modern

## Cara Menjalankan

### Opsi 1: Menggunakan Script Otomatis (Recommended)
```bash
cd restaurant_menu_optimizer
python run.py
```

### Opsi 2: Manual Execution
```bash
cd restaurant_menu_optimizer

# Install dependencies (jika belum)
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

### Akses Aplikasi
Buka browser dan kunjungi: `http://localhost:5000`

## API Endpoints

### Main Routes
- `GET /` - Landing page
- `GET /dashboard` - Dashboard analisis utama
- `GET /api/export_report` - Export laporan Excel

### Data API
- `GET /api/bestsellers` - Data bestsellers (JSON)
- `GET /api/pricing_suggestions` - Saran harga (JSON)
- `GET /api/optimization_insights` - Insights AI (JSON)

## Visualisasi & Dashboard

### Charts yang Tersedia
1. **Performance Distribution Pie Chart** - Distribusi kategori performa menu
2. **Profitability vs Price Scatter Plot** - Analisis hubungan harga-profitabilitas
3. **Revenue by Category Bar Chart** - Revenue per kategori (interactive)
4. **Top Bestsellers Table** - Daftar menu terbaik
5. **Critical Items Table** - Menu yang perlu perhatian

### Tabs Dashboard
- **Overview** - Ringkasan performa dan visualisasi utama
- **Pricing** - Saran penyesuaian harga
- **Recommendations** - Peluang menu baru
- **Demand** - Prediksi permintaan

## Business Intelligence Features

### Metrics yang Diukur
- **Total Revenue** - Pendapatan keseluruhan
- **Average Profit Margin** - Rata-rata margin keuntungan
- **Bestseller Count** - Jumlah menu high-performer
- **Underperformer Count** - Jumlah menu low-performer
- **Pricing Adjustments** - Rekomendasi perubahan harga

### AI Algorithms Implemented
1. **Quartile Analysis** untuk kategorisasi performa
2. **Profitability Scoring** dengan weighted metrics
3. **Price Elasticity Modeling** untuk optimasi harga
4. **Demand Pattern Recognition** untuk prediksi
5. **Market Gap Analysis** untuk rekomendasi menu

## Customization & Extensions

### Modifikasi Bobot Analisis
Edit di method `calculate_profitability_score`:
```python
df['profitability_score'] = (
    df['revenue_score'] * 0.4 +    # Bobot revenue
    df['volume_score'] * 0.3 +     # Bobot volume penjualan  
    df['margin_score'] * 0.3       # Bobot profit margin
)
```

### Menambah Kategori Menu
Edit variabel `categories` dalam data generator:
```python
categories = ['Appetizer', 'Main Course', 'Dessert', 'Beverage', 'Side Dish', 'New Category']
```

### Modifikasi Pricing Rules
Edit method `suggest_pricing_adjustments` untuk aturan bisnis kustom.

## Use Cases

### Untuk Restaurant Owner
- Identifikasi menu paling menguntungkan
- Optimasi strategi harga
- Perencanaan menu berdasarkan data
- Manajemen inventory yang lebih baik

### Untuk Menu Developer
- Insights preferensi pelanggan
- Identifikasi peluang menu baru
- Analisis kompetitif tidak langsung
- Data-driven menu development

### Untuk Operations Manager
- Prediksi demand untuk staffing
- Optimasi preparation time
- Supplier management insights
- Cost control opportunities

## Data Security & Privacy

- Data disimpan secara lokal
- Tidak ada external API calls
- Session management dengan secret key
- All calculations done on-server

## Performance Considerations

- Dataset optimized untuk analysis cepat
- Caching implemented untuk visualisasi
- Lazy loading untuk large datasets
- Efficient pandas operations

## Support & Troubleshooting

### Common Issues
1. **Port 5000 sudah digunakan** - Ganti port di `app.run(port=5001)`
2. **Import errors** - Pastikan semua dependencies terinstall
3. **Data loading failed** - Check file `data/restaurant_data.xlsx` exists

### Logging & Debug
- Enable debug mode: `app.run(debug=True)`
- Check console untuk error messages
- Validasi data format di Excel files

## License & Usage

MIT License - Bebas untuk penggunaan komersial dan non-komersial. Dapat dikustomisasi sesuai kebutuhan bisnis spesifik.

---

**Restaurant Menu Optimizer** - Transformasi data restoran menjadi wawasan bisnis yang actionable melalui kekuatan artificial intelligence dan analitik data.
