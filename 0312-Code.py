import os
import sys
from pathlib import Path

# Importing analysis modules
from utils.user_analysis import generate_all_user_visualizations
from utils.item_analysis import generate_all_item_visualizations
from utils.transaction_analysis import generate_all_transaction_visualizations
from utils.parse_data import parse_transaction_data, get_summary_statistics

def main():
    print("\n" + "="*70)
    print(" "*15 + "DATA ANALYSIS - VISUALIZATION")
    print("="*70)
    
    # Data file path
    data_file = 'data.txt'
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"\n❌ ERROR: {data_file} not found in current directory!")
        print(f"   Current directory: {os.getcwd()}")
        sys.exit(1)
    
    print(f"\n📁 Data file: {data_file}")
    
    # Parse data and show summary
    print("\n📊 Parsing data...")
    try:
        users_data, items_data, transactions_data, num_users = parse_transaction_data(data_file)
        stats = get_summary_statistics(users_data, items_data, transactions_data)
        
        print("\n✓ Data parsed successfully!")
        print("\n📈 SUMMARY STATISTICS:")
        print("-" * 70)
        print(f"  Total Users:                {stats['total_users']}")
        print(f"  Total Transactions:         {stats['total_transactions']}")
        print(f"  Total Unique Items:         {stats['total_items_unique']}")
        print(f"  Total Revenue:              ₹{stats['total_revenue']:,.2f}")
        print(f"  Average Transaction Value:  ₹{stats['avg_transaction_value']:,.2f}")
        print(f"  Average Basket Size:        {stats['avg_basket_size']:.2f} items")
        print(f"  Avg Transactions/User:      {stats['avg_transactions_per_user']:.2f}")
        print("-" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR parsing data: {e}")
        sys.exit(1)
    
    # Creating output directories
    output_dirs = [
        'outputs/user_analysis',
        'outputs/item_analysis',
        'outputs/transaction_analysis'
    ]
    
    print("\n📁 Creating output directories...")
    for dir_path in output_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"  ✓ {dir_path}/")
    
    # Visualizations
    print("\n\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    try:
        # User Analysis
        generate_all_user_visualizations(data_file, 'outputs/user_analysis')
        
        # Item Analysis
        generate_all_item_visualizations(data_file, 'outputs/item_analysis')
        
        # Transaction Analysis
        generate_all_transaction_visualizations(data_file, 'outputs/transaction_analysis')
        
    except Exception as e:
        print(f"\n❌ ERROR during visualization generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Final summary
    print("\n\n" + "="*70)
    print("✓ ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    print("\n📊 OUTPUT STRUCTURE:")
    print("""
    outputs/
    ├── user_analysis/
    │   ├── 01_user_frequency_histogram.png
    │   ├── 02_user_total_spending.png
    │   ├── 03_user_daily_spending_grid.png
    │   ├── 04_days_between_transactions.png
    │   └── 05_items_bought_stacked_bar.png
    │
    ├── item_analysis/
    │   ├── 01_item_frequency_horizontal_bar.png
    │   ├── 02_item_revenue_bar.png
    │   ├── 03_market_basket_analysis_P.png
    │   ├── 04_item_demand_elasticity.png
    │   └── 05_top_items_daily_sales.png
    │
    └── transaction_analysis/
        ├── 01_time_series_transactions.png
        ├── 02_basket_size_vs_value_scatter.png
        ├── 03_lorenz_curve_gini.png
        ├── 04_daily_transaction_count.png
        └── 05_transaction_size_distribution.png
    """)
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()