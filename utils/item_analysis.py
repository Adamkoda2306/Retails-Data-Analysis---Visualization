import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from utils.parse_data import parse_transaction_data

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def plot_item_frequency_horizontal_bar(items_data, output_folder):
    create_folder(output_folder)
    
    item_freq = [(item, items_data[item]['frequency']) for item in items_data]
    item_freq.sort(key=lambda x: x[1], reverse=True)
    
    items = [x[0] for x in item_freq]
    frequencies = [x[1] for x in item_freq]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    bars = ax.barh(items, frequencies, color='teal', edgecolor='darkslategray', alpha=0.7)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {int(width)}',
                ha='left', va='center', fontsize=9)
    
    ax.set_xlabel('Frequency (Number of Times Bought)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Item', fontsize=12, fontweight='bold')
    ax.set_title('Item Frequency Distribution - Most to Least Popular', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/01_item_frequency_horizontal_bar.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 01_item_frequency_horizontal_bar.png")
    plt.close()

def plot_item_revenue_bar(items_data, output_folder):
    create_folder(output_folder)
    
    item_revenue = [(item, items_data[item]['total_revenue']) for item in items_data]
    item_revenue.sort(key=lambda x: x[1], reverse=True)
    
    items = [x[0] for x in item_revenue]
    revenues = [x[1] for x in item_revenue]
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    bars = ax1.bar(range(len(items)), revenues, color='steelblue', alpha=0.7, edgecolor='navy')
    ax1.set_xlabel('Item', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Total Revenue (₹)', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(items)))
    ax1.set_xticklabels(items)
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax1.set_title('Item Revenue Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/02_item_revenue_bar.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 02_item_revenue_bar.png")
    plt.close()

def plot_market_basket_analysis(users_data, items_data, output_folder, target_item='P'):
    create_folder(output_folder)
    
    item_cooccurrence = defaultdict(int)
    
    for uid in users_data:
        items_bought = users_data[uid]['items_bought']
        if target_item in items_bought:
            for trans in users_data[uid]['transactions']:
                if target_item in [item[0] for item in trans['items']]:
                    for item_name, _ in trans['items']:
                        if item_name != target_item:
                            item_cooccurrence[item_name] += 1
    
    sorted_items = sorted(item_cooccurrence.items(), key=lambda x: x[1], reverse=True)[:15]
    
    items = [x[0] for x in sorted_items]
    frequencies = [x[1] for x in sorted_items]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(items, frequencies, color='mediumpurple', edgecolor='indigo', alpha=0.7)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {int(width)}', ha='left', va='center', fontsize=10)
    
    ax.set_xlabel('Frequency (Co-occurrence)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Item', fontsize=12, fontweight='bold')
    ax.set_title(f'Market Basket: Top 15 Items Bought With "{target_item}"', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/03_market_basket_analysis_{target_item}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 03_market_basket_analysis_{target_item}.png")
    plt.close()

def plot_item_demand_elasticity(items_data, output_folder):
    create_folder(output_folder)
    
    items = []
    avg_prices = []
    frequencies = []
    colors_list = []
    
    for item in items_data:
        total_price = items_data[item]['total_revenue']
        frequency = items_data[item]['frequency']
        avg_price = total_price / frequency if frequency > 0 else 0
        
        items.append(item)
        avg_prices.append(avg_price)
        frequencies.append(frequency)
        colors_list.append(total_price)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(avg_prices, frequencies, s=200, c=colors_list, cmap='viridis', 
                         alpha=0.6, edgecolors='black', linewidth=1.5)
    
    for i, item in enumerate(items):
        ax.annotate(item, (avg_prices[i], frequencies[i]), fontsize=9, ha='center', va='center', fontweight='bold')
    
    ax.set_xlabel('Average Price per Item (₹)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency (Number of Times Bought)', fontsize=12, fontweight='bold')
    ax.set_title('Item Demand Elasticity: Price vs Popularity', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Total Revenue (₹)', fontsize=11, fontweight='bold')
    
    z = np.polyfit(avg_prices, frequencies, 2)
    p = np.poly1d(z)
    x_trend = np.linspace(min(avg_prices), max(avg_prices), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/04_item_demand_elasticity.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 04_item_demand_elasticity.png")
    plt.close()

def plot_top_items_daily_sales(items_data, output_folder, num_items=5):
    create_folder(output_folder)
    
    top_items = sorted(items_data.items(), key=lambda x: x[1]['total_revenue'], reverse=True)[:num_items]
    top_item_names = [x[0] for x in top_items]
    
    max_day = max(max(items_data[item]['daily_sales'].keys()) for item in top_item_names)
    daily_sales_dict = {item: [] for item in top_item_names}
    
    for day in range(1, max_day + 1):
        for item in top_item_names:
            daily_sales = items_data[item]['daily_sales'].get(day, 0)
            daily_sales_dict[item].append(daily_sales)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.Set1(np.linspace(0, 1, num_items))
    for idx, item in enumerate(top_item_names):
        ax.plot(range(1, max_day + 1), daily_sales_dict[item], 
                marker='o', linewidth=2.5, markersize=6, label=f'Item {item}', color=colors[idx])
    
    ax.set_xlabel('Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Daily Sales (₹)', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {num_items} Items - Daily Sales Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(1, max_day + 1, max(1, max_day // 10)))
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/05_top_items_daily_sales.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 05_top_items_daily_sales.png")
    plt.close()

def generate_all_item_visualizations(data_file='data.txt', output_folder='outputs/item_analysis'):
    print("\n" + "="*60)
    print("GENERATING ITEM-RELATED VISUALIZATIONS")
    print("="*60)
    
    users_data, items_data, transactions_data, num_users = parse_transaction_data(data_file)
    
    plot_item_frequency_horizontal_bar(items_data, output_folder)
    plot_item_revenue_bar(items_data, output_folder)
    plot_market_basket_analysis(users_data, items_data, output_folder, target_item='P')
    plot_item_demand_elasticity(items_data, output_folder)
    plot_top_items_daily_sales(items_data, output_folder, num_items=5)
    
    print(f"\n✓ All item visualizations saved to: {output_folder}/")