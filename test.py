from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm



def hello(c):
    c.drawString(0, 0, "Hello World")

def fonts(canvas):
    from reportlab.lib.units import inch
    text = "Now is the time for all good men to..."
    x = 1.8*inch
    y = 2.7*inch
    for font in canvas.getAvailableFonts():
        canvas.setFont(font, 10)
        canvas.drawString(x,y,text)
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(x-10,y, font+":")
        y = y-13

def horizontalscale(canvas):
    from reportlab.lib.units import inch
    textobject = canvas.beginText()
    textobject.setTextOrigin(3, 2.5*inch)
    textobject.setFont("Helvetica-Oblique", 12)
    horizontalscale = 80 # 100 is default
    lyrics = ["azzeertytui", "jkjlkjlkjlllllllllll", "abbbbbbddddkkffffffffffffffffflllllllllllgggggggggggggggggggllll"]
    for line in lyrics:
        textobject.setHorizScale(horizontalscale)
        textobject.textLine("%s: %s" %(horizontalscale,line))
        horizontalscale += 10
        textobject.setFillColorCMYK(0.0,0.4,0.4,0.2)
        textobject.textLines('''
        With many apologies to the Beach Boys
        and anyone else who finds this objectionable
        ''')
    canvas.drawText(textobject)


c = canvas.Canvas("hello.pdf", landscape(A4))
# move the origin up and to the left
c.translate(cm, cm)
# define a large font
size = 14
c.setFont("Helvetica", size)
hello(c)
c.showPage()

c.setFillColorRGB(0, 0, 0.77)
tw = c.stringWidth("COUCOU", "Helvetica", size)
c.rect(9.8 * cm, 9.8 * cm, tw, size + 0.2*cm, fill=1)
c.setFillColorRGB(1, 0, 1)
c.drawString(10 * cm, 10 * cm, "COUCOU")
c.showPage()

fonts(c)
c.showPage()

horizontalscale(c)
c.showPage()

c.save()
