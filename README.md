{\rtf1\ansi\ansicpg950\cocoartf2866
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Elderly Homes Filter & Export Tool\
\
A Streamlit web application to filter and export elderly residential care home data by District and Type of Place.\
\
## Features\
\
- Multi-select District Filter: Choose one or multiple districts (\uc0\u22320 \u21312 )\
- Type of Place Filter: Filter by Care-and-Attention and/or Nursing Home\
- Data Display: View filtered results in an interactive table\
- CSV Export: Download filtered data as CSV\
- PDF Export: Generate and download filtered data as a formatted PDF report\
\
## Installation\
\
### Step 1: Install Python Dependencies\
\
pip install -r requirements.txt\
\
Or manually:\
\
pip install streamlit pandas reportlab openpyxl\
\
### Step 2: Prepare Your Data\
\
Make sure the following files are in the same directory as the app:\
- elderly_homes_app.py\
- elderly_homes_combined_filtered.csv\
- requirements.txt\
\
## Running the App\
\
streamlit run elderly_homes_app.py\
\
The app will open in your browser at http://localhost:8501\
\
---\
\
## Usage\
s\
1. Select Districts in the sidebar\
2. Select Type of Place filter\
3. View results\
4. Export CSV or PDF\
\
---\
\
## Troubleshooting\
\
Check Dependencies are installed\
\
Ensure CSV is in the same folder and accessible\
\
---\
\
## System Requirements\
\
Python 3.8 or higher, modern web browser\
}