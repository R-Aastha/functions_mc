import requests

header = {
   "access_token": "fe66583bfe5185048c66571293e0d358"
}

response = requests.get("https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales", headers=header)

response.status_code

response.json()

base_url = "https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws"
endpoint = "/mentorskool/v1/sales?offset=0&limit=100"
final_data = []
for i in range(5):
   print('URL: ', base_url + endpoint)
   response = requests.get(base_url + endpoint, headers=header)
   response_data = response.json()
   data = response_data['data']
   final_data.extend(data)
   endpoint = response_data['next']

final_data

len(final_data)

import pandas as pd

df = pd.json_normalize(final_data)

df

df.head()

df.replace("null", None, inplace=True)

null_values = df.isnull().sum()

null_values[null_values>0]

df[df.duplicated()]

df.dtypes

df['day_number'] = pd.to_datetime(df['order.order_purchase_date']).dt.weekday

df['day_number']

df['day_label'] = df['day_number'].apply(lambda day: 'weekend' if (day==5) or (day==6) else 'weekday')

df['day_label']

df.groupby("day_label")['profit_amt'].sum()

df.columns

df.groupby("product.category")['sales_amt'].sum()

def get_available_sizes(df, product_name):
   product_data = df[df['product.product_name'] == product_name]
   available_size = product_data['product.sizes'].tolist()
   return available_size

product_name = "Redi-Strip #10 Envelopes, 4 1/8 x 9 1/2"
sizes = get_available_sizes(df, product_name)
print(sizes)

product_name = "Cisco SPA 501G IP Phone"
sizes = get_available_sizes(df, product_name)
print(sizes)

product_name = "Bretford CR4500 Series Slim Rectangular Table"
sizes = get_available_sizes(df, product_name)
print(sizes)

product_name = "Eldon Fold 'N Roll Cart System"
sizes = get_available_sizes(df, product_name)
print(sizes)

product_name = "Mitel 5320 IP Phone VoIP phone"
sizes = get_available_sizes(df, product_name)
print(sizes)

df['order.order_purchase_date'] = pd.to_datetime(df['order.order_purchase_date'])

df['Month_Name'] = df['order.order_purchase_date'].apply(lambda x: x.strftime('%B'))

monthly_sales = df.groupby('Month_Name').agg({'sales_amt': 'sum', 'profit_amt': 'sum'}).reset_index()

print(monthly_sales)

df['profit_margin'] = (df['profit_amt'] / df['sales_amt']) * 100

monthly_profit_margin = df.groupby(df['order.order_purchase_date'].dt.strftime('%B'))['profit_margin'].sum()

monthly_profit_margin

positive_profit_rows = df[df['profit_margin'] > 0]

no_of_months = positive_profit_rows['order.order_purchase_date'].dt.strftime('%B').nunique()

no_of_months

# derive the new column called delay
df["delay"] = ((pd.to_datetime(df["order.order_delivered_customer_date"]) - pd.to_datetime(df["order.order_estimated_delivery_date"])) / pd.Timedelta(days=1)).fillna(0).astype(int)
df.head()

# these are the cases where there are null values then also we are getting delay as 0, 
# fix this
df[df["delay"]==0][["order.order_estimated_delivery_date", "order.order_delivered_customer_date", "delay"]]

# Replace the delay with NaT, in the case where order_delivered_customer_date is NaT
df['delay'] = df['delay'].where(df['order.order_delivered_customer_date'].notna(), pd.NaT)

# these are the cases where there are null values then also we are getting delay as 0, 
# fix this
df[df["delay"]==0][["order.order_estimated_delivery_date", "order.order_delivered_customer_date", "delay"]]

df.shape

# filter out the instances of NaT type
sales_df2 = df[~pd.isna(df['delay'])]

sales_df2["delay_status"] = sales_df2["delay"].apply(lambda x: "Late" if x>0 else "Early" if x<0 else "On-time" if x==0 else None)
sales_df2.head()

# How many orders are late delivered to the customers
late_delivered = sales_df2[sales_df2["delay_status"]=="Late"]["order.order_id"].unique()
len(late_delivered)

## Which vendors has highest late deliveries
late_delivered.groupby("order.VendorID")["order.order_id"].count()
