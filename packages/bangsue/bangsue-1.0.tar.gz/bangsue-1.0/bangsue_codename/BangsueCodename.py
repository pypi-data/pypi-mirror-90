import csv
import os
from numpy import random


class Bangsue:

    def __init__(self):
        self.file_loc = os.path.join(os.path.dirname(__file__), 'file', 'tambon_bse.csv')

    def codename_csv_get(self):
        bangsue = []
        reader = csv.DictReader(open(file=self.file_loc, newline='', encoding='utf-8-sig'))
        for row in reader:
            if row['sub_district'] == '' or row['district'] == '' or row['province'] == '':
                pass
            elif row['sub_district'] == row['district'] or row['district'] == row['province']:
                pass
            else:
                if row['sub_district'] == "district":
                    bangsue.append({
                        "district": (row['district']).replace(' ', '').lower(),
                        "province": (row['province']).replace(' ', '_').lower()
                    })
                else:
                    bangsue.append({
                        "sub_district": (row['sub_district']).replace(' ', '').lower(),
                        "district": (row['district']).replace(' ', '').lower(),
                        "province": (row['province']).replace(' ', '_').lower()
                    })

        return bangsue

    def get_code_name(self):
        bangsue = self.codename_csv_get()
        number = random.randint(0, len(bangsue))
        return bangsue[number]

    def convert_codename_to_string(self, bangsue, selection=None):
        if bangsue['sub_district'] == '':
            if selection == "province_with_district":
                return '_'.join([bangsue['province'], bangsue['district']])
            elif selection == "district":
                return '_'.join([bangsue['district']])
            elif selection == "province":
                return '_'.join([bangsue['province']])
            elif selection == "all":
                return '_'.join([bangsue['district'], bangsue['province']])
        else:
            if selection == "province_with_district":
                return '_'.join([bangsue['province'], bangsue['district']])
            elif selection == "province_with_subdistrict":
                return '_'.join([bangsue['sub_district'], bangsue['province']])
            elif selection == "subdistrict_with_district":
                return '_'.join([bangsue['sub_district'], bangsue['district']])
            elif selection == "subdistrict":
                return '_'.join([bangsue['subdistrict']])
            elif selection == "district":
                return '_'.join([bangsue['district']])
            elif selection == "province":
                return '_'.join([bangsue['province']])
            elif selection == "all":
                return '_'.join([bangsue['sub_district'], bangsue['district'], bangsue['province']])
