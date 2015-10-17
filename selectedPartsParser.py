__author__ = 'brycecater'

import csv
import re

passed = []
failed = []

passives = []

with open("ROVER_PCB_BOM.csv") as f:
    reader = csv.DictReader(f, ('Description', 'none', 'none2', 'none3', 'link'))
    lineNumber = 1
    for row in reader:

        refdes = None
        digikeyNumber = None
        mfgpartNumber = None
        link = row['link']

        # ========================

        refdesMatch = re.match(r'^([A-Z]{1,6}[0-9]{1,2})', row['Description'])
        try:
            refdes = refdesMatch.groups()[0]
        except AttributeError:
            print row
            failed.append(row)

        # ========================

        partNumberMatch = re.search(r'en/(.*)/(.*)/[0-9]*', row['link'])
        try:
            mfgpartNumber = partNumberMatch.groups()[0]
            digikeyNumber = partNumberMatch.groups()[1]
        except AttributeError:

            failed.append(row)

        passives.append({'refdes':refdes,
                         'link':link,
                         'digikeyPN': digikeyNumber,
                         'mfgPN': mfgpartNumber
                         })

        lineNumber += 1
print lineNumber

goodParts = []

with open("BOM.csv") as f:
    reader = csv.DictReader(f)
    lineNumber = 1
    for row in reader:
        parts = row['Parts'].replace(' ','').split(',')
        digikeyPN = None
        mfgPN = None
        link = None
        state = 'UNMATCHED'

        for passive in passives:
            if passive['refdes'] in parts:
                print passive['refdes'],parts
                if state != 'ERROR':
                    if link is None:
                        link = passive['link']
                        digikeyPN = passive['digikeyPN']
                        mfgPN = passive['mfgPN']
                        state = 'MATCHED'
                    else:
                        if passive['link'] not in link:
                            state = 'ERROR'
                            link = link + ';' + passive['link']

        row['DigikeyPN'] = digikeyPN
        row['MfgPN'] = mfgPN
        row['Link'] = link
        row['State'] = state
        goodParts.append(row)



keys = goodParts[0].keys()
with open('good_bom.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(goodParts)




print len(goodParts)



print len(failed)
# print failed
