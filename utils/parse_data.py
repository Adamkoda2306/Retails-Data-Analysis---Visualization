import re
from collections import defaultdict

def parse_transaction_data(filename):
    
    users_data = defaultdict(lambda: {
        'transaction_count': 0,
        'total_spent': 0.0,
        'items_bought': [],
        'transactions': [],
        'days_visited': set()
    })
    
    items_data = defaultdict(lambda: {
        'frequency': 0,
        'total_revenue': 0.0,
        'users_bought': set(),
        'daily_sales': defaultdict(float),
        'daily_frequency': defaultdict(int)
    })
    
    transactions_data = []
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # total number of users
    num_users_match = re.search(r'Num Users=\s*(\d+)', content)
    num_users = int(num_users_match.group(1)) if num_users_match else 0
    
    # Split by day
    day_blocks = re.findall(r'D(\d+)\((\d+)\)(.*?)(?=D\d+\(|$)', content, re.DOTALL)
    
    for day_num, num_trans, day_content in day_blocks:
        day_num = int(day_num)
        
        # all transactions for this day
        transactions = re.findall(r'U(\d+):\s*(.*?)(?=U\d+:|$)', day_content, re.DOTALL)
        
        for user_id, items_str in transactions:
            user_id = int(user_id)
            
            # items with prices
            items = re.findall(r'([A-Z])\(([0-9.]+)\)', items_str)
            
            if items:
                transaction_value = 0.0
                day_items = []
                
                for item_name, price in items:
                    price = float(price)
                    transaction_value += price
                    
                    # user data
                    users_data[user_id]['items_bought'].append(item_name)
                    users_data[user_id]['total_spent'] += price
                    users_data[user_id]['days_visited'].add(day_num)
                    
                    # item data
                    items_data[item_name]['frequency'] += 1
                    items_data[item_name]['total_revenue'] += price
                    items_data[item_name]['users_bought'].add(user_id)
                    items_data[item_name]['daily_sales'][day_num] += price
                    items_data[item_name]['daily_frequency'][day_num] += 1
                    
                    day_items.append((item_name, price))
                
                # transaction
                transaction = {
                    'user_id': user_id,
                    'day': day_num,
                    'items': day_items,
                    'basket_size': len(day_items),
                    'transaction_value': transaction_value
                }
                
                users_data[user_id]['transactions'].append(transaction)
                users_data[user_id]['transaction_count'] += 1
                transactions_data.append(transaction)
    
    users_data = dict(users_data)
    items_data = dict(items_data)
    
    for user_id in users_data:
        users_data[user_id]['days_visited'] = sorted(list(users_data[user_id]['days_visited']))
    
    return users_data, items_data, transactions_data, num_users


def get_summary_statistics(users_data, items_data, transactions_data):
    
    total_transactions = len(transactions_data)
    total_users = len(users_data)
    total_items_unique = len(items_data)
    
    total_revenue = sum(t['transaction_value'] for t in transactions_data)
    avg_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
    avg_basket_size = sum(t['basket_size'] for t in transactions_data) / total_transactions if total_transactions > 0 else 0
    
    user_transaction_counts = [users_data[uid]['transaction_count'] for uid in users_data]
    avg_transactions_per_user = sum(user_transaction_counts) / total_users if total_users > 0 else 0
    
    return {
        'total_transactions': total_transactions,
        'total_users': total_users,
        'total_items_unique': total_items_unique,
        'total_revenue': total_revenue,
        'avg_transaction_value': avg_transaction_value,
        'avg_basket_size': avg_basket_size,
        'avg_transactions_per_user': avg_transactions_per_user
    }


if __name__ == "__main__":
    users_data, items_data, transactions_data, num_users = parse_transaction_data('data.txt')
    stats = get_summary_statistics(users_data, items_data, transactions_data)
    
    print("Data Parsing Complete!")
    print(f"\nSummary Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")