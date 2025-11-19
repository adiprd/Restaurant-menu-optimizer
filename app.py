from flask import Flask, render_template, request, jsonify, session, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import json
import random
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import warnings
warnings.filterwarnings('ignore')

# Setup matplotlib untuk non-GUI environment
plt.switch_backend('Agg')

app = Flask(__name__)
app.secret_key = 'restaurant_optimizer_secret_2024'

class RestaurantAIAnalyzer:
    def __init__(self):
        self.menu_data = None
        self.sales_data = None
        self.feedback_data = None
        self.inventory_data = None
        
    def load_data(self):
        """Load data dari file Excel"""
        try:
            self.menu_data = pd.read_excel('data/restaurant_data.xlsx', sheet_name='menu_items')
            self.sales_data = pd.read_excel('data/restaurant_data.xlsx', sheet_name='sales_transactions')
            self.feedback_data = pd.read_excel('data/restaurant_data.xlsx', sheet_name='customer_feedback')
            self.inventory_data = pd.read_excel('data/restaurant_data.xlsx', sheet_name='inventory')
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_bestsellers(self):
        """Identifikasi bestsellers dan underperformers"""
        sales_summary = self.sales_data.groupby('menu_item_id').agg({
            'quantity': 'sum',
            'total_price': 'sum',
            'transaction_id': 'count'
        }).rename(columns={'transaction_id': 'order_count'})
        
        menu_with_sales = self.menu_data.merge(sales_summary, left_on='item_id', right_index=True, how='left')
        menu_with_sales = menu_with_sales.fillna(0)
        
        # Kategorisasi berdasarkan quartile
        revenue_quartiles = menu_with_sales['total_price'].quantile([0.25, 0.5, 0.75])
        quantity_quartiles = menu_with_sales['quantity'].quantile([0.25, 0.5, 0.75])
        
        def categorize_performance(row):
            if row['total_price'] >= revenue_quartiles[0.75] and row['quantity'] >= quantity_quartiles[0.75]:
                return 'Bestseller'
            elif row['total_price'] <= revenue_quartiles[0.25] and row['quantity'] <= quantity_quartiles[0.25]:
                return 'Underperformer'
            else:
                return 'Average'
        
        menu_with_sales['performance_category'] = menu_with_sales.apply(categorize_performance, axis=1)
        
        # Hitung profit margin
        menu_with_sales['profit_margin'] = ((menu_with_sales['selling_price'] - menu_with_sales['cost_price']) / 
                                          menu_with_sales['selling_price']) * 100
        
        return menu_with_sales
    
    def calculate_profitability_score(self, df):
        """Hitung skor profitability untuk setiap menu item"""
        # Normalisasi metrics
        df['revenue_score'] = (df['total_price'] - df['total_price'].min()) / (df['total_price'].max() - df['total_price'].min())
        df['volume_score'] = (df['quantity'] - df['quantity'].min()) / (df['quantity'].max() - df['quantity'].min())
        df['margin_score'] = (df['profit_margin'] - df['profit_margin'].min()) / (df['profit_margin'].max() - df['profit_margin'].min())
        
        # Hitung overall score (bisa disesuaikan bobotnya)
        df['profitability_score'] = (df['revenue_score'] * 0.4 + 
                                   df['volume_score'] * 0.3 + 
                                   df['margin_score'] * 0.3)
        
        return df
    
    def suggest_pricing_adjustments(self, df):
        """Saran penyesuaian harga berdasarkan analisis"""
        pricing_suggestions = []
        
        for _, item in df.iterrows():
            suggestion = {
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'current_price': item['selling_price'],
                'current_margin': item['profit_margin'],
                'suggestion': 'Maintain',
                'new_price': item['selling_price'],
                'expected_margin_change': 0
            }
            
            # Tambahkan price_elasticity dummy untuk analisis
            price_elasticity = random.uniform(-1.5, -0.2)
            
            # Bestseller dengan margin rendah - bisa naik harga
            if (item['performance_category'] == 'Bestseller' and 
                item['profit_margin'] < 30 and 
                price_elasticity > -0.5):  # Asumsi inelastic demand
                price_increase = item['selling_price'] * 0.1  # 10% increase
                suggestion.update({
                    'suggestion': 'Increase Price',
                    'new_price': round(item['selling_price'] + price_increase, 2),
                    'expected_margin_change': 8
                })
            
            # Underperformer dengan margin tinggi - bisa turun harga
            elif (item['performance_category'] == 'Underperformer' and 
                  item['profit_margin'] > 40):
                price_decrease = item['selling_price'] * 0.15  # 15% decrease
                suggestion.update({
                    'suggestion': 'Decrease Price',
                    'new_price': round(item['selling_price'] - price_decrease, 2),
                    'expected_margin_change': -5
                })
            
            # Item dengan margin sangat rendah
            elif item['profit_margin'] < 15:
                suggestion.update({
                    'suggestion': 'Review Recipe Cost',
                    'new_price': item['selling_price'],
                    'expected_margin_change': 0
                })
            
            pricing_suggestions.append(suggestion)
        
        return pd.DataFrame(pricing_suggestions)
    
    def analyze_customer_preferences(self):
        """Analisis preferensi customer dari feedback"""
        if self.feedback_data.empty:
            return None
            
        feedback_analysis = self.feedback_data.groupby('menu_item_id').agg({
            'rating': ['mean', 'count'],
            'feedback_text': 'count'
        }).round(2)
        
        feedback_analysis.columns = ['avg_rating', 'rating_count', 'feedback_count']
        feedback_analysis = feedback_analysis.reset_index()
        
        # Merge dengan data menu
        menu_with_feedback = self.menu_data.merge(feedback_analysis, left_on='item_id', right_on='menu_item_id', how='left')
        
        return menu_with_feedback
    
    def recommend_new_dishes(self, df):
        """Rekomendasi menu baru berdasarkan trend"""
        # Analisis kategori yang populer - HANYA gunakan kolom yang sudah ada
        aggregation_dict = {
            'profitability_score': 'mean',
            'quantity': 'sum',
            'total_price': 'sum'
        }
        
        # Cek jika kolom avg_rating ada, baru tambahkan ke aggregation
        if 'avg_rating' in df.columns:
            aggregation_dict['avg_rating'] = 'mean'
        
        category_performance = df.groupby('category').agg(aggregation_dict).round(3)
        
        # Identifikasi gaps dalam menu
        popular_categories = category_performance.nlargest(3, 'profitability_score').index.tolist()
        
        recommendations = []
        for category in popular_categories:
            category_items = df[df['category'] == category]
            
            # Cari price points yang belum ter-cover
            price_ranges = {
                'Budget': (0, 15),
                'Mid-range': (15, 30),
                'Premium': (30, 100)
            }
            
            for range_name, (min_price, max_price) in price_ranges.items():
                items_in_range = category_items[
                    (category_items['selling_price'] >= min_price) & 
                    (category_items['selling_price'] < max_price)
                ]
                
                if len(items_in_range) == 0:
                    recommendations.append({
                        'category': category,
                        'price_range': range_name,
                        'suggested_price': (min_price + max_price) / 2,
                        'opportunity_score': 'High'
                    })
        
        return recommendations
    
    def predict_demand(self):
        """Prediksi demand untuk inventory management"""
        # Siapkan data untuk prediction
        sales_daily = self.sales_data.groupby(['date', 'menu_item_id']).agg({
            'quantity': 'sum'
        }).reset_index()
        
        # Feature engineering
        sales_daily['date'] = pd.to_datetime(sales_daily['date'])
        sales_daily['day_of_week'] = sales_daily['date'].dt.dayofweek
        sales_daily['is_weekend'] = sales_daily['day_of_week'].isin([5, 6]).astype(int)
        sales_daily['month'] = sales_daily['date'].dt.month
        
        # Prediksi menggunakan model sederhana
        predictions = []
        for item_id in sales_daily['menu_item_id'].unique():
            item_data = sales_daily[sales_daily['menu_item_id'] == item_id]
            
            if len(item_data) > 10:  # Hanya prediksi untuk item dengan data cukup
                # Model sederhana: rata-rata per hari dalam minggu
                weekly_pattern = item_data.groupby('day_of_week')['quantity'].mean()
                
                for day in range(7):
                    predicted_qty = weekly_pattern.get(day, item_data['quantity'].mean())
                    predictions.append({
                        'menu_item_id': item_id,
                        'day_of_week': day,
                        'predicted_demand': max(0, round(predicted_qty)),
                        'confidence': 'High' if len(item_data) > 30 else 'Medium'
                    })
        
        return pd.DataFrame(predictions)
    
    def generate_visualizations(self, df):
        """Generate visualisasi data"""
        visualizations = {}
        
        # Warna coklat palette
        brown_palette = ['#8B4513', '#A0522D', '#CD853F', '#D2691E', '#F4A460']
        
        # 1. Bestseller vs Underperformer Chart
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        performance_counts = df['performance_category'].value_counts()
        ax1.pie(performance_counts.values, labels=performance_counts.index, autopct='%1.1f%%', colors=brown_palette[:3])
        ax1.set_title('Menu Performance Distribution')
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight', facecolor='#FAF0E6')
        img1.seek(0)
        visualizations['performance_pie'] = base64.b64encode(img1.getvalue()).decode()
        plt.close(fig1)
        
        # 2. Profitability vs Price Scatter
        fig2, ax2 = plt.subplots(figsize=(12, 8), facecolor='#FAF0E6')
        categories = df['category'].unique()
        
        for i, category in enumerate(categories):
            category_data = df[df['category'] == category]
            ax2.scatter(category_data['selling_price'], 
                       category_data['profitability_score'],
                       c=[brown_palette[i % len(brown_palette)]], label=category, alpha=0.7, s=100)
        
        ax2.set_xlabel('Selling Price ($)')
        ax2.set_ylabel('Profitability Score')
        ax2.set_title('Profitability vs Price by Category')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#FAF0E6')
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight', facecolor='#FAF0E6')
        img2.seek(0)
        visualizations['scatter_plot'] = base64.b64encode(img2.getvalue()).decode()
        plt.close(fig2)
        
        # 3. Revenue by Category
        revenue_data = df.groupby('category')['total_price'].sum().reset_index()
        fig3 = px.bar(revenue_data,
                     x='category', y='total_price',
                     title='Total Revenue by Category',
                     color='total_price',
                     color_continuous_scale=['#8B4513', '#A0522D', '#CD853F'])
        fig3.update_layout(plot_bgcolor='#FAF0E6', paper_bgcolor='#FAF0E6')
        visualizations['revenue_bar'] = fig3.to_html()
        
        return visualizations

