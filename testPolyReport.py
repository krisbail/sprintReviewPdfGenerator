from PollyReports import *
from reportlab.pdfgen.canvas import Canvas
#from reportlab.lib.units import cm
#from testdata import data
from testCsv import getBug, getSprint


#data = [("Hello", "World")]
rpt = Report(datasource=getBug(),
             detailband=Band([
                 Element((36, 0), ("Helvetica", 12),
                         key="aid"),
                 Element((100, 0), ("Helvetica", 12),
                         key="summary", align="left")]))

rpt.pageheader = Band([
    Element((36, 0),
            ("Times-Bold", 20),
            text = "Page Header"),
    Element((36, 24),
            ("Helvetica", 12),
            text = "aid"),
    Element((100, 24),
            ("Helvetica", 12),
            text = "Summary", align = "right"),
    Rule((36, 42), 7.5*72, thickness=4), ])

rpt.pagefooter = Band([
    Element((72*8, 0),
            ("Times-Bold", 20),
            text = "Page Footer", align = "right"),
    Element((36, 16), ("Helvetica-Bold", 12),
            sysvar = "pagenumber",
            format = lambda x: "Page %d" % x),
])

rpt.groupheaders2=\
    [
        Band(
            [
            Rule((36, 20), 7.5*72),
            Element((36, 4),
                    ("Helvetica-Bold", 12),
                    getvalue=lambda x: x["name"][0].upper(),
                    format=lambda x: "Names beginning with %s" % x)
            ],
            getvalue=lambda x: x["name"][0].upper()
        )
    ]

canvas = Canvas("out/reportStory.pdf", (72*11, 72*8.5))
rpt2 = Report(datasource=getSprint(),
             detailband=Band(
                 [
                     Element((36, 0), ("Helvetica", 12),
                             key="aid"),
                     Element((100, 0), ("Helvetica", 12),
                             key="point"),
                     Element((140, 0), ("Helvetica", 12),
                            key="title", align="left")
                 ]))
rpt2.groupheaders=\
    [
        Band(
            [
            Rule((20, 20), 60),
            Element((20, 4),
                    ("Helvetica-Bold", 12),
                    getvalue=lambda x: x["sprint"].upper(),
                    format=lambda x: "%s" % x)
            ],
            getvalue=lambda x: x["sprint"].upper()
        )
    ]

rpt2.pageheader = Band([
    Element((20, 0),
            ("Times-Bold", 20),
            text = "Review"),
    Element((36, 24),
            ("Helvetica", 12),
            text = "Aid"),
    Element((100, 24),
            ("Helvetica", 12),
            text="Point"),
    Element((140, 24),
            ("Helvetica", 12),
            text = "Title", align="left"),
    Rule((36, 42), 7.5*72, thickness=1), ])

rpt2.generate(canvas)
canvas.save()