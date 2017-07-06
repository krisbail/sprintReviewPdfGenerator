# coding: utf8

import logging
from chardet.universaldetector import UniversalDetector
from cursesmenu import *
from cursesmenu.items import *
from ReportConfigParser import *
from os import walk, system, rename, makedirs
from os.path import join, basename, exists, isdir, splitext
from ReportBuilder import ReportBuilder
from shutil import copy2


class SprintItem(FunctionItem):

    def _change_sprint(self):
        current_sprint = self.config.sprint()
        resp = raw_input("Change current sprint [%s]: " % current_sprint)
        sprint = resp if resp else current_sprint
        if sprint is not None:
            self.config.update_sprint(sprint)
            if not exists(self.config.sprint_path()):
                makedirs(self.config.sprint_path())
            self.config.save()

    def __init__(self, report_config, text):
        self.config = report_config
        super(SprintItem, self).__init__(text, lambda x: self._change_sprint(), [""], should_exit=True)


class ImportFilesItem(FunctionItem):

    @staticmethod
    def _get_encoding(detector, import_file):
        detector.reset()
        for line in file(import_file, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        encoding = detector.result["encoding"]
        return encoding if encoding else "utf-8"

    def _copy_files(self, import_path):
        work_path = self.config.work_path()
        detector = UniversalDetector()
        for (import_path, dirnames, filenames) in walk(import_path):
            for filename in filenames:
                file_name, file_extension = splitext(filename)
                if file_extension == ".csv":
                    import_file = join(import_path, filename)
                    work_file = join(work_path, filename)
                    encoding = self._get_encoding(detector, import_file)
                    if encoding != "utf-8":
                        system("iconv -f %s -t UTF-8 '%s' > '%s'" % (encoding, import_file, work_file))
                    else:
                        copy2(import_file, work_file)

    def _import(self):
        current_path = self.config.import_path()
        resp = raw_input("import files from [%s]: " % current_path)
        import_path = resp if resp else current_path
        if import_path is not None and exists(import_path):
            self._copy_files(import_path)
            if current_path != import_path:
                self.config.update_import_path(import_path)
                self.config.save()

    def __init__(self, report_config, text):
        self.config = report_config
        super(ImportFilesItem, self).__init__(text, lambda x: self._import(), [""], should_exit=True)


class SaveReportItem(FunctionItem):

    def _save(self):
        current_version = self.config.version()
        resp = raw_input("version of file [%s]: " % current_version)
        val = "% 02.2f" % float(resp) if resp else current_version
        if resp is not None:
            self._move_files()
            self.config.save(val)

    def _move_files(self):
        work_files = self.config.work_files()
        data_path = self.config.data_path()
        if not isdir(data_path):
            makedirs(data_path)
        for (section_conf, file_section) in work_files:
            data_file = join(data_path, basename(file_section))

            if exists(file_section):
                rename(file_section, data_file)
            self.config.set_file(section_conf, data_file)

    def __init__(self, report_config, text):
        self.config = report_config
        self.defaultText = text;
        super(SaveReportItem, self).__init__(text, lambda x: self._save(), [""])

    def show(self, index):
        tag = "*" if self.config.is_dirty() else ""
        self.text = "%s %s" % (tag, self.defaultText)
        return super(SaveReportItem, self).show(index)


class ShowReportItem(FunctionItem):

    def _showReport(self):
        try:
            logging.info("Build Report")
            self.report_builder.build()
            if self.report_builder.report_config.report_viewer():
                logging.info("Show Report")
                system("%s %s" % (self.report_builder.report_config.report_viewer(), self.report_builder.report_config.report_name()))
        except Exception as e:
            logging.exception("Error report builder : %s", e)

    def __init__(self, report_config, text):
        self.report_builder = ReportBuilder(report_config=report_config)
        super(ShowReportItem, self).__init__(text, lambda x: self._showReport(), [""])


class SubmenuFileChoice(SubmenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(self, reportConfig, section, text,  menu=None, should_exit=False):
        """
        :ivar CursesMenu self.submenu: The submenu to be opened when this item is selected
        """
        self.defaultText = text
        self.config = reportConfig
        self.section = section

        self.files = []
        for (dirpath, dirnames, filenames) in walk(reportConfig.work_path()):
            self.files = [join(dirpath, filename) for filename in filenames]
            break
        data_files = []
        for (dirpath, dirnames, filenames) in walk(reportConfig.data_path()):
            data_files = [join(dirpath, filename) for filename in filenames]
            break
        self.files.extend(data_files)
        self.files = sorted(self.files)

        super(SubmenuFileChoice, self).__init__(text, SelectionMenu(self.files), menu=menu, should_exit=should_exit)
        self.refreshText()

    def refreshText(self):
        file_section = self.config.get_file(self.section)
        tag = "X" if file_section and exists(file_section) else ""
        self.text = "[%s] %s" % (tag, self.defaultText)

    def set_up(self):
        current_file = self.config.get_file(self.section)
        for i, import_file in enumerate(self.files):
            tag = "X" if current_file == import_file else ""
            self.submenu.items[i].text = "[%s] %s" % (tag, import_file)

        self.refreshText()

        super(SubmenuFileChoice, self).set_up()

    def clean_up(self):
        super(SubmenuFileChoice, self).clean_up()
        index = self.submenu.selected_option
        if index < len(self.files):
            file_choice = self.files[index]
            file_choice = "" if self.config.get_file(self.section) == file_choice else file_choice
            self.config.set_file(self.section, name_file=file_choice)
        self.refreshText()


def update_configuration(main_report):
    sprint = main_report.sprint()
    menu = CursesMenu("Sprint Review report builder", "Sprint %s :" % sprint)
    report_configuration = ReportConfiguration(sprint=sprint)

    menu.append_item(SprintItem(main_report, "Change current Sprint"))
    menu.append_item(ImportFilesItem(report_configuration, "Import files"))
    for section in sorted(Section.ALL):
        item = SubmenuFileChoice(report_configuration, section, section, menu=menu)
        menu.append_item(item)

    show_item = ShowReportItem(report_configuration, "Show report")
    menu.append_item(show_item)
    save_item = SaveReportItem(report_configuration, "Save")
    menu.append_item(save_item)

    menu.show()
    print menu.stdscr.getmaxyx()

    return menu.selected_option == len(menu.items) - 1


logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
user_exit = False

while not user_exit:
    main_report = MainReportConfiguration()
    user_exit = update_configuration(main_report)







