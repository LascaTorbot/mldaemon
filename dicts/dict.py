from mldaemon.utils.output import *
from mldaemon.utils.pkldata import *
from pymongo import MongoClient
import os

class Dictionary:
    def __init__(self, mongo_host, mongo_port):
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client.cuckoo

    def gen_dict(self, output_path):
        # loading data from mongodb
        limit_data = self.db.analysis.count()
        db_data = self.db.analysis.find()

        # arrays for dictionary
        pe_sections = []
        dlls = {}

        count = 0
        for data_dict in db_data:
            count += 1
            progress(count, limit_data)
            
            obj = dict(data_dict)

            # add to pe_sections dict
            if 'static' in obj and 'pe_sections' in obj['static']:
                for section in obj['static']['pe_sections']:
                    if section['name'].lower() and section['name'].lower() not in pe_sections:
                        pe_sections.append(section['name'].lower())

            if 'static' in obj and 'pe_imports' in obj['static']:
                for imp in obj['static']['pe_imports']:
                    dll = imp['dll'].lower()

                    if dll and dll not in dlls:
                        dlls[dll] = []

                    for i in imp['imports']:
                        if i['name'] and not i['name'].lower() in dlls[dll]:
                            dlls[dll].append(i['name'].lower())

        print()

        save_data(pe_sections, os.path.join(output_path, 'pe_sections.pkl'))
        save_data(dlls, os.path.join(output_path, 'pe_imports_dll.pkl'))
