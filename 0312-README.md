# Retail Data Analysis - Visualization

A comprehensive Python-based analytics tool that generates 15 visualizations from retail transaction data.

## 📋 Overview

This analyzes retail transaction data and generate visualizations across three categories:

### User Analysis (5 Visualizations)
1. **User Frequency Histogram** - How many transactions per user
2. **User Total Spending (Bar Chart)** - Total revenue by user (sorted)
3. **User Daily Spending (Small Multiples Grid)** - Day-to-day spending patterns using shared axes for easy comparison
4. **Days Between Transactions** - Box plot detailing the purchasing rhythm of users
5. **Items Bought (Stacked Bar)** - Unique vs repeated items per user

### Item Analysis (5 Visualizations)
1. **Item Frequency (Horizontal Bar)** - Most to least popular items
2. **Item Revenue (Bar Chart)** - Revenue distribution showing which items bring in the most money
3. **Market Basket Analysis** - Items frequently bought together with a target item
4. **Item Demand Elasticity** - Price vs popularity scatter plot
5. **Top Items Daily Sales** - Multi-line chart tracking product lifecycle

### Transaction Analysis (5 Visualizations)
1. **Time-Series Transactions** - Daily transaction count trend over time
2. **Basket Size vs Value** - Scatter plot with jitter showing correlation
3. **Lorenz Curve & Gini Coefficient** - Revenue inequality analysis
4. **Daily Transaction Count** - Bar chart with all peak activity days highlighted
5. **Transaction Size Distribution** - Standard linear histogram of transaction values

## 🛠️ Setup

### Requirements
- Python 3.7+
- Required packages:
  ```
  numpy
  pandas
  matplotlib
  seaborn
  scipy
  ```

### Installation

1. **Install Dependencies**
   ```bash
   pip install numpy pandas matplotlib seaborn scipy
   ```

2. **Place Your Data File**
   - Save your transaction data as `data.txt` in the working directory
   - File should be in the format provided (see Example section below)

3. **Files Structure**
   Make sure all Python files are in the same directory:
   ```
   ├── utils/
   |  ├── parse_data.py
   |  ├── user_analysis.py
   |  ├── item_analysis.py
   |  └── transaction_analysis.py
   ├── data.txt
   ├── 0312-Code.py
   ├── 0312-Report.pdf
   └── 0312-README.md
   ```

## 🚀 Usage

### Quick Start - Run Everything
```bash
python 0312-Code.py
```

This single command:
- Parses your data
- Shows summary statistics
- Generates all 15 visualizations
- Automatically creates output folders
- Saves all charts as PNG files

## 📊 Output Structure

All visualizations are automatically saved in organized folders:

```
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
```

## 📝 Data Format

Your `data.txt` file should follow this format:

```
Num Users= 20

--------------------------------------
Day (No. Trans)
UID: Items (Prices)
--------------------------------------
D1(16) 
U3: A(196.32) S(235.03) C(347.93) ...
U19: A(196.32) R(220.27) D(12.73) ...
...
```

**Format Details:**
- Line 1: Total number of users
- Each day starts with `D[day_number]([transaction_count])`
- Each transaction: `U[user_id]: [Item(Price)] [Item(Price)] ...`
- Items are single letters (A-Z)
- Prices are decimal numbers

## 🔍 Detailed Visualization Guide

### USER ANALYSIS

#### 1. User Frequency Histogram
- **Purpose:** See customer activity levels
- **Insight:** Identifies high-engagement and low-engagement customers

#### 2. User Total Spending
- **Purpose:** Identify your highest-value customers
- **Insight:** Which customers generate the most revenue

#### 3. User Daily Spending Small Multiples Grid
- **Purpose:** Find spending patterns over time per user on a shared scale
- **Insight:** Seasonal preferences, repeat customers, isolated individual trends

#### 4. Days Between Transactions
- **Purpose:** Understand customer purchase cycles
- **Insight:** Average gap between purchases, indicating customer loyalty and purchasing rhythm\

#### 5. Items Bought - Stacked Bar
- **Purpose:** See customer exploration vs loyalty
- **Insight:** Who buys new items vs repeats

### ITEM ANALYSIS

#### 1. Item Frequency Horizontal Bar
- **Purpose:** Identify bestsellers vs slow movers
- **Insight:** Most and least popular items

#### 2. Item Revenue Bar Chart
- **Purpose:** Find items that drive most revenue
- **Insight:** Pure revenue ranking without cumulative distractions

#### 3. Market Basket Analysis
- **Purpose:** Find items frequently bought together
- **Insight:** Product affinities and co-occurrence

#### 4. Item Demand Elasticity
- **Purpose:** Understand price-popularity relationship
- **Insight:** How average item price affects purchasing frequency

#### 5. Top Items Daily Sales
- **Purpose:** Track product performance over time
- **Insight:** Sales trends, lifecycle stages


### TRANSACTION ANALYSIS

#### 1. Time-Series Transactions
- **Purpose:** Track daily store traffic
- **Insight:** Total number of transactions taking place each day

#### 2. Basket Size vs Value
- **Purpose:** Correlation between items bought and amount spent
- **Insight:** Shows if larger baskets consist of cheap fillers or premium items

#### 3. Lorenz Curve & Gini Coefficient
- **Purpose:** Measure inequality in transaction sizes
- **Insight:** How concentrated revenue is among certain transactions or days

#### 4. Daily Transaction Count
- **Purpose:** See busiest days
- **Insight:** Which days have peak activity

#### 5. Transaction Size Distribution
- **Purpose:** Understand transaction value patterns
- **Insight:** General linear distribution of checkout totals


## 🐛 Troubleshooting

### "data.txt not found"
- Ensure `data.txt` is in the same directory as Python scripts
- Check file name spelling and capitalization


## Author
Koda Adam
S20230020312
UG3, ECE
---
