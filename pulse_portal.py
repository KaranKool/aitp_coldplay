# @title 🚀 Launch Pulse Portal (All Data / No Filter)
# 1. INSTALL DEPENDENCIES
import os
import sys

# 2. IMPORTS
import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from supabase import create_client, Client
import requests

# 3. SETUP & CONFIGURATION
# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# Supabase Credentials
SUPABASE_URL = "https://eoplegdvqvsaiaxjrdvb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvcGxlZ2R2cXZzYWlheGpyZHZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgyMTQ2MDAsImV4cCI6MjA4Mzc5MDYwMH0.pOWycrOHt8oAEKjXVwvAzF0g4wS4MMs-D2hRUBrODT0"

# Initialize Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 4. ASSETS (Logo & CSS)
LOGO_URL = "https://raw.githubusercontent.com/KaranKool/aitp_coldplay/main/pulse_portal_logo.png"

# Fetch CSS
try:
    css_response = requests.get("https://raw.githubusercontent.com/KaranKool/aitp_coldplay/refs/heads/main/style.py")
    if css_response.status_code == 200:
        raw_text = css_response.text
        if 'css = """' in raw_text:
            CUSTOM_CSS = raw_text.split('css = """')[1].split('"""')[0]
        else:
            CUSTOM_CSS = raw_text
    else:
        CUSTOM_CSS = ""
except:
    CUSTOM_CSS = ""

# --- CSS FIX FOR TABLE WRAPPING ---
CUSTOM_CSS += """
.gradio-container td {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    vertical-align: top !important;
}
td {
    max-width: 500px !important;
}
"""

# 5. DATA FUNCTIONS
def fetch_and_analyze():
    print(f"--- TRIGGERED REFRESH: ALL DATA ---")
    try:
        # 1. Fetch Comments
        comments_response = supabase.table("comments").select("*").execute()
        comments_df = pd.DataFrame(comments_response.data)

        # 2. Fetch Videos
        videos_response = supabase.table("videos").select("*").execute()
        videos_df = pd.DataFrame(videos_response.data)

        # DEBUG: Check if data exists
        if comments_df.empty:
            print("❌ No comments found in DB.")
            return None, None, "No data found.", pd.DataFrame()
        if videos_df.empty:
            print("❌ No videos found in DB.")
            return None, None, "No video metadata found.", pd.DataFrame()

        # 3. CLEAN & MERGE
        # Force IDs to string to ensure they match
        comments_df['video_id'] = comments_df['video_id'].astype(str).str.strip()
        videos_df['video_id'] = videos_df['video_id'].astype(str).str.strip()
        
        # Merge
        merged_df = pd.merge(comments_df, videos_df, on='video_id', how='left')
        print(f"✅ Merge Complete. Total rows: {len(merged_df)}")

        if merged_df.empty:
            print("⚠️ Result is empty after merge.")
            return None, None, "### No data found.", pd.DataFrame()

        # 4. ANALYSIS
        merged_df['compound'] = merged_df['comment'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])
        merged_df['sentiment_type'] = merged_df['compound'].apply(lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral'))

        # 5. CHARTS
        # Pie Chart
        sentiment_counts = merged_df['sentiment_type'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig_pie = px.pie(sentiment_counts, values='Count', names='Sentiment',
                         title='<b>Total Sentiment Distribution</b>',
                         color='Sentiment',
                         color_discrete_map={'Positive':'#00cc96', 'Negative':'#EF553B', 'Neutral':'#636efa'})
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        # Line Chart
        merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'])
        time_df = merged_df.set_index('timestamp').resample('D')['compound'].mean().reset_index()
        fig_line = px.line(time_df, x='timestamp', y='compound', markers=True,
                           title='<b>Average Sentiment Over Time</b>')
        fig_line.add_hline(y=0.05, line_dash="dash", line_color="green", annotation_text="Positive Threshold")
        fig_line.add_hline(y=-0.05, line_dash="dash", line_color="red", annotation_text="Negative Threshold")
        fig_line.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Sentiment Score")

        # 6. DRILL DOWN
        # Handle cases with fewer than 2 comments
        n_largest = min(2, len(merged_df))
        top_pos = merged_df.nlargest(n_largest, 'compound')[['author', 'comment', 'compound']]
        top_neg = merged_df.nsmallest(n_largest, 'compound')[['author', 'comment', 'compound']]

        drill_down_md = "### 🔥 Top Positive Comments\n"
        for _, row in top_pos.iterrows():
            drill_down_md += f"> **@{row['author']}**: *\"{row['comment']}\"* (Score: {row['compound']})\n\n"

        drill_down_md += "---\n### ❄️ Top Negative Comments\n"
        for _, row in top_neg.iterrows():
            drill_down_md += f"> **@{row['author']}**: *\"{row['comment']}\"* (Score: {row['compound']})\n\n"

        # Table
        table_df = merged_df[['timestamp', 'author', 'comment', 'sentiment_type', 'compound']].copy()
        table_df.columns = ["Timestamp", "Author", "Comment", "Sentiment Class", "VADER Score"]
        table_df['Timestamp'] = table_df['Timestamp'].astype(str)

        return fig_pie, fig_line, drill_down_md, table_df

    except Exception as e:
        print(f"❌ Error in logic: {e}")
        return None, None, f"Error: {e}", pd.DataFrame()

# 6. GRADIO UI
with gr.Blocks(css=CUSTOM_CSS, title="Pulse Portal") as demo:

    # --- Header ---
    with gr.Row(elem_id="header-row"):
        with gr.Column(scale=1):
            gr.Image(
                value=LOGO_URL,
                show_label=False,
                show_download_button=False,
                show_fullscreen_button=False,
                container=False,
                width=150,
                interactive=False
            )
        with gr.Column(scale=4):
            gr.Markdown("# 🎵 Pulse Portal: Coldplay Sentiment Tracker\n### Real-time stakeholder monitoring dashboard")

    # --- Controls ---
    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh Data", variant="primary")

    # --- Visuals ---
    with gr.Row():
        with gr.Column():
            plot_pie = gr.Plot(label="Sentiment Ratio")
        with gr.Column():
            plot_line = gr.Plot(label="Sentiment Trend")

    # --- Drill Down & Data ---
    with gr.Tabs():
        with gr.TabItem("🔍 Deep Dive"):
            drill_down_output = gr.Markdown("Click Refresh to load analysis...")

        with gr.TabItem("📋 Raw Data Inspector"):
            raw_data_table = gr.Dataframe(
                headers=["Timestamp", "Author", "Comment", "Sentiment Class", "VADER Score"],
                interactive=False,
                wrap=True
            )

    # --- Logic ---
    # Trigger on load
    demo.load(fetch_and_analyze, inputs=None, outputs=[plot_pie, plot_line, drill_down_output, raw_data_table])
    # Trigger on button
    refresh_btn.click(fetch_and_analyze, inputs=None, outputs=[plot_pie, plot_line, drill_down_output, raw_data_table])

# 7. LAUNCH
if __name__ == "__main__":
    demo.launch(debug=True, share=True)
