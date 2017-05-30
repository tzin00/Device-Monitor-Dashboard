"""
Utilities used by the webapp.
"""
import csv


def parse_csv(csvfile):
    return_data = []
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if 'fqdn' in row[0].lower():
                continue
            fqdn = row[0]
            port = row[1]
            name = row[2]
            return_data.append(dict(
                    fqdn=fqdn,
                    port=port,
                    name=name
                    ))
    return return_data
