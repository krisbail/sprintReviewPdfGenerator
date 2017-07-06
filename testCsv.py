import csv
import os.path

# coding: utf8

# iconv -f ISO-8859-1 -t UTF-8 test.csv > testUtf8.csv OU decode('latin-1)

#urgency;FORGE id;QC id;component;summary;last_update_date;status_id;resolution;target_sprint_1
map_key_bug_debt2 = {
    'aid': 'FORGE id',
    'title': 'summary',
    'component': 'component',
    'status': 'status_id',
    'urgency': 'urgency'
}
map_key_bug_debt = {
    'aid': 'id',
    'title': 'title',
    'component': 'component',
    'status': 'status',
    'urgency': 'urgency'
}

map_key_bug = {
    'aid': 'Defect ID',
    'title': 'Summary',
    'component': 'component',
    'status': 'Status',
    'urgency': 'Urgency'
}

map_key_story = {
    'aid': 'id',
    'component': 'component',
    'sprint_mib4': 'target_sprint_mib4',
    'sprint_newbox': 'target_sprint_newbox',
    'point': 'point',
    'rang': 'rang_1',
    'title': 'title',
    'status_mib4': 'status_mib4',
    'status_newbox': 'status_newbox'
}


def getSprint(name_file='artifact_UserStory_phoenixbacklog.csv', delimiter=';'):
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key_story, delimiter=delimiter)


def getOpenBug(name_file='artifact_BugTracker_obox.csv', delimiter=';'):
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key_bug, delimiter=delimiter)


def getFixedBug(name_file='artifact_BugTracker_obox.csv', delimiter=';'):
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key_bug, delimiter=delimiter)


def getOpenDebt(name_file='artifact_BugTracker_obox.csv', delimiter=';'):
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key_bug_debt, delimiter=delimiter)


def getFixedDebt(name_file='artifact_BugTracker_obox.csv', delimiter=';'):
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key_bug_debt, delimiter=delimiter)


def getRetroToKeep(name_file='testUtf8.csv', delimiter=';'):
    map_key={'to_keep': 'to_keep'}
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key, delimiter=delimiter)


def getRetroToImproveAndActions(name_file='testUtf8.csv', delimiter=';'):
    map_key = {'to_improve': 'to_improve', 'actions': 'actions'}
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key, delimiter=delimiter)


def getVelocity(name_file='velocity.csv', delimiter=','):
    map_key = {'sprint': 'Sprint', 'velocity': 'Velocity', 'effort': 'Effort', 'capacity_effort': 'Capacity/Effort'}
    return extractDataFromCsv(nameFile=name_file, mapKey=map_key, delimiter=delimiter)

def getRetroGoodTime(name_file='retro.csv', delimiter=';'):
    return getRowDataFromCsv(name_file, delimiter=delimiter)


def extractDataFromCsv(nameFile, mapKey={}, delimiter=';'):
    data = []
    if not os.path.exists(nameFile):
        return data
    with open(nameFile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for rowCsv in reader:
            mapRow={}
            for (key, val) in mapKey.items():
                mapRow[key] = rowCsv[val] if val in rowCsv else "-"
            data.append(mapRow)
    return data


def getRowDataFromCsv(nameFile, delimiter=';'):
    data = []
    if not os.path.exists(nameFile):
        return data
    with open(nameFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for rowCsv in reader:
            data.append(rowCsv)
    return data
