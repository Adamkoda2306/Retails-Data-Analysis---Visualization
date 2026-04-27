import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy import stats as sp_stats
from utils.parse_data import parse_transaction_data

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def plot_time_series_transactions(transactions_data, output_folder):
    create_folder(output_folder)
    
    daily_data = defaultdict(lambda: {'count': 0})
    for trans in transactions_data:
        daily_data[trans['day']]['count'] += 1
    
    days = sorted(daily_data.keys())
    trans_counts = [daily_data[day]['count'] for day in days]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(days, trans_counts, color='tab:blue', marker='s', linewidth=2.5, markersize=6, label='Transactions')
    ax.set_xlabel('Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    ax.set_title('Time-Series: Transaction Count Over Days', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/01_time_series_transactions.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 01_time_series_transactions.png")
    plt.close()

def plot_basket_size_vs_value_scatter(transactions_data, output_folder):
    create_folder(output_folder)
    
    basket_sizes = [trans['basket_size'] for trans in transactions_data]
    trans_values = [trans['transaction_value'] for trans in transactions_data]
    
    jitter_amount = 0.1
    basket_sizes_jittered = [size + np.random.normal(0, jitter_amount) for size in basket_sizes]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(basket_sizes_jittered, trans_values, alpha=0.6, s=100, 
                         c=trans_values, cmap='plasma', edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel('Basket Size (Number of Items)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Transaction Value (₹)', fontsize=12, fontweight='bold')
    ax.set_title('Basket Size vs Transaction Value Correlation', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Transaction Value (₹)', fontsize=11, fontweight='bold')
    
    correlation = np.corrcoef(basket_sizes, trans_values)[0, 1]
    ax.text(0.05, 0.95, f'Correlation: {correlation:.3f}', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=11, verticalalignment='top')
    
    z = np.polyfit(basket_sizes, trans_values, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(basket_sizes), max(basket_sizes), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2.5, label='Linear Trend')
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/02_basket_size_vs_value_scatter.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 02_basket_size_vs_value_scatter.png")
    plt.close()

def plot_lorenz_curve_gini(transactions_data, output_folder):
    create_folder(output_folder)
    
    trans_values = sorted([trans['transaction_value'] for trans in transactions_data])
    cumsum = np.cumsum(trans_values)
    total_value = cumsum[-1]
    
    cumsum_pct = cumsum / total_value
    population_pct = np.arange(1, len(trans_values) + 1) / len(trans_values)
    
    population_pct = np.insert(population_pct, 0, 0)
    cumsum_pct = np.insert(cumsum_pct, 0, 0)
    
    gini = 2 * np.sum(population_pct * cumsum_pct) / len(trans_values) - 1
    gini = abs(gini)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.plot(population_pct * 100, cumsum_pct * 100, 'b-', linewidth=2.5, label='Lorenz Curve')
    ax.plot([0, 100], [0, 100], 'r--', linewidth=2, label='Perfect Equality')
    ax.fill_between(population_pct * 100, cumsum_pct * 100, population_pct * 100, 
                     alpha=0.3, color='blue', label='Inequality Area')
    
    ax.set_xlabel('Cumulative % of Transactions', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative % of Revenue', fontsize=12, fontweight='bold')
    ax.set_title(f'Lorenz Curve: Revenue Inequality (Gini Coefficient: {gini:.3f})', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    gini_text = f"Gini Coefficient: {gini:.4f}\n(0 = Perfect Equality)\n(1 = Perfect Inequality)"
    ax.text(0.6, 0.1, gini_text, transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8), fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/03_lorenz_curve_gini.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 03_lorenz_curve_gini.png")
    plt.close()

def plot_daily_transaction_count(transactions_data, output_folder):
    create_folder(output_folder)
    
    daily_counts = defaultdict(int)
    for trans in transactions_data:
        daily_counts[trans['day']] += 1
    
    days = sorted(daily_counts.keys())
    counts = [daily_counts[day] for day in days]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    bars = ax.bar(days, counts, color='steelblue', edgecolor='navy', alpha=0.7)
    
    max_count = max(counts)
    max_days = [days[i] for i, c in enumerate(counts) if c == max_count]
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if days[i] in max_days:
            bar.set_color('coral')
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    ax.set_title('Daily Transaction Count', fontsize=14, fontweight='bold')
    ax.set_xticks(days)
    ax.set_xticklabels([f'D{day}' for day in days], rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    max_days_str = ", ".join([str(d) for d in max_days])
    ax.text(0.02, 0.95, f'Highest Transactions: {max_count}\nOccurred on Days: {max_days_str}',
            transform=ax.transAxes, fontsize=11, fontweight='bold', color='darkred',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), va='top')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/04_daily_transaction_count.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 04_daily_transaction_count.png")
    plt.close()

def plot_transaction_size_distribution(transactions_data, output_folder):
    create_folder(output_folder)
    
    trans_values = [trans['transaction_value'] for trans in transactions_data]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(trans_values, bins=30, color='steelblue', edgecolor='navy', alpha=0.7)
    ax.set_xlabel('Transaction Value (₹)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Transaction Size Distribution', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    stats_text = f"""
    Mean: ₹{np.mean(trans_values):.2f}
    Median: ₹{np.median(trans_values):.2f}
    Std Dev: ₹{np.std(trans_values):.2f}
    Min: ₹{np.min(trans_values):.2f}
    Max: ₹{np.max(trans_values):.2f}
    Skewness: {sp_stats.skew(trans_values):.3f}
    """
    
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontsize=10, verticalalignment='top', horizontalalignment='right', family='monospace')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/05_transaction_size_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: 05_transaction_size_distribution.png")
    plt.close()

def generate_all_transaction_visualizations(data_file='data.txt', output_folder='outputs/transaction_analysis'):
    print("\n" + "="*60)
    print("GENERATING TRANSACTION-RELATED VISUALIZATIONS")
    print("="*60)
    
    users_data, items_data, transactions_data, num_users = parse_transaction_data(data_file)
    
    plot_time_series_transactions(transactions_data, output_folder)
    plot_basket_size_vs_value_scatter(transactions_data, output_folder)
    plot_lorenz_curve_gini(transactions_data, output_folder)
    plot_daily_transaction_count(transactions_data, output_folder)
    plot_transaction_size_distribution(transactions_data, output_folder)
    
    print(f"\n✓ All transaction visualizations saved to: {output_folder}/")