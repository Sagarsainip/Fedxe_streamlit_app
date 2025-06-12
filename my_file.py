import streamlit as st  
import pandas as pd  
import numpy as np  
import plotly.express as px  
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="FedEx Logistics Dashboard", layout="wide")
st.title("📦 FedEx Logistics Performance Dashboard")

# side bar details ----------------------------------------------------------------   
st.sidebar.title("📚 FedEx Logistics Navigation")

# Sidebar Options
page = st.sidebar.radio(
    "Go to",
    ["🙏 Welcome Page",
     "🔍 Data Distribution Overview",
     "📊 Performance Factor Analysis",
     "📈 Relationship Analysis",
     "📌 Conclusion & Insights"]
)

# side bar to upload the dataset (csv file only) -----------------------------
st.sidebar.title("Upload Dataset")
file = st.sidebar.file_uploader("Upload your CSV", type=["csv"], key="uploader")

# ──────────────────────────────────────────────────────────────
# 📦 Read & Feature‑Engineer (inline)
# ──────────────────────────────────────────────────────────────

if file:
    FedEx_df = pd.read_csv(
        file,
        parse_dates=[
            'PQ First Sent to Client Date',
            'PO Sent to Vendor Date',
            'Scheduled Delivery Date',
            'Delivered to Client Date',
            'Delivery Recorded Date'
        ],
    )

# Creating  a new column for year as categorical for further analysis
    FedEx_df['Delivery Year'] = FedEx_df['Delivered to Client Date'].dt.year

# Calculate delivery lead time in days for further analysis.
    FedEx_df['Lead Time Days'] = (FedEx_df['Delivered to Client Date'] - FedEx_df['Scheduled Delivery Date']).dt.days
else:
    FedEx_df = None


# ───────────────────────────────────────────────────────────────────────────────────────────
# 1️⃣ Welcome Page
# ───────────────────────────────────────────────────────────────────────────────────────────

if page == "🙏 Welcome Page":
    st.title("📦 Welcome to the FedEx Logistics Performance Dashboard")
    
    st.markdown(
        """
**About FedEx Logistics 🚛**  
FedEx Logistics, a subsidiary of FedEx Corporation, specializes in international supply chain solutions, offering services ranging from freight forwarding and customs brokerage to eCommerce logistics and warehousing. As global trade expands, FedEx continues to innovate in delivering reliable, timely, and cost-efficient logistics services worldwide.

---

**📌 Why this Dashboard?**  
This dataset is designed to support the enhancement of **FedEx Logistics' international supply chain** by offering comprehensive information on **purchase orders, shipping options, vendor partnerships, and delivery timelines**.  

In response to the growing demands of eCommerce and expanding global distribution networks, analyzing this data will uncover **operational inefficiencies**, reduce **transportation expenses**, and boost **delivery performance**.  

The ultimate objective is to:
- 📈 Optimize logistics workflows
- 🤝 Elevate customer satisfaction
- 🏆 Sustain a competitive advantage through reliable, timely, and cost-effective delivery services.

---

**📑 Sections in this app:**

- 🙏 **Welcome Page** — Introduction, objective, and dataset download.
- 🔍 **Data Distribution Overview** — Visualize univariate distributions for key logistics variables.
- 📊 **Performance Factor Analysis** — Bivariate analysis to identify operational factors affecting logistics performance.
- 📈 **Relationship Analysis** — Multivariate relationship patterns across key metrics.
- 📌 **Conclusion & Insights** — Actionable takeaways and business recommendations.

---

**📥 Download the FedEx Logistics Dataset**  
You can download the original dataset used for this dashboard from the link below:

👉 [📦 Download FedEx Logistics CSV](https://drive.google.com/file/d/13YUGzfhJcSmDBHqJxGhbFdWnEu7BWgvL/view?usp=drive_link)

> 📂 **Pro Tip:** Use the navigation sidebar on the left to switch between different sections and uncover valuable insights about FedEx’s logistics operations.
        """
    )

