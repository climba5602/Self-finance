import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch, mm
from io import BytesIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register your font - ensure font file exists with this name/path
pdfmetrics.registerFont(TTFont('NotoSansCJKtc', 'NotoSansTC-Regular.ttf'))

st.set_page_config(page_title="Elderly Homes Filter Tool", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('elderly_homes_combined_filtered.csv')
        df['District'] = df['District'].fillna('').astype(str)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def generate_pdf(data, districts):
    margin = 15 * mm
    page_width, page_height = landscape(A4)
    available_width = page_width - 2 * margin

    original_widths = [1.5*inch, 3.0*inch, 3.5*inch, 1.2*inch, 1.0*inch, 1.0*inch, 1.0*inch]
    total_original_width = sum(original_widths)

    scale_factor = available_width / total_original_width
    col_widths = [w * scale_factor for w in original_widths]

    max_rows_per_page = 6

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    elements = []
    styles = getSampleStyleSheet()
    font_name = 'NotoSansCJKtc'

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName=font_name,
                                 fontSize=15, textColor=colors.black, alignment=1, spaceAfter=12)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontName=font_name,
                                    fontSize=15, textColor=colors.black, alignment=1, spaceAfter=20)
    wrap_style = ParagraphStyle('Wrap', fontName=font_name, fontSize=13, leading=15,
                                wordWrap='CJK', alignment=0, spaceAfter=4, textColor=colors.black, valign='top')

    title = Paragraph(
        "提供資助安老服務宿位的津助安老院、合約院舍、自負盈虧安老院名單 List of Subvented Homes, Self-financing Homes and Contract Homes Providing Subsidised Places for the Elderly",
        title_style)

    districts_str = ", ".join(districts)
    subtitle = Paragraph(f"地區: {districts_str}", subtitle_style)

    headers = ['地區\nDistrict', '院舍名稱\nName', '地址\nAddress', '電話\nTel', '護理安老宿位\nC&A',
               '護養院宿位\nNH', '總數\nTotal']

    for start in range(0, len(data), max_rows_per_page):
        elements.append(title)
        elements.append(subtitle)
        elements.append(Spacer(1, 0.2 * inch))

        table_data = [[Paragraph(h, wrap_style) for h in headers]]

        for _, row in data.iloc[start:start + max_rows_per_page].iterrows():
            district_lines = str(row['District']).split('\\n')
            district_text = "\n".join(district_lines) if len(district_lines) > 1 else str(row['District'])

            name_lines = str(row['Name']).split('\\n')
            name_text = "\n".join(name_lines) if len(name_lines) > 1 else str(row['Name'])

            address_lines = str(row['Address']).split('\\n')
            address_text = "\n".join(address_lines) if len(address_lines) > 1 else str(row['Address'])

            tel = str(row['Tel'])
            care = str(int(row['Care_and_Attention'])) if row['Care_and_Attention'] > 0 else '-'
            nursing = str(int(row['Nursing_Home'])) if row['Nursing_Home'] > 0 else '-'
            total = str(int(row['Total'])) if pd.notna(row['Total']) else '-'

            table_data.append([
                Paragraph(district_text, wrap_style),
                Paragraph(name_text, wrap_style),
                Paragraph(address_text, wrap_style),
                Paragraph(tel, wrap_style),
                Paragraph(care, wrap_style),
                Paragraph(nursing, wrap_style),
                Paragraph(total, wrap_style),
            ])

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 15),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 13),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))

        elements.append(table)
        if start + max_rows_per_page < len(data):
            elements.append(PageBreak())

    doc.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value


df = load_data()

if df is not None:
    st.sidebar.header("🔍 Filters")
    districts = sorted(df['District'].fillna('').astype(str).unique())

    selected_districts = st.sidebar.multiselect(
        "地區 District:", options=districts, default=districts[:3]
    )

    st.sidebar.subheader("宿位種類 Type of Place")
    show_care_attention = st.sidebar.checkbox("護理安老宿位 C&A", value=True)
    show_nursing_home = st.sidebar.checkbox("護養院宿位 NH", value=True)

    filtered_df = df[df['District'].isin(selected_districts)].copy()

    if show_care_attention and show_nursing_home:
        type_filtered_df = filtered_df[(filtered_df['Care_and_Attention'] > 0) | (filtered_df['Nursing_Home'] > 0)]
    elif show_care_attention:
        type_filtered_df = filtered_df[filtered_df['Care_and_Attention'] > 0]
    elif show_nursing_home:
        type_filtered_df = filtered_df[filtered_df['Nursing_Home'] > 0]
    else:
        type_filtered_df = pd.DataFrame()

    st.sidebar.markdown("---")
    st.sidebar.metric("總記錄 Total Records", len(type_filtered_df))

    if len(type_filtered_df) > 0:
        st.success(f"找到 **{len(type_filtered_df)}** 筆記錄符合您的條件")
        st.subheader("篩選結果")

        display_cols = ['District', 'Name', 'Address', 'Tel', 'Care_and_Attention', 'Nursing_Home', 'Total']
        st.dataframe(type_filtered_df[display_cols].style.set_properties(**{'font-size': '14pt'}), use_container_width=True, height=500)

        st.markdown("---")
        st.subheader("匯出選項")

        col1, col2 = st.columns(2)

        with col1:
            csv = type_filtered_df[display_cols].to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="下載 CSV",
                data=csv,
                file_name="elderly_homes_filtered.csv",
                mime="text/csv"
            )

        with col2:
            if st.button("生成並下載 PDF"):
                with st.spinner("正在生成 PDF..."):
                    pdf_buffer = generate_pdf(type_filtered_df, selected_districts)
                    st.download_button(
                        label="下載 PDF",
                        data=pdf_buffer,
                        file_name="elderly_homes_filtered.pdf",
                        mime="application/pdf"
                    )
    else:
        st.warning("未找到符合條件的記錄，請調整篩選器。")
else:
    st.error("無法載入資料，請確保 'elderly_homes_combined_filtered.csv' 與程式在同一目錄")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: grey; font-size: 0.8em;'>
<p>資料來源: 提供非資助安老服務宿位的院舍名單</p>
</div>
""", unsafe_allow_html=True)
