# coding: utf8

import os
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from belugaReportTemplate import ReportPhoenixTemplate
from ReportConfigParser import ReportConfiguration, Section, Images
from reportlab.lib.pagesizes import A4, landscape

from testCsv import getSprint, getFixedBug, getFixedDebt, \
    getRetroToKeep, getRetroToImproveAndActions, \
    getOpenBug, getOpenDebt, getVelocity, getRetroGoodTime, getRowDataFromCsv


class ReportBuilder:

    def __init__(self, report_config=ReportConfiguration("xx")):
        self.report_config = report_config
        self.doc = ReportPhoenixTemplate(
            report_config.report_name(),
            sprint=report_config.sprint,
            logo_orange=report_config.images(Images.LOGO_ORANGE),
            logo_phoenix=report_config.images(Images.LOGO_PHOENIX),
            team_img=report_config.images(Images.TEAM),
            pagesize=landscape(A4)
        )

    def getLink(self, url, aid):
        if url is not None:
            url = url % aid
            linkurl = "<a href='%s'><u>%s</u></a>" % (url, aid)
            return Paragraph(linkurl, self.doc.styles['Link'])
        else:
            return Paragraph(aid, self.doc.styles['Link'])

    def review_old(self, sprint, data, next_stories_list = None):
        if data is None or len(data) == 0:
            data = [{'sprint': 'current', 'aid': 'no data', 'point': 'no data', 'component': 'no data', 'title': 'no data'},
                    {'sprint': 'next', 'aid': 'no data', 'point': 'no data', 'component': 'no data', 'title': 'no data'}
                    ]
        headings = ('sprint', 'Aid', 'Complexity', 'Component', 'Title')
        row_index_last_cell_current_sprint = len(data)
        stories = []
        current_label_sprint = "sprint %d" % int(sprint)
        if next_stories_list is not None and len(next_stories_list) > 0:
            data.extend(next_stories_list)
        for index, p in enumerate(data):
            label_sprint = current_label_sprint if index < row_index_last_cell_current_sprint else "sprint %d" %( int(sprint) + 1)
            stories.append((label_sprint,
                            self.getLink(self.report_config.url_tracker(), p['aid']),
                            p['point'],
                            Paragraph(p['component'], self.doc.styles['Normal']),
                            Paragraph(p['title'], self.doc.styles['Normal'])
                            ))

        t = Table([headings] + stories, colWidths=[2 * cm, 2 * cm, 2 * cm, 3 * cm, 16 * cm], repeatRows=1)
        tab_style = TableStyle(
            [
                ('LINEBELOW', (0, 1), (-1, -1), 1, colors.lightgrey),
                ('BOX', (0, 1), (0, -1), 1, colors.black),
                ('BOX', (1, 1), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('SPAN', (0, 1), (0, row_index_last_cell_current_sprint)),
                ('VALIGN', (0, 1), (0, row_index_last_cell_current_sprint), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (-1, row_index_last_cell_current_sprint), colors.lightcyan)
            ])

        if next_stories_list is not None and len(next_stories_list) > 0:
            tab_style.add('LINEBELOW', (0, row_index_last_cell_current_sprint), (-1, row_index_last_cell_current_sprint), 2, colors.grey)
            tab_style.add('SPAN', (0, row_index_last_cell_current_sprint + 1), (0, -1))
            tab_style.add('VALIGN', (0, row_index_last_cell_current_sprint), (0, -1), 'MIDDLE')

        t.setStyle(tab_style)
        return t

    def review(self, data):
        if data is None or len(data) == 0:
            data = [
                {'aid': 'no data', 'sprint_mib4': 'no data', 'sprint_newbox': 'no data', 'point': 'no data',
                 'component': 'no data', 'title': 'no data'}
            ]
        headings = ('Aid', 'Mib4', 'Newbox', 'Complexity', 'Component', 'Title')
        stories = []

        for index, p in enumerate(data):
            status_mib4 = "<font color=red>{0}</font>".format(p['status_mib4']) if p['status_mib4'] == "Dev en cours" else p['status_mib4']
            status_newbox = "<font color=red>{0}</font>".format(p['status_newbox']) if p['status_newbox'] == "Dev en cours" else p['status_newbox']

            stories.append((self.getLink(self.report_config.url_tracker(), p['aid']),
                            Paragraph(p['sprint_mib4'] + "<br/>" + status_mib4, self.doc.styles['Normal']),
                            Paragraph(p['sprint_newbox'] + '<br/>' + status_newbox, self.doc.styles['Normal']),
                            p['point'],
                            Paragraph(p['component'], self.doc.styles['Normal']),
                            Paragraph(p['title'], self.doc.styles['Normal'])
                            ))

        t = Table([headings] + stories, colWidths=[2 * cm, 3 * cm, 3 * cm, 2 * cm, 3 * cm, 12 * cm], repeatRows=1)
        tab_style = [

            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('ALIGN', (1, 1), (3, -1), 'CENTER'),
            ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),
        ]
        self.oddRowStyle(tab_style, stories, colors.lightcyan)
        t.setStyle(TableStyle(tab_style))
        return t

    def review_next(self, data):
        if data is None or len(data) == 0:
            data = [
                {'aid': 'no data', 'sprint_mib4': 'no data', 'sprint_newbox': 'no data', 'point': 'no data', 'component': 'no data', 'title': 'no data'}
                ]
        headings = ('Aid', 'Sprint Mib4', 'Sprint Newbox', 'Complexity', 'Component', 'Title')
        stories = []
        for index, p in enumerate(data):
            stories.append((self.getLink(self.report_config.url_tracker(), p['aid']),
                            Paragraph(p['sprint_mib4'], self.doc.styles['Normal']),
                            Paragraph(p['sprint_newbox'], self.doc.styles['Normal']),
                           p['point'],
                           Paragraph(p['component'], self.doc.styles['Normal']),
                           Paragraph(p['title'], self.doc.styles['Normal'])
                            ))

        t = Table([headings] + stories, colWidths=[2 * cm, 3 * cm, 3 * cm, 2 * cm, 3 * cm, 12 * cm], repeatRows=1)
        tab_style = [

                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('ALIGN', (1, 1), (3, -1), 'CENTER'),
                ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),
            ]
        self.oddRowStyle(tab_style, stories, colors.lightcyan)
        t.setStyle(TableStyle(tab_style))
        return t

    def bug(self, data, color=colors.lightcyan, addAidlink=True):
        urlTracker = self.report_config.url_tracker() if addAidlink else None
        headings = [('Aid', 'Urgency', 'Component', 'Title', 'Status')]
        bugs = [(
                    self.getLink(urlTracker, bug['aid']), bug['urgency'], bug['component'],
                    Paragraph(bug['title'], self.doc.styles['Normal']), bug['status']
                )
                for bug in data]
        t = Table(headings + bugs, colWidths=[2 * cm, 3 * cm, 3 * cm, 15 * cm, 2 * cm], repeatRows=1)
        table_style = [
                        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                      ]
        self.oddRowStyle(table_style, bugs, color)
        t.setStyle(TableStyle(table_style))
        return t

    def retroToKeep(self, data=None):
        rowTab = []
        rowTab.append(['To keep'])

        if data is None or len(data) == 0:
            data = [{'to_keep': 'no data'}]
        for row in data:
            rowTab.append([Paragraph(row['to_keep'], self.doc.styles['Normal'])])
        table_style = [
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]
        self.oddRowStyle(table_style, rowTab[1:])
        t = Table(rowTab, repeatRows=1, colWidths=[self.doc.width])
        t.setStyle(TableStyle(table_style))
        return t

    def retroToImproveAndActions_old(self, data=None):
        headings = [('To improve', 'Actions')]

        if data is None or len(data) == 0:
            data = [{'to_improve': 'no data', 'actions': 'no data'}]

        rowTab = [
                    (
                        Paragraph(row['to_improve'], self.doc.styles['Normal']),
                        Paragraph(row['actions'], self.doc.styles['Normal'])
                    ) for row in data
                 ]

        table_style = [
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('LINEAFTER', (0, 1), (0, -1), 2, colors.lightgrey),
        ]
        self.oddRowStyle(table_style, rowTab)
        t = Table(headings + rowTab, repeatRows=1, colWidths=[self.doc.width / 2, self.doc.width / 2])
        t.setStyle(TableStyle(table_style))
        return t

    def retroToImproveAndActions(self, data=None):
        headings = [('To keep', 'To improve', 'To resolve')]

        if data is None or len(data) == 0:
            data = [('no data', 'no data', 'no_data')]

        rowTab = [
            (
                Paragraph(row[0], self.doc.styles['Normal']),
                Paragraph(row[1], self.doc.styles['Normal']),
                Paragraph(row[2], self.doc.styles['Normal'])
            ) for row in data[1:]
            ]

        table_style = [
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('LINEAFTER', (0, 1), (0, -1), 1, colors.lightgrey),
            ('LINEAFTER', (1, 1), (1, -1), 1, colors.lightgrey)
        ]
        self.oddRowStyle(table_style, rowTab)
        t = Table(headings + rowTab, repeatRows=1, colWidths=[self.doc.width / 3, self.doc.width / 3, self.doc.width / 3])
        t.setStyle(TableStyle(table_style))
        return t

    def retroGoodTime(self, data=None):
        if data is None or len(data) == 0:
            data = [['no data', 'no data']]
        rowTab = []
        headings = ['To keep', 'To improve', 'To resolve']
        table_style = []
        index_color = 0
        for (index, row) in enumerate(data):
            if row[0] in headings:
                rowTab.append([Paragraph(row[0], self.doc.styles['Normal']), Paragraph("Vote", self.doc.styles['Normal'])])
                index_color = 1
                table_style.append(('LINEBELOW', (0, index), (-1, index), 2, colors.black))
                table_style.append(('ALIGN', (0, index), (-1, index), 'CENTER'))
                table_style.append(('FONTSIZE', (0, index), (-1, index), 14))
                table_style.append(('BOTTOMPADDING', (0, index), (-1, index), 8))
            else:
                rowTab.append([Paragraph(row[0], self.doc.styles['Normal']), Paragraph(row[1], self.doc.styles['Normal'])])
            if index_color % 2 == 0:
                table_style.append(('BACKGROUND', (0, index), (-1, index), colors.lightcyan))
            index_color += 1

        t = Table(rowTab, colWidths=[self.doc.width / 2, self.doc.width / 2])
        t.setStyle(TableStyle(table_style))
        return t

    def velocity(self, data=None):
        headings = [('Sprint', 'Velocity', 'Effort', 'Capacity per effort')]

        if data is None or len(data) == 0:
            data = [{'sprint': 'no data', 'velocity': 'no data', 'effort': 'no data',
                     'capacity_effort': 'no data'}]

        rowTab = [
            (
                Paragraph("<para align='center'><b>%s</b></para>" % row['sprint'], self.doc.styles['Normal']),
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
        self.oddRowStyle(table_style, rowTab)
        t = Table(headings + rowTab,
                  repeatRows=1,
                  colWidths=[self.doc.width / 4, self.doc.width / 4, self.doc.width / 4, self.doc.width / 4])

        t.setStyle(TableStyle(table_style))
        return t

    def oddRowStyle(self, table_style, table_rows, color=colors.lightcyan, offset=0):
        for i, row in enumerate(table_rows):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i + 1 + offset), (-1, i + 1 + offset), color))

    def build(self):
        elements = []

        # Retrospective ( good Time )
        file_name = self.report_config.get_file(Section.RETRO_GOOD_TIME)
        if file_name:
            self.doc.add_title(elements, "Retrospective")
            elements.append(self.retroGoodTime(getRetroGoodTime(file_name)))
            elements.append(PageBreak())

        # Retrospective ( to keep )
        file_name = self.report_config.get_file(Section.RETRO_KEEP)
        if file_name:
            self.doc.add_title(elements, "Retrospective")
            elements.append(self.retroToKeep(getRetroToKeep(file_name)))
            elements.append(PageBreak())

        # Retrospective ( to improve and actions )
        file_name = self.report_config.get_file(Section.RETRO_IMPROVE)
        if file_name:
            self.doc.add_title(elements, "Retrospective")
            elements.append(self.retroToImproveAndActions(getRowDataFromCsv(file_name, delimiter=',')))
            #elements.append(self.retroToImproveAndActions(getRetroToImproveAndActions(file_name)))
            elements.append(PageBreak())

        # Review
        file_name = self.report_config.get_file(Section.REVIEW)
        if file_name:
            self.doc.add_title(elements, "Review")
            elements.append(self.review(getSprint(self.report_config.get_file(Section.REVIEW))))
            elements.append(PageBreak())

        # Review Next
        file_name = self.report_config.get_file(Section.REVIEW_NEXT)
        if file_name:
            self.doc.add_title(elements, "Proposal")
            elements.append(self.review_next(getSprint(self.report_config.get_file(Section.REVIEW_NEXT))))
            elements.append(PageBreak())

        # Bug fixed
        file_name = self.report_config.get_file(Section.BUGS_CLOSED)
        if file_name:
            self.doc.add_title(elements, "Bugs fixed")
            elements.append(self.bug(getFixedBug(file_name), addAidlink=False))
            elements.append(PageBreak())

        # Technical debt closed
        file_name = self.report_config.get_file(Section.DEBTS_CLOSED)
        if file_name:
            self.doc.add_title(elements, "Technical debt fixed")
            elements.append(self.bug(getFixedDebt(file_name)))
            elements.append(PageBreak())

        # Bug open
        file_name = self.report_config.get_file(Section.BUGS_OPEN)
        if file_name:
            self.doc.add_title(elements, "Bugs open")
            elements.append(self.bug(getOpenBug(file_name), addAidlink=False))
            elements.append(PageBreak())

        # Technical debt open
        file_name = self.report_config.get_file(Section.DEBTS_OPEN)
        if file_name:
            self.doc.add_title(elements, "Technical debt open")
            elements.append(self.bug(getOpenDebt(file_name)))
            elements.append(PageBreak())

        # Velocity
        file_name = self.report_config.get_file(Section.VELOCITY)
        if file_name:
            self.doc.add_title(elements, "Velocity")
            elements.append(self.velocity(getVelocity(file_name)))
            elements.append(PageBreak())

        self.doc.generate(elements)


if __name__ == '__main__':
    reportBuilder = ReportBuilder(ReportConfiguration(26))
    reportBuilder.build()
    if reportBuilder.report_config.report_viewer():
        os.system("%s %s" % (reportBuilder.report_config.report_viewer(), reportBuilder.report_config.report_name()))

