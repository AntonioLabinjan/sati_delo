from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import re

raw_input = """
7. mjesec 
14.7.2025. 8-15
15.7.2025. 8-15  
16.7.2025. 8-15
17.7.2025. 8-15
18.7.2025. 8-15
21.7.2025. 8-15:30
22.7.2025. 8-15:30
23.7.2025. 8-15:30
24.7.2025. 8-15:30
25.7.2025. 8-15:30
28.7.2025. 8-15:30
29.7.2025. 8-15:30
30.7.2025. 8-16
31.7.2025. 8-16
"""

pattern = re.compile(
    r'(\d{1,2}\.\d{1,2}\.\d{4})\.\s+(\d{1,2})(?::(\d{2}))?-(\d{1,2})(?::(\d{2}))?'
)
entries = []

for line in raw_input.splitlines():
    line = line.strip()
    match = pattern.match(line)
    if match:
        date_str, start_hour, start_minute, end_hour, end_minute = match.groups()
        date = datetime.strptime(date_str, '%d.%m.%Y')
        start_minute = int(start_minute) if start_minute else 0
        end_minute = int(end_minute) if end_minute else 0
        start = datetime(year=date.year, month=date.month, day=date.day, hour=int(start_hour), minute=start_minute)
        end = datetime(year=date.year, month=date.month, day=date.day, hour=int(end_hour), minute=end_minute)
        hours = round((end - start).total_seconds() / 3600, 2)
        entries.append((
            date.strftime('%d.%m.%Y'),
            f"{start.hour}:{start.minute:02d}",
            f"{end.hour}:{end.minute:02d}",
            hours
        ))

def generate_pdf(entries, mjesec, output_path='Satnica.pdf'):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Satnica za {mjesec}", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [['Datum', 'Pocetak', 'Kraj', 'Broj sati']] + [
        [e[0], e[1], e[2], f"{e[3]:.2f}"] for e in entries
    ]
    total = sum(e[3] for e in entries)
    data.append(['', '', 'Ukupno:', f'{total:.2f}'])

    table = Table(data, colWidths=[100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    print(f"PDF generiran: {output_path}")

generate_pdf(entries, mjesec="7. mjesec", output_path="Satnica_7_mjesec.pdf")
