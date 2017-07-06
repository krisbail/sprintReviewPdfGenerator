# coding: utf8
from ConfigParser import SafeConfigParser

DEFAULT_SECTION = "DEFAULT"
IMAGES_SECTION = "IMAGES"


class Section:
    BUGS_OPEN = "BUGS_OPEN"
    BUGS_CLOSED = "BUGS_CLOSED"
    DEBTS_OPEN = "DEBTS_OPEN"
    DEBTS_CLOSED = "DEBTS_CLOSED"
    REVIEW = "REVIEW"
    REVIEW_NEXT = "REVIEW_NEXT"
    VELOCITY = "VELOCITY"
    RETRO_IMPROVE = "RETRO_IMPROVE"
    RETRO_KEEP = "RETRO_KEEP"
    RETRO_GOOD_TIME = "RETRO_GOOD_TIME"
    ALL = set([BUGS_OPEN, BUGS_CLOSED, DEBTS_OPEN, DEBTS_CLOSED, REVIEW, REVIEW_NEXT, VELOCITY, RETRO_IMPROVE, RETRO_KEEP, RETRO_GOOD_TIME])


class Images:
    LOGO_ORANGE = "logo-orange"
    LOGO_PHOENIX = "logo-phoenix"
    TEAM = "team"


class MainReportConfiguration:

    def __init__(self, project_path='.', candidates=[]):
        self.parser = SafeConfigParser()
        self.name = "%s/main.ini" % project_path
        _candidates = [self.name]
        _candidates.extend(candidates)
        self.config_found = self.parser.read(_candidates)
        self.config_missing = set(candidates) - set(self.config_found)

    def show(self):
        print 'Found config files:', sorted(self.config_found)
        print 'Missing config files:', sorted(self.config_missing)
        for section_name in self.parser.sections():
            print 'Section:', section_name
            print '  Options:', self.parser.options(section_name)
            for name, value in self.parser.items(section_name):
                print '  %s = %s' % (name, value)
            print

    def work_path(self):
        return self.parser.get(DEFAULT_SECTION, "work-path")

    def import_path(self):
        return self.parser.get(DEFAULT_SECTION, "import-path")

    def sprint_path(self):
        return self.parser.get(DEFAULT_SECTION, "sprint-path")

    def update_import_path(self, import_path):
        return self.parser.set(DEFAULT_SECTION, "import-path", import_path)

    def sprint(self):
        return self.parser.get(DEFAULT_SECTION, "sprint")

    def update_sprint(self, sprint):
        return self.parser.set(DEFAULT_SECTION, "sprint", sprint)

    def save(self):
        self.parser.write(file(self.name, mode="w"))


class ReportConfiguration(MainReportConfiguration):

    dirty = False

    def __init__(self, sprint, project_path='.'):
        self.sprint = sprint if sprint is not None else "xxx"
        self.config_spring_file = "%s/sprint/%s/sprint.ini" % (project_path, sprint)
        candidates = ["%s/config.ini" % project_path, self.config_spring_file]
        MainReportConfiguration.__init__(self, project_path=project_path, candidates=candidates)
        if len(self.config_missing) > 0:
            self.parser.set(DEFAULT_SECTION, "sprint", str(sprint))
            self.dirty = True

    def set_file(self, section=None, name_file=""):
        if section not in Section.ALL:
            return
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, "file", name_file)
        self.dirty = True

    def get_file(self, section=None):
        return self.parser.get(section, "file") if self.parser.has_section(section) else ""

    def save(self, version=None):
        if version is not None:
            self.parser.set(DEFAULT_SECTION, "version", version)
        self.parser.write(file(self.config_spring_file, mode="w"))
        self.dirty = False

    def report_name(self):
        return self.parser.get(DEFAULT_SECTION, "report-name")

    def is_dirty(self):
        return self.dirty

    def version(self):
        return self.parser.get(DEFAULT_SECTION, "version")

    def images(self, name):
        return self.parser.get(IMAGES_SECTION, name) if self.parser.has_option(IMAGES_SECTION, name) else ""

    def report_viewer(self):
        return self.parser.get(DEFAULT_SECTION, "report-viewer")

    def url_tracker(self):
        return self.parser.get(DEFAULT_SECTION, "url-tracker")

    def data_path(self):
        return self.parser.get(DEFAULT_SECTION, "data-path")

    def all_files(self):
        files = []
        for section in Section.ALL:
            file_section = self.get_file(section)
            if file_section:
                files.append((section, file_section))
        return files

    def work_files(self):
        path = self.work_path()
        return [(section, file_section) for (section, file_section) in self.all_files() if file_section.count(path) > 0]

    def data_files(self):
        path = self.data_path()
        return [(section, file_section) for (section, file_section) in self.all_files() if file_section.count(path) > 0]


if __name__ == '__main__':
    report = ReportConfiguration(58)
    report.show()
    #report.save()

