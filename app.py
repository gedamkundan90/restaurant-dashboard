import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🍽️ Fine Dine Analytics", page_icon="🍽️", layout="wide")

# ── THEME TOGGLE ──
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

col_toggle, _ = st.columns([1, 9])
with col_toggle:
    mode = st.toggle("🌙 Dark", value=st.session_state.dark_mode)
    st.session_state.dark_mode = mode

if st.session_state.dark_mode:
    bg = "#0D0D0D"
    card = "#1A1A2E"
    card2 = "#16213E"
    text = "#F0E6FF"
    accent = "#9B59B6"
    gold = "#F1C40F"
    green = "#2ECC71"
    blue = "#3498DB"
    brown = "#A0522D"
    plotly_theme = "plotly_dark"
    sidebar_bg = "#16213E"
    grid_color = "rgba(155,89,182,0.15)"
    accent_border = "rgba(155,89,182,0.27)"
    gold_border = "rgba(241,196,15,0.27)"
    accent_fill = "rgba(155,89,182,0.2)"
else:
    bg = "#FAF8FF"
    card = "#F3E8FF"
    card2 = "#EAF4FB"
    text = "#2C3E50"
    accent = "#8E44AD"
    gold = "#D4AC0D"
    green = "#27AE60"
    blue = "#2980B9"
    brown = "#795548"
    plotly_theme = "plotly_white"
    sidebar_bg = "#F3E8FF"
    grid_color = "rgba(142,68,173,0.15)"
    accent_border = "rgba(142,68,173,0.27)"
    gold_border = "rgba(212,172,13,0.27)"
    accent_fill = "rgba(142,68,173,0.2)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Lato', sans-serif;
        background-color: {bg};
        color: {text};
    }}
    .main {{ background-color: {bg}; }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 2px solid {accent};
    }}

    h1 {{
        font-family: 'Playfair Display', serif;
        color: {gold};
        font-size: 2.8rem;
        letter-spacing: 2px;
        text-align: center;
    }}
    h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: {accent};
        letter-spacing: 1px;
    }}

    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, {card}, {card2});
        border-radius: 16px;
        padding: 18px 20px;
        border-left: 5px solid {gold};
        box-shadow: 0 4px 20px rgba(155,89,182,0.2);
        margin-bottom: 10px;
    }}
    div[data-testid="stMetricLabel"] {{ color: {accent} !important; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; }}
    div[data-testid="stMetricValue"] {{ color: {gold} !important; font-size: 1.8rem; font-weight: 700; }}

    .page-title {{
        text-align: center;
        padding: 20px 0 10px 0;
        border-bottom: 2px solid {gold_border};
        margin-bottom: 30px;
    }}
    .divider {{
        height: 2px;
        background: linear-gradient(to right, transparent, {accent}, {gold}, {accent}, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }}
    </style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    sales = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Sales").dropna(axis=1, how='all').dropna(axis=0, how='all')
    menu = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Menu").dropna(axis=1, how='all').dropna(axis=0, how='all')
    employees = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Employee").dropna(axis=1, how='all').dropna(axis=0, how='all')
    delivery = pd.read_excel("data(AutoRecovered).xlsx", sheet_name="Delivery").dropna(axis=1, how='all').dropna(axis=0, how='all')
    return sales, menu, employees, delivery

sales, menu, employees, delivery = load_data()
sales['Date'] = pd.to_datetime(sales['Date'])

COLORS = [accent, gold, green, blue, brown, "#E74C3C", "#1ABC9C", "#E67E22"]

# ── SIDEBAR ──
st.sidebar.markdown(f"""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-size: 3rem;'>🍽️</div>
        <div style='font-family: Playfair Display, serif; font-size: 1.3rem; color: {gold}; font-weight: 700;'>Fine Dine</div>
        <div style='font-size: 0.75rem; color: {accent}; letter-spacing: 3px; text-transform: uppercase;'>Analytics Suite</div>
    </div>
    <div style='height:1px; background: linear-gradient(to right, transparent, {gold}, transparent); margin-bottom: 20px;'></div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["🏠  Overview", "📈  Sales", "🍴  Menu", "🛵  Delivery", "👥  Employee"])

st.sidebar.markdown(f"""
    <div style='text-align: center; margin-top: 40px;'>
        <div style='height:1px; background: linear-gradient(to right, transparent, {gold}, transparent); margin-bottom: 15px;'></div>
        <div style='font-size: 0.7rem; color: {accent}; letter-spacing: 2px;'>★ FIVE STAR EXPERIENCE ★</div>
    </div>
""", unsafe_allow_html=True)

def luxury_chart(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Lato', color=text),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
    )
    fig.update_xaxes(gridcolor=grid_color, showgrid=True)
    fig.update_yaxes(gridcolor=grid_color, showgrid=True)
    return fig

# ══════════════════════════════
# 🏠 OVERVIEW PAGE
# ══════════════════════════════
if "Overview" in page:
    st.markdown(f"""
        <div class='page-title'>
            <h1>🍽️ Fine Dine Analytics</h1>
            <p style='color:{accent}; letter-spacing: 3px; font-size: 0.85rem;'>★ RESTAURANT INTELLIGENCE DASHBOARD ★</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧾 Total Orders", f"{len(sales):,}")
    c2.metric("💰 Total Revenue", f"₹{sales['Transaction_amount'].sum():,.0f}")
    c3.metric("🍱 Menu Items", len(menu))
    c4.metric("🛵 Deliveries", len(delivery))

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3>📈 Revenue Trend</h3>", unsafe_allow_html=True)
        monthly = sales.groupby(sales['Date'].dt.strftime('%Y-%m'))['Transaction_amount'].sum().reset_index()
        fig = px.area(monthly, x='Date', y='Transaction_amount',
                     color_discrete_sequence=[accent],
                     template=plotly_theme)
        fig.update_traces(fill='tozeroy', fillcolor=accent_fill, line_color=gold)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col2:
        st.markdown(f"<h3>🛵 Platform Split</h3>", unsafe_allow_html=True)
        fig = px.pie(delivery, names='Platform',
                    color_discrete_sequence=[accent, gold],
                    template=plotly_theme, hole=0.55)
        fig.update_traces(textfont_size=14)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"<h3>🍽️ Top Selling Items</h3>", unsafe_allow_html=True)
        top = sales.groupby('Item Menu')['Quantity'].sum().nlargest(8).reset_index()
        fig = px.bar(top, x='Quantity', y='Item Menu', orientation='h',
                    color='Quantity',
                    color_continuous_scale=[[0, brown], [0.5, accent], [1, gold]],
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col4:
        st.markdown(f"<h3>📊 Category Profit</h3>", unsafe_allow_html=True)
        cat = menu.groupby('Category')['Profit Margin %'].mean().reset_index()
        fig = px.bar(cat, x='Category', y='Profit Margin %',
                    color='Profit Margin %',
                    color_continuous_scale=[[0, green], [0.5, blue], [1, accent]],
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

# ══════════════════════════════
# 📈 SALES PAGE
# ══════════════════════════════
elif "Sales" in page:
    st.markdown(f"<div class='page-title'><h1>📈 Sales Analysis</h1></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Revenue", f"₹{sales['Transaction_amount'].sum():,.0f}")
    c2.metric("📦 Qty Sold", f"{sales['Quantity'].sum():,}")
    c3.metric("⭐ Avg Rating", f"{sales['Feedback_Rating'].mean():.1f}/5")
    c4.metric("🧾 Orders", len(sales))

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown(f"<h3>📅 Monthly Revenue</h3>", unsafe_allow_html=True)
    monthly = sales.groupby(sales['Date'].dt.strftime('%Y-%m'))['Transaction_amount'].sum().reset_index()
    fig = px.bar(monthly, x='Date', y='Transaction_amount',
                color='Transaction_amount',
                color_continuous_scale=[[0, brown], [0.5, accent], [1, gold]],
                template=plotly_theme)
    st.plotly_chart(luxury_chart(fig), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3>🏆 Top 10 Items</h3>", unsafe_allow_html=True)
        top = sales.groupby('Item Menu')['Quantity'].sum().nlargest(10).reset_index()
        fig = px.bar(top, x='Quantity', y='Item Menu', orientation='h',
                    color='Quantity',
                    color_continuous_scale=[[0, green], [1, blue]],
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col2:
        st.markdown(f"<h3>💳 Transaction Types</h3>", unsafe_allow_html=True)
        trans = sales['Transaction_type'].value_counts().reset_index()
        fig = px.pie(trans, names='Transaction_type', values='count',
                    color_discrete_sequence=COLORS,
                    template=plotly_theme, hole=0.5)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    st.markdown(f"<h3>⭐ Rating Distribution</h3>", unsafe_allow_html=True)
    fig = px.histogram(sales, x='Feedback_Rating', nbins=5,
                      color_discrete_sequence=[accent],
                      template=plotly_theme)
    fig.update_traces(marker_line_color=gold, marker_line_width=1.5)
    st.plotly_chart(luxury_chart(fig), use_container_width=True)

# ══════════════════════════════
# 🍴 MENU PAGE
# ══════════════════════════════
elif "Menu" in page:
    st.markdown(f"<div class='page-title'><h1>🍴 Menu Analysis</h1></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("🍱 Total Items", len(menu))
    c2.metric("💹 Avg Profit", f"{menu['Profit Margin %'].mean():.1f}%")
    c3.metric("🔥 Avg Calories", f"{menu['Calories'].mean():.0f} kcal")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3>📊 Profit by Category</h3>", unsafe_allow_html=True)
        cat = menu.groupby('Category')['Profit Margin %'].mean().reset_index()
        fig = px.bar(cat, x='Category', y='Profit Margin %',
                    color='Profit Margin %',
                    color_continuous_scale=[[0, green], [0.5, blue], [1, accent]],
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col2:
        st.markdown(f"<h3>🥧 Category Distribution</h3>", unsafe_allow_html=True)
        fig = px.pie(menu, names='Category',
                    color_discrete_sequence=COLORS,
                    template=plotly_theme, hole=0.45)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    st.markdown(f"<h3>💰 Price vs Profit Margin</h3>", unsafe_allow_html=True)
    fig = px.scatter(menu, x='Price', y='Profit Margin %',
                    color='Category', size='Calories',
                    hover_name='Item Name',
                    color_discrete_sequence=COLORS,
                    template=plotly_theme)
    fig.update_traces(marker=dict(line=dict(width=1, color=gold)))
    st.plotly_chart(luxury_chart(fig), use_container_width=True)

    st.markdown(f"<h3>🏆 Top 10 Profitable Items</h3>", unsafe_allow_html=True)
    top = menu.nlargest(10, 'Profit Margin %')
    fig = px.bar(top, x='Item Name', y='Profit Margin %',
                color='Profit Margin %',
                color_continuous_scale=[[0, brown], [0.5, accent], [1, gold]],
                template=plotly_theme)
    st.plotly_chart(luxury_chart(fig), use_container_width=True)

# ══════════════════════════════
# 🛵 DELIVERY PAGE
# ══════════════════════════════
elif "Delivery" in page:
    st.markdown(f"<div class='page-title'><h1>🛵 Delivery Analysis</h1></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Total Deliveries", len(delivery))
    c2.metric("⭐ Avg Rating", f"{delivery['Customer Rating'].mean():.1f}/5")
    c3.metric("📍 Avg Distance", f"{delivery['Distance (KM)'].mean():.1f} km")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3>🏆 Swiggy vs Zomato</h3>", unsafe_allow_html=True)
        fig = px.pie(delivery, names='Platform',
                    color_discrete_sequence=[accent, gold],
                    template=plotly_theme, hole=0.55)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col2:
        st.markdown(f"<h3>💳 Payment Modes</h3>", unsafe_allow_html=True)
        pay = delivery['Payment Mode'].value_counts().reset_index()
        fig = px.bar(pay, x='Payment Mode', y='count',
                    color='count',
                    color_continuous_scale=[[0, green], [0.5, blue], [1, accent]],
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    st.markdown(f"<h3>📍 Distance vs Customer Rating</h3>", unsafe_allow_html=True)
    fig = px.scatter(delivery, x='Distance (KM)', y='Customer Rating',
                    color='Platform', size='Total Price',
                    color_discrete_sequence=[accent, gold],
                    template=plotly_theme)
    fig.update_traces(marker=dict(line=dict(width=1, color=gold)))
    st.plotly_chart(luxury_chart(fig), use_container_width=True)

# ══════════════════════════════
# 👥 EMPLOYEE PAGE
# ══════════════════════════════
elif "Employee" in page:
    st.markdown(f"<div class='page-title'><h1>👥 Employee Analysis</h1></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Total Staff", len(employees))
    c2.metric("⭐ Avg Performance", f"{employees['Performance Rating '].mean():.1f}/5")
    c3.metric("💰 Avg Salary", f"₹{employees['Salary'].mean():,.0f}")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3>🏆 Performance by Dept</h3>", unsafe_allow_html=True)
        fig = px.bar(employees, x='Department', y='Performance Rating ',
                    color='Department',
                    color_discrete_sequence=COLORS,
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col2:
        st.markdown(f"<h3>👫 Gender Distribution</h3>", unsafe_allow_html=True)
        fig = px.pie(employees, names='Gender',
                    color_discrete_sequence=[accent, gold],
                    template=plotly_theme, hole=0.5)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"<h3>💰 Salary by Department</h3>", unsafe_allow_html=True)
        fig = px.box(employees, x='Department', y='Salary',
                    color='Department',
                    color_discrete_sequence=COLORS,
                    template=plotly_theme)
        st.plotly_chart(luxury_chart(fig), use_container_width=True)

    with col4:
        st.markdown(f"<h3>📋 Attendance vs Performance</h3>", unsafe_allow_html=True)
        fig = px.scatter(employees, x='Attendace', y='Performance Rating ',
                        color='Department',
                        color_discrete_sequence=COLORS,
                        hover_name='Employee Name',
                        template=plotly_theme)
        fig.update_traces(marker=dict(size=10, line=dict(width=1, color=gold)))
        st.plotly_chart(luxury_chart(fig), use_container_width=True)
