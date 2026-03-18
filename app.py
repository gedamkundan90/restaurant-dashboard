import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Restaurant Analytics", page_icon="🍽️", layout="wide")

# Load data
@st.cache_data
def load_data():
    sales = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Sales").dropna(axis=1, how='all').dropna(axis=0, how='all')
    menu = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Menu").dropna(axis=1, how='all').dropna(axis=0, how='all')
    employees = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Employee").dropna(axis=1, how='all').dropna(axis=0, how='all')
    delivery = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Delivery").dropna(axis=1, how='all').dropna(axis=0, how='all')
    return sales, menu, employees, delivery

sales, menu, employees, delivery = load_data()

# Sidebar
st.sidebar.title("🍽️ Restaurant Dashboard")
page = st.sidebar.selectbox("Go to", ["🏠 Home", "📈 Sales", "🍴 Menu", "🛵 Delivery", "👥 Employee"])

# Home Page
if page == "🏠 Home":
    st.title("🍽️ Restaurant Analytics Dashboard")
    st.markdown("Welcome to the Restaurant Data Analytics Website!")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", len(sales))
    col2.metric("Total Revenue", f"₹{sales['Transaction_amount'].sum():,.0f}")
    col3.metric("Menu Items", len(menu))
    col4.metric("Delivery Orders", len(delivery))

# Sales Page
elif page == "📈 Sales":
    st.title("📈 Sales Analysis")

    sales['Date'] = pd.to_datetime(sales['Date'])
    monthly = sales.groupby(sales['Date'].dt.strftime('%Y-%m'))['Transaction_amount'].sum().reset_index()
    fig1 = px.line(monthly, x='Date', y='Transaction_amount', title='Monthly Sales Trend')
    st.plotly_chart(fig1, use_container_width=True)

    top_items = sales.groupby('Item Menu')['Quantity'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_items, x='Item Menu', y='Quantity', title='Top 10 Selling Items')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Filter by Item Type")
    item_type = st.selectbox("Select Item Type", sales['Item_type'].unique())
    filtered = sales[sales['Item_type'] == item_type]
    st.dataframe(filtered)

# Menu Page
elif page == "🍴 Menu":
    st.title("🍴 Menu Analysis")

    fig3 = px.pie(menu, names='Category', values='Profit Margin %', title='Profit Margin by Category')
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(menu.nlargest(10, 'Profit Margin %'), x='Item Name', y='Profit Margin %', title='Top 10 Most Profitable Items')
    st.plotly_chart(fig4, use_container_width=True)

# Delivery Page
elif page == "🛵 Delivery":
    st.title("🛵 Delivery Analysis")

    fig5 = px.pie(delivery, names='Platform', title='Swiggy vs Zomato Orders')
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.bar(delivery, x='Payment Mode', title='Orders by Payment Mode')
    st.plotly_chart(fig6, use_container_width=True)

# Employee Page
elif page == "👥 Employee":
    st.title("👥 Employee Analysis")

    fig7 = px.bar(employees, x='Department', y='Performance Rating ', color='Department', title='Performance by Department')
    st.plotly_chart(fig7, use_container_width=True)

    fig8 = px.box(employees, x='Department', y='Salary', title='Salary Distribution by Department')
    st.plotly_chart(fig8, use_container_width=True)