# Initialize analyzer
analyzer = RestaurantAIAnalyzer()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not analyzer.load_data():
        return render_template('error.html', message="Failed to load data")
    
    # Analisis data
    menu_analysis = analyzer.analyze_bestsellers()
    menu_analysis = analyzer.calculate_profitability_score(menu_analysis)
    pricing_suggestions = analyzer.suggest_pricing_adjustments(menu_analysis)
    customer_prefs = analyzer.analyze_customer_preferences()
    
    # Merge customer preferences TERLEBIH DAHULU sebelum recommend_new_dishes
    if customer_prefs is not None:
        menu_analysis = menu_analysis.merge(
            customer_prefs[['item_id', 'avg_rating', 'rating_count']], 
            on='item_id', how='left'
        )
    
    # Sekarang baru panggil recommend_new_dishes setelah merge
    new_dish_recommendations = analyzer.recommend_new_dishes(menu_analysis)
    demand_predictions = analyzer.predict_demand()
    
    # Generate visualizations
    visuals = analyzer.generate_visualizations(menu_analysis)
    
    # Stats untuk dashboard
    stats = {
        'total_items': len(menu_analysis),
        'bestsellers': len(menu_analysis[menu_analysis['performance_category'] == 'Bestseller']),
        'underperformers': len(menu_analysis[menu_analysis['performance_category'] == 'Underperformer']),
        'total_revenue': menu_analysis['total_price'].sum(),
        'avg_profit_margin': menu_analysis['profit_margin'].mean(),
        'pricing_adjustments': len(pricing_suggestions[pricing_suggestions['suggestion'] != 'Maintain'])
    }
    
    return render_template('dashboard.html',
                         stats=stats,
                         menu_data=menu_analysis.to_dict('records'),
                         pricing_suggestions=pricing_suggestions.to_dict('records'),
                         new_dish_recommendations=new_dish_recommendations,
                         demand_predictions=demand_predictions.to_dict('records'),
                         visuals=visuals)
    
