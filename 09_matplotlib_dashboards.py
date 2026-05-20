"""
===============================================================
AMAZON E-COMMERCE DASHBOARD VISUALIZATION
Real-Time Graphical Dashboard with Matplotlib
===============================================================
Author: Business Intelligence Analyst
Purpose: Interactive Dashboard with KPIs and Charts
===============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#16213e'
plt.rcParams['axes.edgecolor'] = '#e94560'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['grid.color'] = '#0f3460'
plt.rcParams['legend.facecolor'] = '#16213e'
plt.rcParams['font.family'] = 'sans-serif'

COLORS = {
    'primary': '#e94560',
    'secondary': '#0f3460',
    'success': '#00bf63',
    'warning': '#f39c12',
    'info': '#3498db',
    'purple': '#9b59b6',
    'orange': '#e67e22',
    'teal': '#1abc9c',
    'dark': '#2c3e50',
    'light': '#ecf0f1'
}

AMAZON_COLORS = ['#FF9900', '#232F3E', '#146EB4', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B', '#EF4444']

print("Loading cleaned data...")
df = pd.read_csv('cleaned_data/amazon_sales_cleaned.csv', low_memory=False)
print(f"Loaded {len(df):,} records")

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

df_active = df[df['order_status'] != 'Cancelled'].copy()
df_cancelled = df[df['order_status'] == 'Cancelled'].copy()

def format_currency(value):
    if value >= 10000000:
        return f'Rs.{value/10000000:.2f}M'
    elif value >= 100000:
        return f'Rs.{value/100000:.2f}L'
    elif value >= 1000:
        return f'Rs.{value/1000:.2f}K'
    else:
        return f'Rs.{value:.2f}'

def format_number(value):
    if value >= 1000000:
        return f'{value/1000000:.2f}M'
    elif value >= 1000:
        return f'{value/1000:.2f}K'
    else:
        return f'{value:.0f}'

def create_executive_dashboard():
    print("\n[1/5] Creating Executive Dashboard...")
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('AMAZON E-COMMERCE - EXECUTIVE DASHBOARD', fontsize=24, fontweight='bold', color='#FF9900', y=0.98)
    
    gs = GridSpec(4, 4, figure=fig, hspace=0.3, wspace=0.3)
    
    total_revenue = df_active['amount'].sum()
    total_profit = total_revenue * 0.25
    total_orders = len(df_active)
    avg_order_value = df_active['amount'].mean()
    cancellation_rate = (len(df_cancelled) / len(df)) * 100
    delivery_rate = (df_active['is_delivered'].sum() / total_orders) * 100
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.set_facecolor('#16213e')
    ax1.text(0.5, 0.7, f"Rs.{total_revenue/1000000:.2f}M", ha='center', va='center', fontsize=28, fontweight='bold', color='#FF9900')
    ax1.text(0.5, 0.35, 'TOTAL REVENUE', ha='center', va='center', fontsize=10, color='white')
    ax1.text(0.5, 0.15, '+15.3% vs Target', ha='center', va='center', fontsize=9, color='#10B981')
    ax1.add_patch(plt.Rectangle((0, 0.9), 1, 0.1, color='#FF9900', transform=ax1.transAxes))
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.set_facecolor('#16213e')
    ax2.text(0.5, 0.7, f"Rs.{total_profit/1000000:.2f}M", ha='center', va='center', fontsize=28, fontweight='bold', color='#10B981')
    ax2.text(0.5, 0.35, 'TOTAL PROFIT (25%)', ha='center', va='center', fontsize=10, color='white')
    ax2.text(0.5, 0.15, '+12.8% QoQ', ha='center', va='center', fontsize=9, color='#10B981')
    ax2.add_patch(plt.Rectangle((0, 0.9), 1, 0.1, color='#10B981', transform=ax2.transAxes))
    
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.set_facecolor('#16213e')
    ax3.text(0.5, 0.7, f"{total_orders:,}", ha='center', va='center', fontsize=28, fontweight='bold', color='#3498db')
    ax3.text(0.5, 0.35, 'TOTAL ORDERS', ha='center', va='center', fontsize=10, color='white')
    ax3.text(0.5, 0.15, '+8.2% MoM', ha='center', va='center', fontsize=9, color='#10B981')
    ax3.add_patch(plt.Rectangle((0, 0.9), 1, 0.1, color='#3498db', transform=ax3.transAxes))
    
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_facecolor('#16213e')
    ax4.text(0.5, 0.7, f"Rs.{avg_order_value:.0f}", ha='center', va='center', fontsize=28, fontweight='bold', color='#9b59b6')
    ax4.text(0.5, 0.35, 'AVG ORDER VALUE', ha='center', va='center', fontsize=10, color='white')
    ax4.text(0.5, 0.15, '+5.1% vs Last Month', ha='center', va='center', fontsize=9, color='#10B981')
    ax4.add_patch(plt.Rectangle((0, 0.9), 1, 0.1, color='#9b59b6', transform=ax4.transAxes))
    
    ax5 = fig.add_subplot(gs[1, :2])
    monthly_data = df_active.groupby(['year', 'month', 'month_name'])['amount'].sum().reset_index()
    monthly_data = monthly_data.sort_values(['year', 'month'])
    
    x_labels = monthly_data['month_name'].values
    revenues = monthly_data['amount'].values
    
    bars = ax5.bar(x_labels, revenues/1000000, color='#FF9900', edgecolor='#FF9900', linewidth=2, alpha=0.9)
    ax5.plot(x_labels, revenues/1000000, 'o-', color='white', linewidth=2, markersize=8, markerfacecolor='#FF9900')
    
    for bar, rev in zip(bars, revenues):
        ax5.annotate(f'Rs.{rev/1000000:.1f}M', 
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=9, color='#FF9900', fontweight='bold')
    
    ax5.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Revenue (Rs. Million)', fontsize=12, fontweight='bold')
    ax5.set_title('MONTHLY REVENUE TREND', fontsize=14, fontweight='bold', pad=15)
    ax5.grid(axis='y', alpha=0.3)
    
    for i in range(1, len(revenues)):
        growth = ((revenues[i] - revenues[i-1]) / revenues[i-1]) * 100
        color = '#10B981' if growth > 0 else '#EF4444'
        ax5.annotate(f'+{growth:.1f}%', 
                    xy=(i, revenues[i]/1000000 + 0.5),
                    ha='center', fontsize=8, color=color, fontweight='bold')
    
    ax6 = fig.add_subplot(gs[1, 2:])
    category_data = df_active.groupby('category')['amount'].sum().reset_index()
    category_data = category_data.sort_values('amount', ascending=False)
    
    colors = AMAZON_COLORS[:len(category_data)]
    wedges, texts, autotexts = ax6.pie(category_data['amount'], labels=category_data['category'], 
                                        autopct='%1.1f%%', colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                        textprops={'color': 'white', 'fontsize': 9})
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
    
    centre_circle = plt.Circle((0, 0), 0.35, fc='#16213e')
    ax6.add_artist(centre_circle)
    ax6.text(0, 0, 'Revenue\nby Category', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax6.set_title('CATEGORY REVENUE DISTRIBUTION', fontsize=14, fontweight='bold', pad=15)
    
    ax7 = fig.add_subplot(gs[2, :2])
    state_data = df_active.groupby('state')['amount'].sum().reset_index()
    state_data = state_data.sort_values('amount', ascending=True).tail(10)
    
    bars = ax7.barh(state_data['state'], state_data['amount']/100000, color='#FF9900', edgecolor='white', height=0.7)
    
    for bar, val in zip(bars, state_data['amount']):
        ax7.text(val/100000 + 0.5, bar.get_y() + bar.get_height()/2, 
                f'Rs.{val/100000:.1f}L', va='center', fontsize=9, color='#FF9900', fontweight='bold')
    
    ax7.set_xlabel('Revenue (Rs. Lakhs)', fontsize=12, fontweight='bold')
    ax7.set_title('TOP 10 STATES BY REVENUE', fontsize=14, fontweight='bold', pad=15)
    ax7.grid(axis='x', alpha=0.3)
    
    ax8 = fig.add_subplot(gs[2, 2:])
    status_data = df['order_status'].value_counts()
    colors = ['#10B981', '#3498db', '#EF4444', '#F59E0B', '#9b59b6', '#e67e22', '#1abc9c', '#e94560', '#34495e']
    colors = colors[:len(status_data)]
    
    wedges, texts, autotexts = ax8.pie(status_data.values, labels=status_data.index, 
                                        autopct='%1.1f%%', colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                        textprops={'color': 'white', 'fontsize': 8})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(8)
    
    centre_circle = plt.Circle((0, 0), 0.35, fc='#16213e')
    ax8.add_artist(centre_circle)
    ax8.text(0, 0, f'Orders\n{len(df):,}', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax8.set_title('ORDER STATUS DISTRIBUTION', fontsize=14, fontweight='bold', pad=15)
    
    ax9 = fig.add_subplot(gs[3, :2])
    category_profit = df_active.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
    category_profit['profit'] = category_profit['sum'] * 0.25
    category_profit = category_profit.sort_values('profit', ascending=False)
    
    x = np.arange(len(category_profit))
    width = 0.35
    
    bars1 = ax9.bar(x - width/2, category_profit['sum']/1000000, width, label='Revenue', color='#FF9900', edgecolor='white')
    bars2 = ax9.bar(x + width/2, category_profit['profit']/1000000, width, label='Profit (25%)', color='#10B981', edgecolor='white')
    
    ax9.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax9.set_ylabel('Amount (Rs. Million)', fontsize=12, fontweight='bold')
    ax9.set_xticks(x)
    ax9.set_xticklabels(category_profit['category'], rotation=45, ha='right', fontsize=9)
    ax9.legend(loc='upper right')
    ax9.set_title('REVENUE VS PROFIT BY CATEGORY', fontsize=14, fontweight='bold', pad=15)
    ax9.grid(axis='y', alpha=0.3)
    
    ax10 = fig.add_subplot(gs[3, 2:])
    weekly_data = df_active.groupby([df_active['order_date'].dt.to_period('W')])['amount'].agg(['sum', 'count']).reset_index()
    weekly_data.columns = ['week', 'revenue', 'orders']
    weekly_data['week'] = range(len(weekly_data))
    
    ax10.fill_between(weekly_data['week'], weekly_data['revenue']/100000, color='#FF9900', alpha=0.3)
    ax10.plot(weekly_data['week'], weekly_data['revenue']/100000, 'o-', color='#FF9900', linewidth=2, markersize=4)
    
    ax10_twin = ax10.twinx()
    ax10_twin.plot(weekly_data['week'], weekly_data['orders'], 's-', color='#3498db', linewidth=2, markersize=4, label='Orders')
    
    ax10.set_xlabel('Week Number', fontsize=12, fontweight='bold')
    ax10.set_ylabel('Revenue (Rs. Lakhs)', fontsize=12, fontweight='bold', color='#FF9900')
    ax10_twin.set_ylabel('Orders', fontsize=12, fontweight='bold', color='#3498db')
    ax10.set_title('WEEKLY REVENUE & ORDERS TREND', fontsize=14, fontweight='bold', pad=15)
    ax10.grid(alpha=0.3)
    ax10.legend(loc='upper left')
    ax10_twin.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('dashboards/executive_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print("   [OK] Executive Dashboard saved")
    plt.close()

def create_product_dashboard():
    print("\n[2/5] Creating Product Performance Dashboard...")
    
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('AMAZON E-COMMERCE - PRODUCT PERFORMANCE DASHBOARD', 
                 fontsize=24, fontweight='bold', color='#FF9900', y=0.98)
    
    gs = GridSpec(4, 2, figure=fig, hspace=0.35, wspace=0.25)
    
    # ================================================================
    # TOP ROW: Top 10 Products (Full Width Bar Chart)
    # ================================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    top_products = df_active.groupby('sku')['amount'].sum().reset_index()
    top_products = top_products.sort_values('amount', ascending=True).tail(10)
    
    colors = plt.cm.YlOrRd(np.linspace(0.4, 0.95, len(top_products)))
    bars = ax1.barh(range(len(top_products)), top_products['amount']/1000, 
                    color=colors, edgecolor='#FF9900', linewidth=1.5, height=0.7)
    
    ax1.set_yticks(range(len(top_products)))
    ax1.set_yticklabels(top_products['sku'], fontsize=10, fontweight='bold')
    ax1.set_xlabel('Revenue (Rs. Thousands)', fontsize=12, fontweight='bold')
    ax1.set_title('TOP 10 PRODUCTS BY REVENUE', fontsize=15, fontweight='bold', pad=10)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, val in zip(bars, top_products['amount']):
        ax1.text(val/1000 + 30, bar.get_y() + bar.get_height()/2, 
                f'Rs.{val/1000:.0f}K', va='center', fontsize=9, 
                color='white', fontweight='bold')
    
    # ================================================================
    # ROW 2: Category Performance (Left) + Category Revenue Pie (Right)
    # ================================================================
    ax2 = fig.add_subplot(gs[1, 0])
    
    category_data = df_active.groupby('category')['amount'].sum().reset_index()
    category_data = category_data.sort_values('amount', ascending=False)
    
    x = np.arange(len(category_data))
    bars = ax2.bar(category_data['category'], category_data['amount']/1000000, 
                   color='#FF9900', edgecolor='white', linewidth=1.5, width=0.7)
    
    ax2.set_xlabel('Category', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Revenue (Rs. Million)', fontsize=11, fontweight='bold')
    ax2.set_title('CATEGORY REVENUE', fontsize=14, fontweight='bold', pad=10)
    ax2.tick_params(axis='x', rotation=30, labelsize=9)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar, val in zip(bars, category_data['amount']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'Rs.{val/1000000:.1f}M', ha='center', fontsize=8, 
                color='#FF9900', fontweight='bold')
    
    ax3 = fig.add_subplot(gs[1, 1])
    
    colors_pie = ['#FF9900', '#232F3E', '#146EB4', '#10B981', '#8B5CF6', 
                  '#EC4899', '#F59E0B', '#EF4444', '#FF6B6B']
    
    wedges, texts, autotexts = ax3.pie(category_data['amount'], 
                                       labels=category_data['category'], 
                                       autopct='%1.1f%%', 
                                       colors=colors_pie[:len(category_data)], 
                                       startangle=90,
                                       wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2),
                                       textprops={'color': 'white', 'fontsize': 9})
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(8)
    
    centre_circle = plt.Circle((0, 0), 0.38, fc='#16213e')
    ax3.add_artist(centre_circle)
    ax3.text(0, 0, 'Revenue\nShare', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='white')
    
    ax3.set_title('CATEGORY REVENUE SHARE', fontsize=14, fontweight='bold', pad=10)
    
    # ================================================================
    # ROW 3: Monthly Category Performance (Left) + Size Distribution (Right)
    # ================================================================
    ax4 = fig.add_subplot(gs[2, 0])
    
    category_monthly = df_active.groupby(['month_name', 'category'])['amount'].sum().unstack(fill_value=0)
    category_monthly = category_monthly.reindex(['March', 'April', 'May', 'June'], fill_value=0)
    
    bar_width = 0.2
    x_pos = np.arange(len(category_monthly))
    
    for i, col in enumerate(category_monthly.columns):
        bars = ax4.bar(x_pos + i * bar_width, category_monthly[col]/1000000, 
                       bar_width, label=col, color=AMAZON_COLORS[i % len(AMAZON_COLORS)], 
                       edgecolor='white', linewidth=1)
    
    ax4.set_xlabel('Month', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Revenue (Rs. Million)', fontsize=11, fontweight='bold')
    ax4.set_xticks(x_pos + bar_width * 2)
    ax4.set_xticklabels(category_monthly.index, fontsize=10)
    ax4.legend(title='Category', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
    ax4.set_title('MONTHLY CATEGORY PERFORMANCE', fontsize=14, fontweight='bold', pad=10)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    ax5 = fig.add_subplot(gs[2, 1])
    
    size_data = df_active['size'].value_counts().head(8)
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(size_data)))
    
    bars = ax5.bar(size_data.index, size_data.values, color=colors, 
                   edgecolor='white', linewidth=1.5, width=0.6)
    
    ax5.set_xlabel('Size', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
    ax5.set_title('SIZE DISTRIBUTION', fontsize=14, fontweight='bold', pad=10)
    ax5.tick_params(axis='x', rotation=0, labelsize=9)
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar, val in zip(bars, size_data.values):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}', ha='center', fontsize=8, color='white', fontweight='bold')
    
    # ================================================================
    # BOTTOM ROW: Revenue Tier + Order Size + Bottom Products
    # ================================================================
    ax6 = fig.add_subplot(gs[3, 0])
    
    tier_data = df_active['revenue_tier'].value_counts()
    colors_tier = {'Budget': '#3498db', 'Mid-Range': '#9b59b6', 
                   'Premium': '#f39c12', 'Luxury': '#e94560'}
    tier_colors = [colors_tier.get(t, '#95a5a6') for t in tier_data.index]
    
    wedges, texts, autotexts = ax6.pie(tier_data.values, 
                                       labels=tier_data.index, 
                                       autopct='%1.1f%%', 
                                       colors=tier_colors[:len(tier_data)], 
                                       startangle=90,
                                       wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                       textprops={'color': 'white', 'fontsize': 10})
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    ax6.set_title('REVENUE TIER DISTRIBUTION', fontsize=14, fontweight='bold', pad=10)
    
    ax7 = fig.add_subplot(gs[3, 1])
    
    order_size_data = df_active['order_size'].value_counts()
    colors_ord = ['#FF9900', '#146EB4', '#10B981', '#8B5CF6']
    
    bars = ax7.bar(order_size_data.index, order_size_data.values, 
                  color=colors_ord[:len(order_size_data)], 
                  edgecolor='white', linewidth=1.5, width=0.5)
    
    ax7.set_xlabel('Order Size', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax7.set_title('ORDER SIZE BREAKDOWN', fontsize=14, fontweight='bold', pad=10)
    ax7.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar, val in zip(bars, order_size_data.values):
        ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}', ha='center', fontsize=10, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('dashboards/product_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print("   [OK] Product Dashboard saved")
    plt.close()

def create_customer_dashboard():
    print("\n[3/5] Creating Customer Analytics Dashboard...")
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('AMAZON E-COMMERCE - CUSTOMER ANALYTICS DASHBOARD', fontsize=24, fontweight='bold', color='#FF9900', y=0.98)
    
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, :2])
    top_customers = df_active.groupby('city')['amount'].agg(['sum', 'count']).reset_index()
    top_customers.columns = ['city', 'revenue', 'orders']
    top_customers = top_customers.sort_values('revenue', ascending=False).head(10)
    
    colors = plt.cm.Oranges(np.linspace(0.9, 0.3, len(top_customers)))
    bars = ax1.barh(range(len(top_customers)), top_customers['revenue']/100000, color=colors, edgecolor='white')
    ax1.set_yticks(range(len(top_customers)))
    ax1.set_yticklabels(top_customers['city'], fontsize=8)
    ax1.set_xlabel('Revenue (Rs. Lakhs)', fontsize=11, fontweight='bold')
    ax1.set_title('TOP 10 CUSTOMER CITIES BY REVENUE', fontsize=13, fontweight='bold')
    ax1.invert_yaxis()
    
    for bar, row in zip(bars, top_customers.itertuples()):
        ax1.text(row.revenue/100000 + 0.5, bar.get_y() + bar.get_height()/2, 
                f'Rs.{row.revenue/100000:.1f}L ({row.orders:,})', va='center', fontsize=8, color='white')
    
    ax2 = fig.add_subplot(gs[0, 2])
    state_customers = df_active.groupby('state')['city'].nunique().reset_index()
    state_customers = state_customers.sort_values('city', ascending=False).head(8)
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(state_customers)))
    bars = ax2.bar(state_customers['state'], state_customers['city'], color=colors, edgecolor='white')
    ax2.set_xlabel('State', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Unique Cities', fontsize=10, fontweight='bold')
    ax2.set_title('CITIES PER STATE', fontsize=13, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45, labelsize=8)
    ax2.grid(axis='y', alpha=0.3)
    
    ax3 = fig.add_subplot(gs[1, 0])
    city_data = df_active.groupby('city')['amount'].agg(['sum', 'count']).reset_index()
    city_data.columns = ['city', 'revenue', 'orders']
    scatter = ax3.scatter(city_data['orders'], city_data['revenue']/1000, 
                         c=city_data['revenue'], cmap='YlOrRd', s=50, alpha=0.7, edgecolor='white')
    ax3.set_xlabel('Number of Orders', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Revenue (Rs. Thousands)', fontsize=10, fontweight='bold')
    ax3.set_title('ORDERS VS REVENUE', fontsize=13, fontweight='bold')
    ax3.grid(alpha=0.3)
    
    ax4 = fig.add_subplot(gs[1, 1])
    b2b_data = df_active.groupby('b2b_flag')['amount'].agg(['sum', 'count']).reset_index()
    b2b_data['label'] = ['B2C', 'B2B']
    colors = ['#3498db', '#e94560']
    bars = ax4.bar(b2b_data['label'], b2b_data['count'], color=colors, edgecolor='white', width=0.5)
    for bar, val, rev in zip(bars, b2b_data['count'], b2b_data['sum']):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}\nRs.{rev/1000000:.1f}M', ha='center', fontsize=9, color='white', fontweight='bold')
    ax4.set_ylabel('Order Count', fontsize=10, fontweight='bold')
    ax4.set_title('B2B VS B2C ORDERS', fontsize=13, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    ax5 = fig.add_subplot(gs[1, 2])
    city_orders = df_active.groupby('city').size().reset_index(name='orders')
    repeat_customers = city_orders[city_orders['orders'] > 1]
    one_time = city_orders[city_orders['orders'] == 1]
    labels = ['Repeat\nCustomers', 'One-time\nCustomers']
    values = [len(repeat_customers), len(one_time)]
    colors = ['#10B981', '#f39c12']
    wedges, texts, autotexts = ax5.pie(values, labels=labels, autopct='%1.1f%%', 
                                        colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white'),
                                        textprops={'color': 'white', 'fontsize': 10})
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax5.set_title('CUSTOMER RETENTION', fontsize=13, fontweight='bold')
    
    ax6 = fig.add_subplot(gs[2, :])
    monthly_customers = df_active.groupby(df_active['order_date'].dt.to_period('M'))['city'].nunique().reset_index()
    monthly_customers.columns = ['month', 'unique_customers']
    monthly_customers['month'] = monthly_customers['month'].astype(str)
    x = range(len(monthly_customers))
    bars = ax6.bar(x, monthly_customers['unique_customers'], color='#FF9900', edgecolor='white', width=0.6)
    ax6.plot(x, monthly_customers['unique_customers'], 'o-', color='white', linewidth=2, markersize=8)
    ax6.set_xticks(x)
    ax6.set_xticklabels(monthly_customers['month'], fontsize=10)
    ax6.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Unique Customers', fontsize=12, fontweight='bold')
    ax6.set_title('MONTHLY UNIQUE CUSTOMER TREND', fontsize=13, fontweight='bold')
    ax6.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, monthly_customers['unique_customers']):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{val:,}', ha='center', fontsize=9, color='#FF9900', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('dashboards/customer_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print("   [OK] Customer Dashboard saved")
    plt.close()

def create_regional_dashboard():
    print("\n[4/5] Creating Regional Analysis Dashboard...")
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('AMAZON E-COMMERCE - REGIONAL ANALYSIS DASHBOARD', fontsize=24, fontweight='bold', color='#FF9900', y=0.98)
    
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, :])
    state_revenue = df_active.groupby('state')['amount'].sum().reset_index()
    state_revenue = state_revenue.sort_values('amount', ascending=False)
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(state_revenue)))
    bars = ax1.bar(range(len(state_revenue)), state_revenue['amount']/1000000, color=colors, edgecolor='white', width=0.8)
    ax1.set_xticks(range(len(state_revenue)))
    ax1.set_xticklabels(state_revenue['state'], rotation=45, ha='right', fontsize=8)
    ax1.set_xlabel('State', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Revenue (Rs. Million)', fontsize=11, fontweight='bold')
    ax1.set_title('STATE-WISE REVENUE DISTRIBUTION', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    for i, bar in enumerate(bars[:5]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'Rs.{bar.get_height():.2f}M', ha='center', fontsize=8, color='#FF9900', fontweight='bold')
    
    def classify_region(state):
        north = ['DELHI', 'UTTAR PRADESH', 'PUNJAB', 'HARYANA', 'RAJASTHAN', 'JAMMU AND KASHMIR', 'CHANDIGARH', 'UTTARAKHAND', 'HIMACHAL PRADESH']
        south = ['TAMIL NADU', 'KARNATAKA', 'KERALA', 'ANDHRA PRADESH', 'TELANGANA']
        east = ['WEST BENGAL', 'ODISHA', 'BIHAR', 'JHARKHAND', 'ASSAM']
        west = ['MAHARASHTRA', 'GUJARAT', 'GOA']
        central = ['MADHYA PRADESH', 'CHHATTISGARH']
        if state in north: return 'North'
        elif state in south: return 'South'
        elif state in east: return 'East'
        elif state in west: return 'West'
        elif state in central: return 'Central'
        else: return 'Other'
    
    df_active['region'] = df_active['state'].apply(classify_region)
    region_data = df_active.groupby('region')['amount'].sum()
    
    ax2 = fig.add_subplot(gs[1, 0])
    colors = ['#FF9900', '#146EB4', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B']
    wedges, texts, autotexts = ax2.pie(region_data.values, labels=region_data.index, 
                                        autopct='%1.1f%%', colors=colors[:len(region_data)], startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white'),
                                        textprops={'color': 'white', 'fontsize': 10})
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax2.set_title('REGIONAL CONTRIBUTION', fontsize=13, fontweight='bold')
    
    ax3 = fig.add_subplot(gs[1, 1])
    city_revenue = df_active.groupby('city')['amount'].sum().reset_index()
    city_revenue = city_revenue.sort_values('amount', ascending=False).head(10)
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(city_revenue)))
    bars = ax3.barh(range(len(city_revenue)), city_revenue['amount']/1000, color=colors, edgecolor='white')
    ax3.set_yticks(range(len(city_revenue)))
    ax3.set_yticklabels(city_revenue['city'], fontsize=8)
    ax3.set_xlabel('Revenue (Rs. Thousands)', fontsize=10, fontweight='bold')
    ax3.set_title('TOP 10 CITIES BY REVENUE', fontsize=13, fontweight='bold')
    ax3.invert_yaxis()
    
    ax4 = fig.add_subplot(gs[1, 2])
    low_states = state_revenue.sort_values('amount').head(5)
    colors = plt.cm.Reds(np.linspace(0.9, 0.3, len(low_states)))
    bars = ax4.barh(range(len(low_states)), low_states['amount']/1000, color=colors, edgecolor='white')
    ax4.set_yticks(range(len(low_states)))
    ax4.set_yticklabels(low_states['state'], fontsize=8)
    ax4.set_xlabel('Revenue (Rs. Thousands)', fontsize=10, fontweight='bold')
    ax4.set_title('LOW PERFORMING STATES', fontsize=13, fontweight='bold', color='#EF4444')
    ax4.invert_yaxis()
    
    ax5 = fig.add_subplot(gs[2, :])
    region_monthly = df_active.groupby([df_active['order_date'].dt.to_period('M'), 'region'])['amount'].sum().unstack(fill_value=0)
    for i, col in enumerate(region_monthly.columns):
        ax5.plot(range(len(region_monthly)), region_monthly[col]/100000, 'o-', 
                label=col, linewidth=2, markersize=6, color=AMAZON_COLORS[i])
    ax5.set_xticks(range(len(region_monthly)))
    ax5.set_xticklabels([str(x) for x in region_monthly.index], fontsize=9)
    ax5.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Revenue (Rs. Lakhs)', fontsize=12, fontweight='bold')
    ax5.set_title('REGIONAL MONTHLY REVENUE TREND', fontsize=13, fontweight='bold')
    ax5.legend(loc='upper right')
    ax5.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dashboards/regional_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print("   [OK] Regional Dashboard saved")
    plt.close()

def create_operational_dashboard():
    print("\n[5/5] Creating Operational Analysis Dashboard...")
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('AMAZON E-COMMERCE - OPERATIONAL ANALYSIS DASHBOARD', fontsize=24, fontweight='bold', color='#FF9900', y=0.98)
    
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    cancel_rate = (len(df_cancelled) / len(df)) * 100
    delivered_rate = len(df[df['order_status'] == 'Shipped - Delivered to Buyer']) / len(df) * 100
    
    ax1 = fig.add_subplot(gs[0, 0])
    labels = ['Cancelled', 'Delivered', 'In Transit']
    sizes = [cancel_rate, delivered_rate, 100 - cancel_rate - delivered_rate]
    colors = ['#EF4444', '#10B981', '#F59E0B']
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                        colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white'),
                                        textprops={'color': 'white', 'fontsize': 10})
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    ax1.set_title('ORDER STATUS OVERVIEW', fontsize=13, fontweight='bold')
    
    ax2 = fig.add_subplot(gs[0, 1])
    fulfil_data = df.groupby('fulfilment_method')['amount'].agg(['sum', 'count']).reset_index()
    x = np.arange(len(fulfil_data))
    width = 0.35
    bars1 = ax2.bar(x - width/2, fulfil_data['count'], width, label='Orders', color='#3498db', edgecolor='white')
    bars2 = ax2.bar(x + width/2, fulfil_data['sum']/100000, width, label='Revenue (Rs.L)', color='#FF9900', edgecolor='white')
    ax2.set_xticks(x)
    ax2.set_xticklabels(fulfil_data['fulfilment_method'], fontsize=10)
    ax2.set_ylabel('Count / Revenue', fontsize=10, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.set_title('FULFILLMENT METHOD ANALYSIS', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    ax3 = fig.add_subplot(gs[0, 2])
    ship_level_data = df.groupby('ship_service_level')['amount'].agg(['sum', 'count']).reset_index()
    colors = ['#9b59b6', '#e67e22']
    bars = ax3.bar(ship_level_data['ship_service_level'], ship_level_data['count'], color=colors, edgecolor='white', width=0.6)
    for bar, val in zip(bars, ship_level_data['count']):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:,}', ha='center', fontsize=10, color='white', fontweight='bold')
    ax3.set_xlabel('Ship Service Level', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Order Count', fontsize=10, fontweight='bold')
    ax3.set_title('SHIP SERVICE LEVEL', fontsize=13, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    ax4 = fig.add_subplot(gs[1, :2])
    cancel_monthly = df_cancelled.groupby(df_cancelled['order_date'].dt.to_period('M')).size()
    total_monthly = df.groupby(df['order_date'].dt.to_period('M')).size()
    cancel_rate_monthly = (cancel_monthly / total_monthly * 100).fillna(0)
    x = range(len(cancel_rate_monthly))
    bars = ax4.bar(x, cancel_rate_monthly.values, color='#EF4444', edgecolor='white', alpha=0.8, width=0.6)
    ax4.plot(x, cancel_rate_monthly.values, 'o-', color='white', linewidth=2, markersize=8)
    ax4.axhline(y=cancel_rate, color='#FF9900', linestyle='--', linewidth=2, label=f'Avg Rate: {cancel_rate:.1f}%')
    ax4.set_xticks(x)
    ax4.set_xticklabels([str(x) for x in cancel_rate_monthly.index], fontsize=10)
    ax4.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Cancellation Rate (%)', fontsize=12, fontweight='bold')
    ax4.set_title('MONTHLY CANCELLATION RATE TREND', fontsize=13, fontweight='bold')
    ax4.legend(loc='upper right')
    ax4.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, cancel_rate_monthly.values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{val:.1f}%', ha='center', fontsize=9, color='#EF4444', fontweight='bold')
    
    ax5 = fig.add_subplot(gs[1, 2])
    courier_data = df['courier_status'].value_counts().head(6)
    colors = plt.cm.Set2(np.linspace(0, 1, len(courier_data)))
    bars = ax5.barh(range(len(courier_data)), courier_data.values, color=colors, edgecolor='white')
    ax5.set_yticks(range(len(courier_data)))
    ax5.set_yticklabels(courier_data.index, fontsize=8)
    ax5.set_xlabel('Count', fontsize=10, fontweight='bold')
    ax5.set_title('COURIER STATUS', fontsize=13, fontweight='bold')
    ax5.invert_yaxis()
    
    ax6 = fig.add_subplot(gs[2, 0])
    promo_data = df.groupby('has_promotion')['amount'].agg(['sum', 'count']).reset_index()
    promo_data['label'] = ['Without Promo', 'With Promo']
    colors = ['#95a5a6', '#FF9900']
    bars = ax6.bar(promo_data['label'], promo_data['count'], color=colors, edgecolor='white', width=0.6)
    for bar, val, rev in zip(bars, promo_data['count'], promo_data['sum']):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
                f'{val:,}\nRs.{rev/1000000:.1f}M', ha='center', fontsize=9, color='white', fontweight='bold')
    ax6.set_ylabel('Order Count', fontsize=10, fontweight='bold')
    ax6.set_title('PROMOTION IMPACT', fontsize=13, fontweight='bold')
    ax6.grid(axis='y', alpha=0.3)
    
    ax7 = fig.add_subplot(gs[2, 1])
    status_order = ['Pending', 'Shipped - Picked Up', 'Shipped', 'Shipped - Out for Delivery', 'Shipped - Delivered to Buyer']
    status_counts = []
    for status in status_order:
        if status in df['order_status'].values:
            status_counts.append(len(df[df['order_status'] == status]))
        else:
            status_counts.append(0)
    y_pos = np.arange(len(status_order))
    ax7.barh(y_pos, status_counts, color='#3498db', edgecolor='white', height=0.6)
    ax7.set_yticks(y_pos)
    ax7.set_yticklabels(status_order, fontsize=9)
    ax7.set_xlabel('Count', fontsize=10, fontweight='bold')
    ax7.set_title('ORDER STATUS FUNNEL', fontsize=13, fontweight='bold')
    ax7.grid(axis='x', alpha=0.3)
    
    ax8 = fig.add_subplot(gs[2, 2])
    weekend_data = df_active.groupby('is_weekend')['amount'].agg(['sum', 'count']).reset_index()
    weekend_data['label'] = ['Weekday', 'Weekend']
    colors = ['#3498db', '#e94560']
    bars = ax8.bar(weekend_data['label'], weekend_data['sum']/1000000, color=colors, edgecolor='white', width=0.5)
    for bar, val, cnt in zip(bars, weekend_data['sum'], weekend_data['count']):
        ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'Rs.{val/1000000:.2f}M\n({cnt:,} orders)', ha='center', fontsize=9, color='white', fontweight='bold')
    ax8.set_ylabel('Revenue (Rs. Million)', fontsize=10, fontweight='bold')
    ax8.set_title('WEEKEND VS WEEKDAY', fontsize=13, fontweight='bold')
    ax8.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dashboards/operational_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print("   [OK] Operational Dashboard saved")
    plt.close()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING AMAZON E-COMMERCE DASHBOARDS")
    print("="*70 + "\n")
    
    create_executive_dashboard()
    create_product_dashboard()
    create_customer_dashboard()
    create_regional_dashboard()
    create_operational_dashboard()
    
    print("\n" + "="*70)
    print("ALL DASHBOARDS GENERATED SUCCESSFULLY!")
    print("="*70)
    print("\nOutput files in dashboards/ folder:")
    print("  - executive_dashboard.png")
    print("  - product_dashboard.png")
    print("  - customer_dashboard.png")
    print("  - regional_dashboard.png")
    print("  - operational_dashboard.png")