# coding: utf8

from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Frame, Paragraph, NextPageTemplate, PageBreak,\
    PageTemplate, Spacer, Image
from reportlab.lib.units import inch, cm
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from os.path import split


class ReportPhoenixTemplate(BaseDocTemplate):
    def __init__(self, filename, sprint=None, logo_orange=None, logo_phoenix=None, team_img=None, **kw):
        self.allowSplitting = 0
        self.sprint = sprint
        self.name_report = split(filename)[1]
        self.logo_orange = logo_orange
        self.logo_phoenix = logo_phoenix
        self.team_img = team_img
        self.orangeColor = colors.Color(1, 0.47, 0)
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='TitlePage', parent=self.styles['Normal'], fontSize=32, textColor=self.orangeColor))
        self.styles.add(ParagraphStyle(name='Link', parent=self.styles['Normal'], textColor=self.orangeColor))
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width,
                      self.height, id='normal')
        self.addPageTemplates([
            PageTemplate(id='First', frames=frame, onPage=lambda c, d: self.first_page(c)),
            PageTemplate(id='OneCol', frames=frame, onPageEnd=lambda c, d: self.foot_page(c)),
        ])

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            if text == "Table of contents":
                return
            style = flowable.style.name
            if style == 'TitlePage':
                key = 'h2-%s' % self.seq.nextf('TitlePage')
                self.canv.bookmarkPage(key)
                self.notify('TOCEntry', (0, text, self.page, key))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

    def first_page(self, c):
        c.saveState()
        c.drawImage(self.logo_orange, 26.7 * cm, 1 * cm, width=2 * cm,
                    height=2 * cm)
        c.drawImage(self.logo_phoenix, 22.7 * cm, 14 * cm, width=6 * cm,
                    height=6 * cm)
        c.setFont("Helvetica-Bold", 62)
        c.setFillColorRGB(1, 0.47, 0)
        c.drawString(2 * cm, 16 * cm, "Sprint Review")
        c.setFont("Helvetica-Bold", 38)
        c.drawCentredString(9 * cm, 14 * cm, "sprint N° %s" % self.sprint)
        c.restoreState()

    def foot_page(self, canvas):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(inch, 0.75 * inch, "Page %d" % self.page)
        canvas.drawRightString(10.75 * inch, 0.75 * inch, "%s" % self.name_report)

        canvas.restoreState()

    def last_page(self):
        img = Image(self.team_img, width=self.width, height=self.height - self.styles['TitlePage'].fontSize - 35)
        return img

    def add_title(self, elements, txt):
        elements.append(Paragraph("<b>%s</b>" % txt, self.styles['TitlePage']))
        elements.append(Spacer(self.width, self.styles['TitlePage'].fontSize + 10))

    def generate(self, report_elements=[]):
        elements = []
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

        # First page
        elements.append(Paragraph("", self.styles['Normal']))
        elements.append(NextPageTemplate('OneCol'))
        elements.append(PageBreak())

        self.add_title(elements, "Table of contents")
        toc = TableOfContents()
        # For conciseness we use the same styles for headings and TOC entries
        toc.levelStyles = [h1, h2]
        elements.append(toc)
        elements.append(PageBreak())

        if len(report_elements) > 0:
            elements.extend(report_elements)

        self.add_title(elements, "Organisation")
        elements.append(self.last_page())
        elements.append(PageBreak())

        self.multiBuild(elements)
