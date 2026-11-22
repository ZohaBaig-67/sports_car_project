import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sport Car Price Explorer", page_icon="🏎️", layout="wide")

@st.cache_data
def load_data():
    path = Path(__file__).parent / "sport_car_price.csv"
    raw = pd.read_csv(path)
    data = raw.drop_duplicates().copy()

    engine_text = data["Engine Size (L)"].astype("string").str.strip()
    data["Engine Type"] = "Combustion / unspecified"
    data.loc[engine_text.str.contains("electric", case=False, na=False), "Engine Type"] = "Electric / electric-assisted"
    data.loc[engine_text.str.contains("hybrid", case=False, na=False), "Engine Type"] = "Hybrid"
    data["Engine Size (L)"] = pd.to_numeric(
        engine_text.str.extract(r"(\d+(?:\.\d+)?)", expand=False), errors="coerce"
    )

    for col in ["Horsepower", "Torque (lb-ft)", "Price (in USD)"]:
        s = data[col].astype("string").str.replace(",", "", regex=False)
        data[col] = pd.to_numeric(s.str.extract(r"(\d+(?:\.\d+)?)", expand=False), errors="coerce")

    s = data["0-60 MPH Time (seconds)"].astype("string").str.replace(",", "", regex=False)
    data["0-60 MPH Time (seconds)"] = pd.to_numeric(s.str.extract(r"(\d+(?:\.\d+)?)", expand=False), errors="coerce")
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")

    numeric = ["Year", "Engine Size (L)", "Horsepower", "Torque (lb-ft)",
               "0-60 MPH Time (seconds)", "Price (in USD)"]
    for col in numeric:
        data[col] = data[col].fillna(data[col].median())
    return data

df = load_data()

st.title("🏎️ Inside the World of Sports Cars")
st.caption("Explore how performance specifications, manufacturers, and model years relate to listed sports-car prices.")

st.sidebar.header("Explore the dataset")
makes = sorted(df["Car Make"].dropna().unique().tolist())
selected_makes = st.sidebar.multiselect("Car manufacturer", makes, default=makes)
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Model year", min_year, max_year, (min_year, max_year))

filtered = df[df["Car Make"].isin(selected_makes)]
filtered = filtered[filtered["Year"].between(year_range[0], year_range[1])]

if filtered.empty:
    st.warning("No cars match these filters. Select at least one manufacturer or widen the year range.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Cars in view", f"{len(filtered):,}")
c2.metric("Median price", f"${filtered['Price (in USD)'].median():,.0f}")
c3.metric("Median horsepower", f"{filtered['Horsepower'].median():,.0f} HP")
c4.metric("Manufacturers", f"{filtered['Car Make'].nunique():,}")

st.subheader("Univariate analysis")
a, b = st.columns(2)
with a:
    fig = px.histogram(filtered, x="Price (in USD)", nbins=30, title="Distribution of listed prices",
                       labels={"Price (in USD)": "Price (USD)", "count": "Number of cars"})
    st.plotly_chart(fig, use_container_width=True)
with b:
    counts = filtered["Car Make"].value_counts().head(12).reset_index()
    counts.columns = ["Car Make", "Records"]
    fig = px.bar(counts.sort_values("Records"), x="Records", y="Car Make", orientation="h",
                 title="Most represented manufacturers")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Bivariate analysis")
a, b = st.columns(2)
with a:
    fig = px.scatter(filtered, x="Horsepower", y="Price (in USD)", color="Engine Type",
                     hover_name="Car Model", title="Price versus horsepower",
                     labels={"Horsepower":"Horsepower (HP)", "Price (in USD)":"Price (USD)"})
    st.plotly_chart(fig, use_container_width=True)
with b:
    fig = px.scatter(filtered, x="0-60 MPH Time (seconds)", y="Price (in USD)",
                     color="Car Make", hover_name="Car Model", title="Price versus 0–60 mph time",
                     labels={"0-60 MPH Time (seconds)":"0–60 mph time (seconds)", "Price (in USD)":"Price (USD)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Manufacturer comparison")
top = filtered["Car Make"].value_counts().head(10).index
compare = filtered[filtered["Car Make"].isin(top)]
fig = px.box(compare, x="Car Make", y="Horsepower", title="Horsepower by manufacturer",
             labels={"Car Make":"Manufacturer", "Horsepower":"Horsepower (HP)"})
fig.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation overview")
corr = filtered[["Year", "Engine Size (L)", "Horsepower", "Torque (lb-ft)",
                 "0-60 MPH Time (seconds)", "Price (in USD)"]].corr()
fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, title="Correlation heatmap")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Key findings")
st.markdown(
    f"""
    - Median listed price in the current view is **${filtered['Price (in USD)'].median():,.0f}**.
    - Median horsepower is **{filtered['Horsepower'].median():,.0f} HP**.
    - Price–horsepower correlation is **{filtered['Horsepower'].corr(filtered['Price (in USD)']):.2f}**.
    - The manufacturer with the most records in this view is **{filtered['Car Make'].value_counts().index[0]}**.
    """
)

if st.checkbox("Show raw filtered data"):
    st.dataframe(filtered, use_container_width=True)

st.caption("Data note: exact duplicate rows are removed. Numeric text is parsed; missing numeric values are median-filled. IQR outliers are retained because they may represent genuine high-performance or luxury models.")