# ──────────────────────────────────────────────────────────────
# 2️⃣  "🔍 Data Distribution Overview"
# ──────────────────────────────────────────────────────────────
if page == "🔍 Data Distribution Overview":
    st.title("Understanding the Problem By Analysing the charts")

    if FedEx_df is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown( """1️⃣ Air and Truck shipments dominate overall volume.
                    2️⃣ Most shipment weights are moderate with few heavy outliers.
                    3️⃣ Top 3 countries handle over half of total shipments.
                    4️⃣ Majority of freight costs are moderate with occasional spikes.
                    5️⃣ A few vendors control the majority of orders.
                    6️⃣ Most orders contain 1–3 line items.
                    7️⃣ Shipments are mainly low to mid-value with rare high-value orders.
                    8️⃣ Delivery volumes steadily increase year by year.
                    9️⃣ Most deliveries arrive on time, with few delays.""")    
    
    st.subheader("📊 ***Univariate Analysis by charts:***")

    col1, col2, col3 = st.columns(3)

    with col1:
        shipment_mode_counts = FedEx_df['Shipment Mode'].value_counts().reset_index()
        shipment_mode_counts.columns = ['Shipment Mode', 'Count']
        fig1 = px.pie(shipment_mode_counts, names='Shipment Mode', values='Count',
                      color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                      title="Shipment Mode Distribution",
                      hole=0.4, template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.box(FedEx_df, y="Weight (Kilograms)", template="plotly_white")
        fig2.update_traces(marker_color="#1f77b4", quartilemethod="inclusive")
        fig2.update_layout(title="Shipment Weight Distribution", yaxis_title="Weight (kg)")
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        country_counts = FedEx_df['Country'].value_counts().nlargest(10).reset_index()
        country_counts.columns = ['Country', 'Shipments']
        fig3 = px.bar(country_counts, y="Country", x="Shipments",
                      orientation='h',
                      color_discrete_sequence=['#ff7f0e'],
                      title="Top 10 Countries by Shipment Count",
                      template="plotly_white")
        fig3.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        avg_freight = FedEx_df['Freight Cost (USD)'].mean()
        fig4 = px.histogram(FedEx_df, x="Freight Cost (USD)", nbins=30, template="plotly_white")
        fig4.add_vline(x=avg_freight, line_dash="dash", line_color="#d62728")
        fig4.update_traces(marker_color="#ff7f0e")
        fig4.update_layout(title="Freight Cost Distribution", xaxis_title="Freight Cost (USD)")
        st.plotly_chart(fig4, use_container_width=True)

    with col5:
        vendor_counts = FedEx_df['Vendor'].value_counts().nlargest(10).reset_index()
        vendor_counts.columns = ['Vendor', 'Orders']
        fig5 = px.treemap(vendor_counts, path=['Vendor'], values='Orders',
                          color_discrete_sequence=px.colors.sequential.Blues,
                          title="Top 10 Vendors by Orders")
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        fig6 = px.histogram(FedEx_df, x="Line Item Quantity", nbins=30, template="plotly_white")
        fig6.update_traces(marker_color="#2ca02c")
        fig6.update_layout(title="Line Item Quantity Distribution")
        st.plotly_chart(fig6, use_container_width=True)

    col7, col8, col9 = st.columns(3)

    with col7:
        fig7 = px.box(FedEx_df, y="Line Item Value", template="plotly_white")
        fig7.update_traces(marker_color="#1f77b4", quartilemethod="inclusive")
        fig7.update_layout(title="Line Item Value Distribution", yaxis_title="Value (USD)")
        st.plotly_chart(fig7, use_container_width=True)

    with col8:
        year_counts = FedEx_df['Delivery Year'].value_counts().reset_index()
        year_counts.columns = ['Delivery Year', 'Deliveries']
        fig8 = px.bar(year_counts, x="Delivery Year", y="Deliveries",
                      text_auto=True,
                      color_discrete_sequence=['#ff7f0e'],
                      template="plotly_white",
                      title="Deliveries by Year")
        st.plotly_chart(fig8, use_container_width=True)

    with col9:
        fig9 = px.box(FedEx_df, y="Lead Time Days",
                      template="plotly_white")
        fig9.update_traces(marker_color="#2ca02c", quartilemethod="inclusive")
        fig9.update_layout(title="Delivery Lead Time Distribution", yaxis_title="Lead Time (Days)")
        st.plotly_chart(fig9, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 3️⃣  📊 Performance Factor Analysis
# ──────────────────────────────────────────────────────────────

if page == "📊 Performance Factor Analysis":
    st.title("📊 Factors and Causes Analysis")

    if FedEx_df is None:
        st.warning("➡️ Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown("""
        🚚 This section breaks down key operational factors affecting FedEx's logistics:  
        freight cost patterns, shipment weights, delivery delays, vendor behavior, and more.
    """)

    st.subheader("📊 Key Insights via Bivariate Charts Analysis:")

    # Prepare required fields
    FedEx_df['Lead Time Days'] = (FedEx_df['Delivered to Client Date'] - FedEx_df['Scheduled Delivery Date']).dt.days
    FedEx_df['Shipment Date'] = FedEx_df['PQ First Sent to Client Date'].fillna(FedEx_df['Scheduled Delivery Date'])

    col11, col12, col13 = st.columns(3)

    # 1️⃣ Lead Time Distribution
    with col11:
        fig1 = px.histogram(FedEx_df, x='Lead Time Days', nbins=20, template="plotly_white",
                            color_discrete_sequence=['#4D148C'])
        fig1.update_layout(title="Lead Time Distribution", xaxis_title="Lead Time (Days)")
        st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Freight Cost by Shipment Mode
    with col12:
        fig2 = px.box(FedEx_df, x='Shipment Mode', y='Freight Cost (USD)', color='Fulfill Via',
                      template="plotly_white",
                      color_discrete_sequence=['#4D148C', '#FF6600'])
        fig2.update_layout(title="Freight Cost by Shipment Mode & Fulfill Via")
        st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Shipments Over Time
    with col13:
        shipments_over_time = FedEx_df.resample('ME', on='Shipment Date').size().reset_index(name='Shipments')
        fig3 = px.area(shipments_over_time, x='Shipment Date', y='Shipments',
                       template="plotly_white",
                       color_discrete_sequence=['#FF6600'])
        fig3.update_layout(title="Total Shipments Over Time", xaxis_title="Date")
        st.plotly_chart(fig3, use_container_width=True)

    col14, col15, col16 = st.columns(3)

    # 4️⃣ Avg Weight by Shipment Mode
    with col14:
        avg_weight = FedEx_df.groupby('Shipment Mode')['Weight (Kilograms)'].mean().reset_index()
        fig4 = px.bar(avg_weight, x='Shipment Mode', y='Weight (Kilograms)',
                      template="plotly_white",
                      color_discrete_sequence=['#FF6600'])
        fig4.update_layout(title="Average Weight by Shipment Mode")
        st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ Top 10 Countries by Freight Cost
    with col15:
        top_cost = FedEx_df.groupby('Country')['Freight Cost (USD)'].sum().nlargest(10).reset_index()
        fig5 = px.bar(top_cost, y='Country', x='Freight Cost (USD)',
                      orientation='h', template="plotly_white",
                      color_discrete_sequence=['#4D148C'])
        fig5.update_layout(title="Top 10 Countries by Freight Cost")
        st.plotly_chart(fig5, use_container_width=True)

    # 6️⃣ Quantity vs Freight Cost Scatter
    with col16:
        fig6 = px.scatter(FedEx_df, x='Line Item Quantity', y='Freight Cost (USD)',
                          color='Shipment Mode',
                          template="plotly_white",
                          color_discrete_sequence=['#4D148C', '#FF6600', 'black'])
        fig6.update_layout(title="Quantity vs Freight Cost by Mode")
        st.plotly_chart(fig6, use_container_width=True)

    col17, col18, col19 = st.columns(3)

    # 7️⃣ Delivery Delays by Shipment Mode
    with col17:
        fig7 = px.violin(FedEx_df, x='Shipment Mode', y='Lead Time Days', box=True,
                         template="plotly_white",
                         color_discrete_sequence=['#FF6600'])
        fig7.update_layout(title="Delivery Delays by Shipment Mode")
        st.plotly_chart(fig7, use_container_width=True)


    # 8️⃣ Freight Cost Distribution by Country
    with col18:
      top_10_country_names = FedEx_df['Country'].value_counts().nlargest(10).index
    filtered_df = FedEx_df[
        FedEx_df['Country'].isin(top_10_country_names)
    ].dropna(subset=['Freight Cost (USD)', 'Country'])

    fig8 = px.box(
        filtered_df,
        x='Country',
        y='Freight Cost (USD)',
        template="plotly_white",
        color='Country',
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig8.update_layout(
        title="Freight Cost Distribution by Country",
        xaxis_title="Country",
        yaxis_title="Freight Cost (USD)"
    )

    st.plotly_chart(fig8, use_container_width=True)

    # 9️⃣ Top 10 Countries by Total Weight
    with col19:
        clean_df = FedEx_df.dropna(subset=['Weight (Kilograms)', 'Country'])
        top_weight = clean_df.groupby('Country')['Weight (Kilograms)'].sum().nlargest(10).reset_index()
        fig9 = px.bar(
            top_weight,
            y='Country',
            x='Weight (Kilograms)',
            orientation='h',
            template="plotly_white",
            color_discrete_sequence=['#4D148C']
        )
        fig9.update_layout(
            title="Top 10 Countries by Total Shipment Weight",
            xaxis_title="Total Shipment Weight (kg)",
            yaxis_title="Country"
        )
        st.plotly_chart(fig9, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────
# 3️⃣  "📈 Relationship Analysis"0
# ──────────────────────────────────────────────────────────────────────────────────────────────────────

if page == "📈 Relationship Analysis":
    st.title("📈 Multivariate Analysis")

    if FedEx_df is None:
        st.warning("➡️ Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown("""
    🚚 This section visualizes relationships between multiple variables from FedEx logistics data  
    using advanced multivariate Plotly charts.
    """)

    # Replace NaN values in Weight (Kilograms) with 1 for visualization
    FedEx_df['Weight (Kilograms)'] = FedEx_df['Weight (Kilograms)'].fillna(1)

    # 1️⃣ Scatter Plot: Freight Cost vs Weight, colored by Shipment Mode, sized by Quantity
    st.subheader("📦 Freight Cost vs Weight (by Mode & Quantity)")
    fig1 = px.scatter(
        FedEx_df,
        x="Weight (Kilograms)",
        y="Freight Cost (USD)",
        color="Shipment Mode",
        size="Line Item Quantity",
        template="plotly_white",
        color_discrete_sequence=['#4D148C', '#FF6600', 'black']
    )
    fig1.update_layout(
        title="Freight Cost vs Weight by Shipment Mode & Quantity",
        title_font_size=20,
        title_x=0.5
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Bubble Chart: Freight Cost vs Quantity, bubble size = Weight, color by Fulfill Via
    st.subheader("📊 Freight Cost vs Quantity (Bubble by Weight & Fulfill Via)")
    fig2 = px.scatter(
        FedEx_df,
        x="Line Item Quantity",
        y="Freight Cost (USD)",
        color="Fulfill Via",
        size="Weight (Kilograms)",
        template="plotly_white",
        color_discrete_sequence=['#FF6600', '#4D148C', 'black']
    )
    fig2.update_layout(
        title="Freight Cost vs Quantity (Bubble size = Weight, Color by Fulfill Via)",
        title_font_size=20,
        title_x=0.5
    )
    st.plotly_chart(fig2, use_container_width=True)


if page == "📌 Conclusion & Insights":
    st.title("📌 Conclusion & Insights")

    st.markdown("""
    This section summarizes **key operational insights** and **strategic conclusions** derived from the FedEx logistics data.
    """)

    st.subheader("📊 Operational Insights:")
    insights = [
        "1️⃣ Air is the most frequently used shipment mode.",
        "2️⃣ Majority of orders are fulfilled via Direct Drop.",
        "3️⃣ Vietnam and Côte d'Ivoire lead in shipment volumes.",
        "4️⃣ High-value orders are mostly shipped by Air.",
        "5️⃣ Freight costs rise steeply with shipment weight over 2000 kg.",
        "6️⃣ Most shipments have a lead time of 0 days.",
        "7️⃣ Few shipments exceeding 5000 kg account for major freight costs.",
        "8️⃣ A significant number of shipments have zero insurance recorded.",
        "9️⃣ Aurobindo Pharma and Sun Pharma are the top vendors by volume.",
        "🔟 Shipment volumes show seasonality with peak months."
    ]

    for item in insights:
        st.markdown(f"- {item}")

    st.subheader("📌 Strategic Conclusions:")
    conclusions = [
        "1️⃣ Negotiate better rates for frequently used Air shipments.",
        "2️⃣ Diversify fulfillment modes to reduce dependency risk.",
        "3️⃣ Strengthen logistics and supply chains in top-performing countries.",
        "4️⃣ Explore premium logistics services for high-value air shipments.",
        "5️⃣ Optimize handling for large, heavy shipments to control costs.",
        "6️⃣ Investigate zero-day lead times for accuracy and process validation.",
        "7️⃣ Revise insurance policies for shipments lacking coverage.",
        "8️⃣ Assess vendor dependency and diversify supply sources where needed.",
        "9️⃣ Plan capacity and staffing for seasonal shipment demand peaks.",
        "🔟 Implement tighter data quality checks for operational records."
    ]

    for item in conclusions:
        st.markdown(f"- {item}")
