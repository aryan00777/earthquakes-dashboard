import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Earthquake Data Explorer')
st.text('Upload your dataset from file to view the data ')

uploaded_file = st.file_uploader('Upload your CSV file here')

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert numeric columns
    numeric_cols = ['location.depth', 'impact.magnitude', 'location.latitude', 'location.distance', 'time.year']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop missing values
    clean_df = df.dropna(subset=['location.depth', 'impact.magnitude'])

    # ---------------- PREVIEW ----------------
    st.header('Data Preview')
    st.write(df.head())

    st.header('Data Statistics')
    st.write(df.describe())

    # ---------------- 1. DEPTH vs MAGNITUDE ----------------
    st.subheader("Depth vs Magnitude")

    fig1, ax1 = plt.subplots()
    ax1.scatter(clean_df['location.depth'], clean_df['impact.magnitude'])
    ax1.set_xlabel('Depth')
    ax1.set_ylabel('Magnitude')
    st.pyplot(fig1)

    # ---------------- 2. MAGNITUDE DISTRIBUTION ----------------
    st.subheader("Magnitude Distribution")

    fig2, ax2 = plt.subplots()
    ax2.hist(clean_df['impact.magnitude'], bins=20)
    ax2.set_xlabel('Magnitude')
    ax2.set_ylabel('Frequency')
    st.pyplot(fig2)

    # ---------------- 3. TOP LOCATIONS ----------------
    st.subheader("Top 10 Earthquake Locations")

    top_locations = df['location.name'].value_counts().head(10)

    fig3, ax3 = plt.subplots()
    ax3.bar(top_locations.index, top_locations.values)
    ax3.set_xlabel('Location')
    ax3.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # ---------------- 4. LATITUDE vs MAGNITUDE ----------------
    st.subheader("Latitude vs Magnitude")

    fig4, ax4 = plt.subplots()
    ax4.scatter(clean_df['location.latitude'], clean_df['impact.magnitude'])
    ax4.set_xlabel('Latitude')
    ax4.set_ylabel('Magnitude')
    st.pyplot(fig4)

    # ---------------- 5. DISTANCE vs MAGNITUDE ----------------
    st.subheader("Distance vs Magnitude")

    fig5, ax5 = plt.subplots()
    ax5.scatter(clean_df['location.distance'], clean_df['impact.magnitude'])
    ax5.set_xlabel('Distance')
    ax5.set_ylabel('Magnitude')
    st.pyplot(fig5)

    # ---------------- 6. DEPTH BUCKET ANALYSIS ----------------
    st.subheader("Earthquake Count by Depth Range")

    # Create depth bins
    bins = [0, 50, 100, 300, 700]
    labels = ['0-50', '50-100', '100-300', '300-700']
    df['depth_range'] = pd.cut(df['location.depth'], bins=bins, labels=labels)

    depth_counts = df['depth_range'].value_counts().sort_index()

    fig6, ax6 = plt.subplots()
    ax6.bar(depth_counts.index.astype(str), depth_counts.values)
    ax6.set_xlabel('Depth Range')
    ax6.set_ylabel('Number of Earthquakes')
    st.pyplot(fig6)

    # ---------------- 7. HIGH vs LOW MAGNITUDE COMPARISON ----------------
    st.subheader("High vs Low Magnitude Earthquakes")

    df['magnitude_category'] = df['impact.magnitude'].apply(
        lambda x: 'High' if x >= 5 else 'Low'
    )

    mag_counts = df['magnitude_category'].value_counts()

    fig7, ax7 = plt.subplots()
    ax7.pie(mag_counts.values, labels=mag_counts.index, autopct='%1.1f%%')
    st.pyplot(fig7)

else:
    st.info("Please upload a CSV file to begin.")