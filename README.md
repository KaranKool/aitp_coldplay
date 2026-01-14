# Coldplay Sentiment analysis Tracker

## How to run
Execute the code block in colab
```
!pip install -q supabase gradio nltk plotly pandas

import requests

url = "https://raw.githubusercontent.com/KaranKool/aitp_coldplay/refs/heads/main/pulse_portal.py"
with open("pulse_portal.py", "w") as f:
    f.write(requests.get(url).text)

# 3. Launch the app
%run pulse_portal.py
```
