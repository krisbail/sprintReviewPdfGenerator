# coding: utf8

"""
examples of reportlab document using
BaseDocTemplate with
2 PageTemplate (one and two columns)

"""
import os

from belugaReportTemplate import ReportPhoenixTemplate

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import Frame, Paragraph, NextPageTemplate, PageBreak,\
    PageTemplate, Table, TableStyle, Spacer, Image

from testCsv import getSprint, getFixedBug, getFixedDebt, \
    getRetroToKeep, getRetroToImproveAndActions, \
    getOpenBug, getOpenDebt, getVelocity

styles = getSampleStyleSheet()
orangeColor = colors.Color(1, 0.47, 0)
styles.add(ParagraphStyle(name='TitlePage', parent=styles['Normal'], fontSize=32, textColor=orangeColor))
styles.add(ParagraphStyle(name='Link', parent=styles['Normal'], textColor=orangeColor))

#doc = BaseDocTemplate('basedoc.pdf', showBoundary=0, pagesize=landscape(A4))
doc = ReportPhoenixTemplate('basedoc.pdf', showBoundary=0, pagesize=landscape(A4))
doc.sprint = 26

urlStory = "https://www.forge.orange-labs.fr/plugins/tracker/?aid=%s"
urlbug = "https://www.forge.orange-labs.fr/plugins/tracker/?aid=%s"
Elements = []


def firstPage(c, doc):
    c.saveState()
    c.drawImage('/home/coib7363/Documents/phoenix/testPdfPython/orange.jpg', 26.7 * cm, 1 * cm, width=2 * cm, height=2 * cm)
    c.drawImage('/home/coib7363/Documents/phoenix/testPdfPython/phoenix.jpg', 22.7 * cm, 14 * cm, width=6 * cm, height=6 * cm)
    c.setFont("Helvetica-Bold", 62)
    c.setFillColorRGB(1, 0.47, 0)
    c.drawString(2 * cm, 16 * cm, "Sprint Review")
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(9 * cm, 14 * cm, "sprint N° %d" % doc.sprint)
    c.restoreState()

def getLink(url, id):
    url = url % id
    linkurl = "<a href='%s'><u>%s</u></a>" % (url, id)
    return Paragraph(linkurl, styles['Link'])


