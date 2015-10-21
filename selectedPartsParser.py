__author__ = 'brycecarter'

import csv
import re

passed = []
failed = []

refdesLinkMapping = []

with open("REFDES_LINK_MAPPING.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:

        refdes = row['Refdes']
        digikeyNumber = None
        mfgpartNumber = None
        link = row['Link']
        # ========================

        partNumberMatch = re.search(r'en/(.*)/(.*)/[0-9]*', link)
        try:
            mfgpartNumber = partNumberMatch.groups()[0]
            digikeyNumber = partNumberMatch.groups()[1]
        except AttributeError:
            failed.append(row)

        refdesLinkMapping.append({'refdes':refdes,
                         'link':link,
                         'digikeyPN': digikeyNumber,
                         'mfgPN': mfgpartNumber
                         })

print '{0} FAILED TO FIND PART NUMBERS'.format(len(failed))

partsList = []

with open("PART_BOM_FROM_EAGLE.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        refdesList = row['Parts'].replace(' ','').split(',')
        digikeyPN = None
        mfgPN = None
        link = None
        state = 'UNMATCHED'

        # Remove annoying "{Region} Symbol" part from descriptions
        match = re.search(r',.*\ssymbol', row['Description'])
        if match is not None:
            row['Description'] = row['Description'].replace(match.group(), '')
        # =================================

        for refdesDict in refdesLinkMapping:
            if refdesDict['refdes'] in refdesList:
                if state != 'ERROR':
                    if link is None:
                        link = refdesDict['link']
                        digikeyPN = refdesDict['digikeyPN']
                        mfgPN = refdesDict['mfgPN']
                        state = 'MATCHED'
                    else:
                        if refdesDict['link'] not in link:
                            state = 'ERROR'
                            link = link + '; ' + refdesDict['link']
                else:
                    link = link + '; ' + refdesDict['link']

        row['DigikeyPN'] = digikeyPN
        row['MfgPN'] = mfgPN
        row['Link'] = link
        row['State'] = state
        row.pop('')
        partsList.append(row)

manualPartsList = []
failed = []

with open('MANUAL_PARTS_BOM.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        row['State'] = 'MANUAL'
        row['Parts'] = 'EXTERNAL'
        row['Device'] = 'NONE'

        partNumberMatch = re.search(r'en/(.*)/(.*)/[0-9]*', row['Link'])
        try:
            row['MfgPN'] = partNumberMatch.groups()[0]
            row['DigikeyPN'] = partNumberMatch.groups()[1]
        except AttributeError:
            failed.append(row)
        manualPartsList.append(row)

print '{0} FAILED TO FIND PART NUMBERS'.format(len(failed))

partsList += manualPartsList

outRows = []
prefix = '200-'
pn = 1
for r in sorted(partsList, key=lambda x: (x['Parts'][0],x['Value'],x['Package'])):
    r['RPN'] = prefix+str(pn).zfill(3)
    outRows.append(r)
    pn += 1

usedLinks = []
for row in outRows:
    if row['Link'] != 'NONE':
        if row['Link'] in usedLinks:
            for row in [r for r in outRows if r['Link'] == row['Link']]:
                row['State'] = 'REUSE ERROR'

        usedLinks.append(row['Link'])

with open('FINAL_BOM(AUTO).csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, ('RPN', 'Description','Package','Value','Qty','State','Parts','Link','Device','DigikeyPN','MfgPN'))
    dict_writer.writeheader()
    dict_writer.writerows(outRows)