@app.route('/api/bestsellers')
def api_bestsellers():
    if not analyzer.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    menu_analysis = analyzer.analyze_bestsellers()
    bestsellers = menu_analysis[menu_analysis['performance_category'] == 'Bestseller']
    
    return jsonify(bestsellers.to_dict('records'))

@app.route('/api/pricing_suggestions')
def api_pricing_suggestions():
    if not analyzer.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    menu_analysis = analyzer.analyze_bestsellers()
    pricing_suggestions = analyzer.suggest_pricing_adjustments(menu_analysis)
    
    return jsonify(pricing_suggestions.to_dict('records'))

@app.route('/api/export_report')
def export_report():
    if not analyzer.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    # Generate comprehensive report
    menu_analysis = analyzer.analyze_bestsellers()
    menu_analysis = analyzer.calculate_profitability_score(menu_analysis)
    pricing_suggestions = analyzer.suggest_pricing_adjustments(menu_analysis)
    
    # Create Excel report
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        menu_analysis.to_excel(writer, sheet_name='Menu Analysis', index=False)
        pricing_suggestions.to_excel(writer, sheet_name='Pricing Suggestions', index=False)
    
    output.seek(0)
    
    return send_file(output, 
                    download_name=f'restaurant_analysis_{datetime.now().strftime("%Y%m%d")}.xlsx',
                    as_attachment=True)

@app.route('/api/optimization_insights')
def api_optimization_insights():
    if not analyzer.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    menu_analysis = analyzer.analyze_bestsellers()
    menu_analysis = analyzer.calculate_profitability_score(menu_analysis)
    
    insights = {
        'top_performers': menu_analysis.nlargest(5, 'profitability_score')[['item_name', 'profitability_score']].to_dict('records'),
        'low_margin_items': menu_analysis[menu_analysis['profit_margin'] < 20][['item_name', 'profit_margin']].to_dict('records'),
        'high_rating_low_sales': menu_analysis[
            (menu_analysis['avg_rating'] > 4) & 
            (menu_analysis['performance_category'] == 'Underperformer')
        ][['item_name', 'avg_rating', 'quantity']].to_dict('records')
    }
    
    return jsonify(insights)

if __name__ == '__main__':
    print("Starting Restaurant Menu Optimizer...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
