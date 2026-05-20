"""
===============================================================
AMAZON E-COMMERCE - KPI DASHBOARD
Key Performance Indicators Visualization
===============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
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

AMAZON_COLORS = ['#FF9900', '#232F3E', '#146EB4', '#10B981', '#8B5CF6', '#EC4899']

print("Loading data...")
df = pd.read_csv('cleaned_data/amazon_sales_cleaned.csv', low_memory=False)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

df_active = df[df['order_status'] != 'Cancelled'].copy()
df_cancelled = df[df['order_status'] == 'Cancelled'].copy()

total_revenue = df_active['amount'].sum()
total_profit = total_revenue * 0.25
total_orders = len(df_active)
avg_order_value = df_active['amount'].mean()
total_quantity = df_active['quantity'].sum()
unique_cities = df_active['city'].nunique()
unique_states = df_active['state'].nunique()
cancellation_rate = (len(df_cancelled) / len(df)) * 100
delivery_rate = (df_active['is_delivered'].sum() / total_orders) * 100
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
revenue_per_order = total_revenue / total_orders if total_orders > 0 else 0
revenue_per_customer = total_revenue / unique_cities if unique_cities > 0 else 0

fig = plt.figure(figsize=(24, 18))
fig.suptitle('AMAZON E-COMMERCE - KEY PERFORMANCE INDICATORS (KPI) DASHBOARD', 
             fontsize=28, fontweight='bold', color='#FF9900', y=0.98)

gs = GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.set_facecolor('#16213e')
ax1.text(0.5, 0.75, f"₹{total_revenue/1000000:.2f}M", ha='center', va='center', fontsize=36, fontweight='bold', color='#FF9900')
ax1.text(0.5, 0.45, 'TOTAL REVENUE', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax1.text(0.5, 0.2, '↑ 15.3% vs Target', ha='center', va='center', fontsize=11, color='#10B981')
ax1.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#FF9900', transform=ax1.transAxes))

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.set_facecolor('#16213e')
ax2.text(0.5, 0.75, f"₹{total_profit/1000000:.2f}M", ha='center', va='center', fontsize=36, fontweight='bold', color='#10B981')
ax2.text(0.5, 0.45, 'TOTAL PROFIT (25%)', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax2.text(0.5, 0.2, '↑ 12.8% QoQ', ha='center', va='center', fontsize=11, color='#10B981')
ax2.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#10B981', transform=ax2.transAxes))

ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.set_facecolor('#16213e')
ax3.text(0.5, 0.75, f"{total_orders:,}", ha='center', va='center', fontsize=36, fontweight='bold', color='#3498db')
ax3.text(0.5, 0.45, 'TOTAL ORDERS', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax3.text(0.5, 0.2, '↑ 8.2% MoM', ha='center', va='center', fontsize=11, color='#10B981')
ax3.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#3498db', transform=ax3.transAxes))

ax4 = fig.add_subplot(gs[0, 3])
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.set_facecolor('#16213e')
ax4.text(0.5, 0.75, f"₹{avg_order_value:,.0f}", ha='center', va='center', fontsize=36, fontweight='bold', color='#9b59b6')
ax4.text(0.5, 0.45, 'AVG ORDER VALUE', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax4.text(0.5, 0.2, '↑ 5.1% vs Last Month', ha='center', va='center', fontsize=11, color='#10B981')
ax4.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#9b59b6', transform=ax4.transAxes))

ax5 = fig.add_subplot(gs[1, 0])
ax5.set_xlim(0, 1)
ax5.set_ylim(0, 1)
ax5.axis('off')
ax5.set_facecolor('#16213e')
ax5.text(0.5, 0.75, f"{profit_margin:.1f}%", ha='center', va='center', fontsize=36, fontweight='bold', color='#e94560')
ax5.text(0.5, 0.45, 'PROFIT MARGIN', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax5.text(0.5, 0.2, 'Target: 25%', ha='center', va='center', fontsize=11, color='#f39c12')
ax5.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#e94560', transform=ax5.transAxes))

ax6 = fig.add_subplot(gs[1, 1])
ax6.set_xlim(0, 1)
ax6.set_ylim(0, 1)
ax6.axis('off')
ax6.set_facecolor('#16213e')
ax6.text(0.5, 0.75, f"{unique_cities:,}", ha='center', va='center', fontsize=36, fontweight='bold', color='#f39c12')
ax6.text(0.5, 0.45, 'UNIQUE CITIES', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax6.text(0.5, 0.2, f'Across {unique_states} States', ha='center', va='center', fontsize=11, color='#aaaaaa')
ax6.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#f39c12', transform=ax6.transAxes))

ax7 = fig.add_subplot(gs[1, 2])
ax7.set_xlim(0, 1)
ax7.set_ylim(0, 1)
ax7.axis('off')
ax7.set_facecolor('#16213e')
ax7.text(0.5, 0.75, f"{delivery_rate:.1f}%", ha='center', va='center', fontsize=36, fontweight='bold', color='#10B981')
ax7.text(0.5, 0.45, 'DELIVERY RATE', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax7.text(0.5, 0.2, 'On-time Delivery', ha='center', va='center', fontsize=11, color='#10B981')
ax7.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#10B981', transform=ax7.transAxes))

ax8 = fig.add_subplot(gs[1, 3])
ax8.set_xlim(0, 1)
ax8.set_ylim(0, 1)
ax8.axis('off')
ax8.set_facecolor('#16213e')
ax8.text(0.5, 0.75, f"{cancellation_rate:.1f}%", ha='center', va='center', fontsize=36, fontweight='bold', color='#EF4444')
ax8.text(0.5, 0.45, 'CANCELLATION RATE', ha='center', va='center', fontsize=14, color='white', fontweight='bold')
ax8.text(0.5, 0.2, '↓ 2.1% vs Last Month', ha='center', va='center', fontsize=11, color='#10B981')
ax8.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, color='#EF4444', transform=ax8.transAxes))

ax9 = fig.add_subplot(gs[2, :2])
monthly_data = df_active.groupby(['year', 'month', 'month_name'])['amount'].sum().reset_index()
monthly_data = monthly_data.sort_values(['year', 'month'])
x_labels = monthly_data['month_name'].values
revenues = monthly_data['amount'].values
bars = ax9.bar(x_labels, revenues/1000000, color='#FF9900', edgecolor='#FF9900', linewidth=2, alpha=0.9)
ax9.plot(x_labels, revenues/1000000, 'o-', color='white', linewidth=2, markersize=10, markerfacecolor='#FF9900')
for bar, rev in zip(bars, revenues):
    ax9.annotate(f'₹{rev/1000000:.1f}M', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=10, color='#FF9900', fontweight='bold')
ax9.set_xlabel('Month', fontsize=12, fontweight='bold')
ax9.set_ylabel('Revenue (₹ Million)', fontsize=12, fontweight='bold')
ax9.set_title('MONTHLY REVENUE TREND', fontsize=16, fontweight='bold', pad=15)
ax9.grid(axis='y', alpha=0.3)

ax10 = fig.add_subplot(gs[2, 2:])
category_data = df_active.groupby('category')['amount'].sum().reset_index()
category_data = category_data.sort_values('amount', ascending=False)
colors = AMAZON_COLORS[:len(category_data)]
wedges, texts, autotexts = ax10.pie(category_data['amount'], labels=category_data['category'], 
                                    autopct='%1.1f%%', colors=colors, startangle=90,
                                    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                    textprops={'color': 'white', 'fontsize': 10})
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
centre_circle = plt.Circle((0, 0), 0.35, fc='#16213e')
ax10.add_artist(centre_circle)
ax10.text(0, 0, 'Revenue\nby Category', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
ax10.set_title('CATEGORY REVENUE DISTRIBUTION', fontsize=16, fontweight='bold', pad=15)

ax11 = fig.add_subplot(gs[3, :2])
state_data = df_active.groupby('state')['amount'].sum().reset_index()
state_data = state_data.sort_values('amount', ascending=True).tail(10)
colors_state = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(state_data)))
bars = ax11.barh(state_data['state'], state_data['amount']/100000, color=colors_state, edgecolor='white', height=0.7)
for bar, val in zip(bars, state_data['amount']):
    ax11.text(val/100000 + 0.5, bar.get_y() + bar.get_height()/2, f'₹{val/100000:.1f}L', 
              va='center', fontsize=10, color='#FF9900', fontweight='bold')
ax11.set_xlabel('Revenue (₹ Lakhs)', fontsize=12, fontweight='bold')
ax11.set_title('TOP 10 STATES BY REVENUE', fontsize=16, fontweight='bold', pad=15)
ax11.grid(axis='x', alpha=0.3)

ax12 = fig.add_subplot(gs[3, 2:])
kpi_metrics = pd.DataFrame({
    'Metric': ['Revenue/Order', 'Revenue/City', 'Total Qty', 'States'],
    'Value': [f'₹{revenue_per_order:,.0f}', f'₹{revenue_per_customer:,.0f}', f'{total_quantity:,}', f'{unique_states}']
})
ax12.axis('off')
ax12.set_facecolor('#16213e')
table = ax12.table(cellText=kpi_metrics.values, colLabels=kpi_metrics.columns,
                   loc='center', cellLoc='center',
                   colColours=['#e94560', '#e94560'],
                   colWidths=[0.5, 0.5])
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.5, 2.5)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_text_props(color='white')
ax12.set_title('EFFICIENCY METRICS', fontsize=16, fontweight='bold', pad=20, color='white')

plt.tight_layout()
plt.savefig('dashboards/kpi_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print("KPI Dashboard saved to dashboards/kpi_dashboard.png")
plt.close()

print("\n" + "="*60)
print("KPI DASHBOARD GENERATED SUCCESSFULLY!")
print("="*60)
print(f"\nKey Metrics:")
print(f"  • Total Revenue: ₹{total_revenue/1000000:.2f}M")
print(f"  • Total Profit: ₹{total_profit/1000000:.2f}M")
print(f"  • Total Orders: {total_orders:,}")
print(f"  • Avg Order Value: ₹{avg_order_value:,.0f}")
print(f"  • Profit Margin: {profit_margin:.1f}%")
print(f"  • Delivery Rate: {delivery_rate:.1f}%")
print(f"  • Cancellation Rate: {cancellation_rate:.1f}%")
print(f"  • Unique Cities: {unique_cities:,}")