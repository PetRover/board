__author__ = 'brycecater'

import csv
import re

failed = []
rows = []
with open('FINAL_BOM.csv', 'rb') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # print row
        partNumberMatch = re.search(r'en/(.*)/(.*)/[0-9]*', row['Link'])
        try:
            row['MfgPN'] = partNumberMatch.groups()[0]
            row['DigikeyPN'] = partNumberMatch.groups()[1]
        except AttributeError:
            failed.append(row)

        rows.append(row)


print len(failed)

with open('FINAL_BOM(AUTO).csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, ('RPN', 'Description','Package','Value','Qty','State','Parts','Link','Device','DigikeyPN','MfgPN','Order Quant.'))
    dict_writer.writeheader()
    dict_writer.writerows(rows)