def review(data):
    if data is None or len(data) == 0:
        data = [{'sprint': 'current', 'aid': 'no data', 'point': 'no data', 'component': 'no data', 'title': 'no data', 'Normal': 'no data'},
                {'sprint': 'next', 'aid': 'no data', 'point': 'no data', 'component': 'no data', 'title': 'no data',
                 'Normal': 'no data'}
                ]
    headings = ('sprint', 'Aid', 'Complexity', 'Component', 'Title')
    index_cell_current_sprint = 0
    stories = []
    currentSprint = data[0]['sprint'] if data[0] else ''
    for p in data:
        url = urlStory % p['aid']
        stories.append((p['sprint'], getLink(urlStory, p['aid']), p['point'], p['component'],
                        Paragraph(p['title'], styles['Normal'])))
        index_cell_current_sprint = index_cell_current_sprint + 1 if currentSprint == p[
            'sprint'] else index_cell_current_sprint

    t = Table([headings] + stories, colWidths=[2 * cm, 2 * cm, 2 * cm, 3 * cm, 16 * cm], repeatRows=1)
    t.setStyle(TableStyle(
        [
            ('LINEBELOW', (0, 1), (-1, -1), 1, colors.lightgrey),
            ('BOX', (0, 1), (0, -1), 1, colors.black),
            ('BOX', (1, 1), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('SPAN', (0, 1), (0, index_cell_current_sprint)),
            ('VALIGN', (0, 1), (0, index_cell_current_sprint), 'MIDDLE'),
            ('LINEBELOW', (0, index_cell_current_sprint), (-1, index_cell_current_sprint), 2, colors.grey),
            ('SPAN', (0, index_cell_current_sprint + 1), (0, -1)),
            ('VALIGN', (0, index_cell_current_sprint + 1), (0, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, index_cell_current_sprint), colors.lightcyan),
        ]))
    return t


def bug(data, color=colors.lightcyan):
    headings = [('Aid', 'Severity', 'Urgency', 'Component', 'Title')]
    bugs = [(getLink(urlbug, bug['aid']), bug['severity'], bug['urgency'], bug['component'],
             Paragraph(bug['title'], styles['Normal']))
            for bug in data]
    t = Table(headings + bugs, colWidths=[2 * cm, 2 * cm, 2 * cm, 3 * cm, 16 * cm], repeatRows=1)
    table_style = [
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                  ]
    oddRowStyle(table_style, bugs, color)
    t.setStyle(TableStyle(table_style))
    return t


def retroToKeep(data=None):
    rowTab = []
    rowTab.append(['To keep'])

    if data is None or len(data) == 0:
        data = [{'to_keep': 'no data'}]
    for row in data:
        rowTab.append([Paragraph(row['to_keep'], styles['Normal'])])
    table_style = [
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]
    oddRowStyle(table_style, rowTab[1:])
    t = Table(rowTab, repeatRows=1, colWidths=[doc.width])
    t.setStyle(TableStyle(table_style))
    return t

def retroToImproveAndActions(data=None):
    headings = [('To improve', 'Actions')]

    if data is None or len(data) == 0:
        data = [{'to_improve': 'no data', 'actions': 'no data'}]

    rowTab = [
                (
                    Paragraph(row['to_improve'], styles['Normal']),
                    Paragraph(row['actions'], styles['Normal'])
                ) for row in data
             ]

    table_style = [
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LINEAFTER', (0, 1), (0, -1), 2, colors.lightgrey),
    ]
    oddRowStyle(table_style, rowTab)
    t = Table(headings + rowTab, repeatRows=1, colWidths=[doc.width / 2, doc.width / 2])
    t.setStyle(TableStyle(table_style))
    return t

def velocity(data=None):
    headings = [('Sprint', 'Velocity', 'Effort', 'Capacity per effort')]

    if data is None or len(data) == 0:
        data = [{'sprint': 'no data', 'velocity': 'no data', 'effort': 'no data',
                 'capacity_effort': 'no data'}]

    rowTab = [
        (
            Paragraph("<para align='center'><b>%s</b></para>" % row['sprint'], styles['Normal']),
            row['velocity'],
            row['effort'],
            row['capacity_effort'],
        ) for row in data
        ]

    table_style = [
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LINEAFTER', (0, 1), (0, -1), 2, colors.lightgrey),
    ]
    oddRowStyle(table_style, rowTab)
    t = Table(headings + rowTab,
              repeatRows=1,
              colWidths=[doc.width / 4, doc.width / 4, doc.width / 4, doc.width / 4])

    t.setStyle(TableStyle(table_style))
    return t


def lastPage():
    # img = Image("TeamBeluga.png", width=doc.width + doc.leftMargin,
    #             height=doc.height + doc.bottomMargin)
    img = Image("TeamBeluga.png", width=doc.width, height=doc.height - styles['TitlePage'].fontSize - 35)
    return img;

def oddRowStyle(table_style, table_rows, color=colors.lightcyan):
    for i, row in enumerate(table_rows):
        if i % 2 == 0:
            table_style.append(('BACKGROUND', (0, i + 1), (-1, i + 1), color))


def foot2(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def title(elements, txt):
    elements.append(Paragraph("<b>%s</b>" % txt, styles['TitlePage']))
    elements.append(Spacer(doc.width, styles['TitlePage'].fontSize + 10))

h1 = ParagraphStyle(
                    name='Heading1',
                    fontSize=14,
                    leading=16
                    )
h2 = ParagraphStyle(
                    name='Heading2',
                    fontSize=12,
                    leading=14,
                    leftIndent=5)


frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width,
               doc.height, id='normal', showBoundary=0)
# First page
Elements.append(Paragraph("", styles['Normal']))
Elements.append(NextPageTemplate('OneCol'))
Elements.append(PageBreak())

title(Elements, "Table of contents")
toc = TableOfContents()
# For conciseness we use the same styles for headings and TOC entries
toc.levelStyles = [h1, h2]
Elements.append(toc)
Elements.append(PageBreak())


# Retrospective ( to keep )
title(Elements, "Retrospective")
Elements.append(retroToKeep(getRetroToKeep()))
Elements.append(PageBreak())

# Retrospective ( to improve and actions )
title(Elements, "Retrospective")
Elements.append(retroToImproveAndActions(getRetroToImproveAndActions()))
Elements.append(PageBreak())

# Review
title(Elements, "Review")
Elements.append(review(getSprint()))
#Elements.append(review([]))
Elements.append(PageBreak())

# Bug fixed
title(Elements, "Bugs fixed")
Elements.append(bug(getFixedBug()))
Elements.append(PageBreak())

# Technical debt open
title(Elements, "Technical debt fixed")
Elements.append(bug(getFixedDebt()))
Elements.append(PageBreak())

# Bug open
title(Elements, "Bugs open")
Elements.append(bug(getOpenBug()))
Elements.append(PageBreak())

# Technical debt open
title(Elements, "Technical debt open")
Elements.append(bug(getOpenDebt()))
Elements.append(PageBreak())

# Velocity
title(Elements, "Velocity")
Elements.append(velocity(getVelocity()))
Elements.append(PageBreak())

title(Elements, "Organisation")
Elements.append(lastPage())
Elements.append(PageBreak())


doc.addPageTemplates([
    PageTemplate(id='First', frames=frameT, onPage=firstPage),
    PageTemplate(id='OneCol', frames=frameT, onPageEnd=foot2),
])
# start the construction of the pdf
#doc.build(Elements)
doc.multiBuild(Elements)
# use external program xpdf to view the generated pdf
os.system("evince basedoc.pdf")
