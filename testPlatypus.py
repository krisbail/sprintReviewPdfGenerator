# coding: utf8

from docutils.nodes import organization
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

Title = "Hello world"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "First Page youyou/ %s" % pageinfo)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()


def go():
    doc = SimpleDocTemplate("out/phello.pdf", pagesize=landscape(A4), showBoundary=1, leftMargin=0)

    Story = [Spacer(1, 1*inch)]
    style = styles["Normal"]
    for i in range(12):
        bogustext = ("<b>This</b> is Paragraph number %s. " % i) *20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1, 0.2*inch))

    img = Image("TeamBeluga.png", width=700, height=439)

    Story.append(img)
    doc.onFirstPage=myFirstPage
    doc.onLaterPages=myLaterPages
    #doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    doc.build(Story)

def firstPageSR():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import Paragraph, Frame
    from reportlab.lib.colors import orange

    c = Canvas("out/firstPageSR.pdf", landscape(A4))
    body = Frame(cm, cm, 19 * cm, 20 * cm, showBoundary=1)
    right = Frame(20 * cm, cm, 6 * cm, 20 * cm, showBoundary=1)
    style = ParagraphStyle(styles["Normal"])
    style2 = styles["BodyText"]
    style.textColor = orange
    style.fontSize = 60

    imgPhoenix = Image("phoenix.jpg", 5 * cm, 5 * cm)
    imgPhoenix.hAlign = 'RIGHT'
    imgPhoenix.vAlign = 'TOP'
    imgOrange = Image("orange.jpg", 2 * cm, 2 * cm)
    imgOrange.hAlign = 'RIGHT'
    imgOrange.vAlign = 'BOTTOM'
    StoryRight = [imgPhoenix]
    p = Paragraph("Team Beluga", style2)
    StoryRight.append(p)
    StoryRight.append(imgOrange)

    StoryBody = [Paragraph("<b>Sprint Review</b>", style)]
    p = Paragraph("Sprint N 13", style2)
    StoryBody.append(p)

    body.addFromList(StoryBody, c)
    right.addFromList(StoryRight, c)
    c.save()

def firstPage():
    from reportlab.pdfgen.canvas import Canvas
    c = Canvas("out/firstPage.pdf", landscape(A4))
    c.drawImage('orange.jpg', 26.7 * cm, 1 * cm, width=2 * cm, height=2 * cm)
    c.drawImage('phoenix.jpg', 22.7 * cm, 14 * cm, width=6 * cm, height=6 * cm)
    c.setFont("Helvetica-Bold", 62)
    c.setFillColorRGB(1, 0.47, 0)
    c.drawString(2 * cm, 16 * cm, "Sprint Review")
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(9 * cm, 14 * cm, "sprint N° 26")
    c.save()

def review():
    from reportlab.platypus import Paragraph
    from reportlab.lib import colors
    from reportlab.pdfgen.canvas import Canvas
    c = Canvas("out/review.pdf", landscape(A4))
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(1, 0.47, 0)
    c.drawString(1 * cm, 19 * cm, "Review")
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawString(1 * cm, 17 * cm, "Story")
    p = Paragraph("<para bulletanchor=start>qsdqsdqsdqdqdqddq<br/>kljkjlkjkj</para>", styles["Normal"], bulletText='\xe2\x80\xa2')
    p.wrap(10 *cm, 4 * cm)
    p.drawOn(c, 1 * cm, 15 * cm)
    c.save()

def getTable():
    data = [['Top\nLeft', '', '02', '03', '04'],
     ['', '', '12', '13', '14'],
     ['20', '21', '22', 'Bottom\nRight', ''],
     ['30', '31', '32', '', '']]
    t = Table(data, style=[
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (1, 1), colors.palegreen),
        ('SPAN', (0, 0), (1, 1)),
        ('BACKGROUND', (-2, -2), (-1, -1), colors.pink),
        ('SPAN', (-2, -2), (-1, -1)),
    ])
    return t


def testFrame():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, Frame
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    story = []
    # add some flowables
    story.append(Paragraph('''This is a Heading''', styleH))
    story.append(getTable())
    story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
                           styleN))

    c = Canvas('out/mydoc.pdf')
    f = Frame(inch, inch, 6 * inch, 9 * inch, showBoundary=1)
    f.addFromList(story, c)
    c.save()

#testFrame()
#go()
#firstPage()
review()
