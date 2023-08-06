import time
import os
import pandas as pd
from datetime import datetime
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, ImageAndFlowables, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors


def gen_form(folder: str, data: pd.DataFrame):
    file_name = os.path.join(folder, "Count Form " + str(datetime.now().strftime("%Y-%h-%d %H%M%S")) + ".pdf")
    doc = SimpleDocTemplate(file_name,
                            rightMargin=48, leftMargin=48,
                            topMargin=18, bottomMargin=24)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Header',
                              fontName='Times-Roman',
                              fontSize=36,
                              alignment=TA_CENTER,
                              ))
    styles.add(ParagraphStyle(name='Row',
                              fontName='Courier',
                              fontSize=12,
                              alignment=TA_CENTER,
                              ))
    styles.add(ParagraphStyle(name='Desc',
                              fontName='Courier',
                              fontSize=12,
                              alignment=TA_LEFT,
                              ))
    styles.add(ParagraphStyle(name='SKU',
                              fontName='Courier',
                              fontSize=12,
                              alignment=TA_RIGHT,
                              ))

    story = []
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ico', 'hellsing.ico')
    p_text = Paragraph("Short Report Count Form", styles['Header'])
    story.append(ImageAndFlowables(Image(logo, 1.5 * cm, 1.5 * cm), [p_text], imageSide='left'))
    story.append(Spacer(1, 36))

    zone = data.iloc[0]['Zone Code']
    for index, row in data.iterrows():
        if zone != row['Zone Code']:
            story.append(PageBreak())
            story.append(ImageAndFlowables(Image(logo, 1.5 * cm, 1.5 * cm), [p_text], imageSide='left'))
            story.append(Spacer(1, 36))

        zone = row['Zone Code']
        tbl_data = [[Paragraph(str(row['Item No.']) + ":", styles['SKU']),
                     Paragraph(str(row['Item Description']), styles['Desc']),
                     Paragraph(str(row['Zone Code']), styles['Row']),
                     Paragraph(str(row['Bin Code']), styles['Row']),
                     Paragraph('_________________', styles['Row'])]]

        tbl = Table(tbl_data,
                    colWidths=[1 * inch, 3.25 * inch, 0.75 * inch, 1 * inch, 2 * inch],
                    rowHeights=[1 * cm],
                    )
        tbl.setStyle([('VALIGN', (0, 0), (-2, -1), 'MIDDLE')])
        if index % 2 == 0:
            tbl.setStyle([('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)])

        story.append(tbl)

    doc.build(story)
    return doc.filename


def main():
    data = pd.DataFrame([[123456, "THE BIGGEST AND BEST ITEM", "PK", "B999"]],
                        columns=['Item No.', 'Item Description', 'Zone Code', 'Bin Code'])
    gen_form(os.path.dirname(os.path.abspath(__file__)), data)


if __name__ == '__main__':
    main()
