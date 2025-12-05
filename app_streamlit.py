# app_streamlit.py
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import src.utils as utils

ROOT = Path(".")
DATA = ROOT / "data"
CLEAN = DATA / "cleaned_poll.csv"

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
st.title("📊 Poll Results Visualizer")

# Sidebar: upload or choose synthetic
with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload poll CSV (Google Forms / Excel export)", type=["csv"])
    use_sample = st.button("Use generated sample")
    if uploaded:
        # robust read from uploaded file-like object
        try:
            uploaded.seek(0)
        except Exception:
            pass
        try:
            df = pd.read_csv(uploaded, encoding="utf-8-sig")
        except Exception:
            # fallback
            df = pd.read_csv(uploaded, encoding="latin1")
        st.success("File loaded (preview below).")
        # try to convert timestamp if present
        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            if "Date" not in df.columns:
                df["Date"] = df["Timestamp"].dt.date
    elif use_sample:
        try:
            utils.ensure_clean_exists(generate_if_missing=True)
            df = utils.load_cleaned()
            st.success("Loaded generated sample.")
        except Exception as e:
            st.error("Could not load sample: " + str(e))
            df = pd.DataFrame()
    else:
        # attempt to load cleaned csv on disk (created by preprocess or data_generator)
        try:
            df = utils.load_cleaned()
        except Exception:
            df = pd.DataFrame()

    st.markdown("---")
    st.header("Filters")
    if not df.empty:
        # defensive: some columns may be missing depending on CSV source
        tool_opts = sorted(df.get("Preferred Tool", pd.Series([], dtype=object)).dropna().unique().tolist())
        sel_tools = st.multiselect("Preferred Tool", options=tool_opts, default=tool_opts if tool_opts else [])
        gender_options = sorted(df.get("Gender", pd.Series([], dtype=object)).dropna().unique().tolist())
        sel_gender = st.multiselect("Gender", options=gender_options, default=None)
        min_sat = int(df.get("Satisfaction (1-5)", pd.Series([], dtype=int)).dropna().min() if not df.get("Satisfaction (1-5)", pd.Series([], dtype=int)).dropna().empty else 1)
        max_sat = int(df.get("Satisfaction (1-5)", pd.Series([], dtype=int)).dropna().max() if not df.get("Satisfaction (1-5)", pd.Series([], dtype=int)).dropna().empty else 5)
        sat_range = st.slider("Satisfaction range", min_value=1, max_value=5, value=(min_sat, max_sat))
    else:
        sel_tools = []; sel_gender = None; sat_range = (1,5)

# Main
if df.empty:
    st.info("No data loaded. Click 'Use generated sample' or upload CSV. Run src/data_generator.py and src/preprocess.py to create sample if needed.")
else:
    # apply filters
    dff = df.copy()
    if sel_tools:
        dff = dff[dff.get("Preferred Tool", pd.Series()).isin(sel_tools)]
    if sel_gender:
        dff = dff[dff.get("Gender", pd.Series()) .isin(sel_gender)]
    # coerce satisfaction column safely
    if "Satisfaction (1-5)" in dff.columns:
        dff["Satisfaction (1-5)"] = pd.to_numeric(dff["Satisfaction (1-5)"], errors="coerce")
        dff = dff[dff["Satisfaction (1-5)"].between(sat_range[0], sat_range[1], inclusive="both")]
    else:
        # if satisfaction missing, do not filter by it
        pass

    st.subheader("Dataset preview")
    st.dataframe(dff.head(200))

    # row: charts
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Preference counts")
        pref_counts = dff.get("Preferred Tool", pd.Series([], dtype=object)).value_counts()
        if pref_counts.empty:
            st.write("No 'Preferred Tool' data available.")
        else:
            fig = px.bar(x=pref_counts.index, y=pref_counts.values, labels={'x':'Tool','y':'Count'}, title="Preferred Tool counts")
            st.plotly_chart(fig, width='stretch')

        st.subheader("Satisfaction distribution")
        if "Satisfaction (1-5)" in dff.columns and not dff["Satisfaction (1-5)"].dropna().empty:
            fig2 = px.histogram(dff, x="Satisfaction (1-5)", nbins=5, title="Satisfaction distribution")
            st.plotly_chart(fig2, width='stretch')
        else:
            st.write("No satisfaction data available.")

    with col2:
        st.subheader("Word cloud (Feedback)")
        text = " ".join(dff.get("Feedback", pd.Series([], dtype=str)).astype(str).tolist())
        if text.strip():
            wc = WordCloud(width=600, height=300, background_color='white').generate(text)
            plt.figure(figsize=(6,3))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt.gcf())
            plt.close()
        else:
            st.write("No feedback text available.")

    st.subheader("Responses over time")
    if "Date" in dff.columns:
        # ensure Date is datetime
        dff["Date"] = pd.to_datetime(dff["Date"], errors="coerce")
        daily = dff.dropna(subset=["Date"]).groupby(dff["Date"].dt.date).size().reset_index(name="count")
        if not daily.empty:
            fig3 = px.line(daily, x="Date", y="count", markers=True, title="Responses over time")
            st.plotly_chart(fig3, width='stretch')
        else:
            st.write("No parseable dates found.")
    else:
        st.write("No date column found.")

    st.markdown("---")
    st.subheader("Export filtered data")
    st.download_button("Download CSV of filtered results", data=dff.to_csv(index=False).encode('utf-8'), file_name="poll_filtered.csv")
