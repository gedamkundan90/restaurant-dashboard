import pandas as pd

# Load all 4 sheets and remove empty columns
sales = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Sales")
menu = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Menu")
employees = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Employee")
delivery = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Delivery")

# Remove empty columns and rows
sales = sales.dropna(axis=1, how='all').dropna(axis=0, how='all')
menu = menu.dropna(axis=1, how='all').dropna(axis=0, how='all')
employees = employees.dropna(axis=1, how='all').dropna(axis=0, how='all')
delivery = delivery.dropna(axis=1, how='all').dropna(axis=0, how='all')

# Remove duplicates
sales.drop_duplicates(inplace=True)
menu.drop_duplicates(inplace=True)
employees.drop_duplicates(inplace=True)
delivery.drop_duplicates(inplace=True)

print("✅ Sales shape:", sales.shape)
print("✅ Menu shape:", menu.shape)
print("✅ Employee shape:", employees.shape)
print("✅ Delivery shape:", delivery.shape)
print("✅ Data cleaned successfully!")
