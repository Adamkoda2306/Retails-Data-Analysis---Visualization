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

def plot_user_frequency_histogram(users_data, output_folder):
    create_folder(output_folder)
    
    user_ids = sorted(users_data.keys())
    transaction_counts = [users_data[uid]['transaction_count'] for uid in user_ids]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    bars = ax.bar(user_ids, transaction_counts, color='steelblue', edgecolor='navy', alpha=0.7)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('User ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    ax.set_title('User Transaction Frequency Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(user_ids)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/01_user_frequency_histogram.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 01_user_frequency_histogram.png")
    plt.close()

def plot_user_daily_spending_small_multiples(users_data, output_folder):
    create_folder(output_folder)
    
    user_ids = sorted(users_data.keys())
    num_users = len(user_ids)
    
    max_day = max((t['day'] for uid in users_data for t in users_data[uid]['transactions']), default=30)
    days = range(1, max_day + 1)
    
    cols = 4
    rows = (num_users + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(20, 16), sharex=True, sharey=True)
    axes = axes.flatten()
    
    for i, uid in enumerate(user_ids):
        ax = axes[i]
        
        daily_spend = {day: 0.0 for day in days}
        for trans in users_data[uid]['transactions']:
            daily_spend[trans['day']] += trans['transaction_value']
            
        spending = [daily_spend[day] for day in days]
        
        ax.fill_between(days, spending, color='steelblue', alpha=0.4)
        ax.plot(days, spending, color='navy', linewidth=1.5)
        
        ax.set_title(f'User {uid}', fontsize=12, fontweight='bold', pad=5, color='darkslategray')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        if i >= len(axes) - cols:
            ax.set_xlabel('Day', fontsize=10, fontweight='bold')
        
        if i % cols == 0:
            ax.set_ylabel('Spend (₹)', fontsize=10, fontweight='bold')
            
    for j in range(num_users, len(axes)):
        axes[j].set_visible(False)
        
    fig.suptitle('Individual User Daily Spending Trends (30 Days)', fontsize=18, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    
    plt.savefig(f'{output_folder}/03_user_daily_spending_grid.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 03_user_daily_spending_grid.png")
    plt.close()

def plot_user_total_spending(users_data, output_folder):
    create_folder(output_folder)
    
    user_spending = [(uid, users_data[uid]['total_spent']) for uid in users_data]
    user_spending.sort(key=lambda x: x[1], reverse=True)
    
    user_ids = [x[0] for x in user_spending]
    spending_amounts = [x[1] for x in user_spending]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    bars = ax.bar(range(len(user_ids)), spending_amounts, color='coral', edgecolor='darkred', alpha=0.7)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:.2f}',
                ha='center', va='bottom', fontsize=8, rotation=0)
    
    ax.set_xlabel('User (Sorted by Total Spending)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Amount Spent (₹)', fontsize=12, fontweight='bold')
    ax.set_title('User Total Spending - Ranked from Highest to Lowest', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(user_ids)))
    ax.set_xticklabels([f'U{uid}' for uid in user_ids], rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/02_user_total_spending.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 02_user_total_spending.png")
    plt.close()

def plot_days_between_transactions(users_data, output_folder):
    create_folder(output_folder)
    
    days_between = []
    
    for uid in users_data:
        transactions = sorted(users_data[uid]['transactions'], key=lambda x: x['day'])
        days_list = [t['day'] for t in transactions]
        
        if len(days_list) > 1:
            gaps = [days_list[i+1] - days_list[i] for i in range(len(days_list)-1)]
            days_between.extend(gaps)
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    box = ax1.boxplot([days_between], labels=['All Users'], patch_artist=True)
    box['boxes'][0].set_facecolor('lightblue')
    ax1.set_ylabel('Days Between Purchases', fontsize=12, fontweight='bold')
    ax1.set_title('Distribution of Days Between Consecutive Transactions', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    stats_text = f"Mean: {np.mean(days_between):.2f} days\nMedian: {np.median(days_between):.2f} days\nStd Dev: {np.std(days_between):.2f} days"
    ax1.text(0.75, 0.95, stats_text, transform=ax1.transAxes, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), va='top')

    explanation = (
        ""
    )
    ax1.text(0.05, 0.95, explanation, transform=ax1.transAxes, 
             bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.8), 
             va='top', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/04_days_between_transactions.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 04_days_between_transactions.png")
    plt.close()

def plot_items_bought_stacked_bar(users_data, output_folder):
    create_folder(output_folder)
    
    user_ids = sorted(users_data.keys())
    unique_items_count = []
    repeated_items_count = []
    
    for uid in user_ids:
        items = users_data[uid]['items_bought']
        item_counter = Counter(items)
        
        unique_items = len(item_counter)
        repeated_items = sum(count - 1 for count in item_counter.values())
        
        unique_items_count.append(unique_items)
        repeated_items_count.append(repeated_items)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = range(len(user_ids))
    width = 0.6
    
    p1 = ax.bar(x, unique_items_count, width, label='Unique Items', color='steelblue', alpha=0.8)
    p2 = ax.bar(x, repeated_items_count, width, bottom=unique_items_count, label='Repeated Items', color='coral', alpha=0.8)
    
    ax.set_xlabel('User ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Items', fontsize=12, fontweight='bold')
    ax.set_title('Items Bought by User: Unique vs Repeated', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'U{uid}' for uid in user_ids], rotation=45, ha='right')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/05_items_bought_stacked_bar.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 05_items_bought_stacked_bar.png")
    plt.close()

def generate_all_user_visualizations(data_file='data.txt', output_folder='outputs/user_analysis'):
    print("\n" + "="*60)
    print("GENERATING USER-RELATED VISUALIZATIONS")
    print("="*60)
    
    users_data, items_data, transactions_data, num_users = parse_transaction_data(data_file)
    
    plot_user_frequency_histogram(users_data, output_folder)
    plot_user_total_spending(users_data, output_folder)
    plot_user_daily_spending_small_multiples(users_data, output_folder)
    plot_days_between_transactions(users_data, output_folder)
    plot_items_bought_stacked_bar(users_data, output_folder)
    
    print(f"\n✓ All user visualizations saved to: {output_folder}/")