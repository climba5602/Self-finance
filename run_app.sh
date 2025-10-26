{\rtf1\ansi\ansicpg950\cocoartf2866
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/bin/bash\
\
echo "========================================"\
echo " Elderly Homes Filter Tool"\
echo "========================================"\
\
# Check if Python is installed\
if ! command -v python3 &> /dev/null\
then\
    echo "ERROR: Python is not installed"\
    echo "Please install Python 3.8 or higher"\
    exit 1\
fi\
\
# Check if dependencies are installed\
echo "Checking dependencies..."\
if ! pip3 show streamlit &> /dev/null\
then\
    echo "Installing dependencies..."\
    pip3 install -r requirements.txt\
fi\
\
# Run the Streamlit app\
echo ""\
echo "Opening application in browser..."\
echo "Press Ctrl+C to stop the application"\
echo ""\
streamlit run elderly_homes_app.py\
}