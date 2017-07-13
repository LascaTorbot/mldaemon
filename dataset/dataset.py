from mldaemon.utils.output import *
from mldaemon.utils.pkldata import *
from pymongo import MongoClient
import numpy as np
import os

MIN_POSITIVES_RATE = 0.51

class Dataset:
    def __init__(self, mongo_host, mongo_port, dict_path):
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client.cuckoo

        # loading dictionary files
        self.pe_sections = load_data(os.path.join(dict_path, 'pe_section.pkl'))
        self.pe_imports_dict = load_data(os.path.join(dict_path, 'pe_imports_dict.pkl'))

        # put the keys in order
        self.pe_imports = []
        for k in pe_imports_dict:
            self.pe_imports.append((k, pe_imports_dict[k]))

    def get_dataset(self):
        """
        This func returns a tuple with numpy objects, in order (X, y)
        """
        
        X_data = []
        y_data = []

        # loading data from mongodb
        limit_data = self.db.analysis.count()
        db_data = self.db.analysis.find()
        count = 0
        for data_dict in db_data:
            count += 1
            progress(count, limit_data)

            obj = dict(data_dict)

            X = []
            if 'static' in obj and 'pe_sections' in obj['static']\
                    and 'pe_imports' in obj['static'] and 'virustotal' in obj:

                ## pe_sections
                names = {}
                for n in obj['static']['pe_sections']:
                    names[n['name']] = [int(n['size_of_data'], 16), int(n['virtual_address'], 16),
                                        n['entropy'], int(n['virtual_size'], 16)]

                for section in self.pe_sections:
                    if section in names:
                        X.extend(names[section])
                    else:
                        X.extend([0, 0, 0, 0)

                ## pe_imports
                for dll_name, funs in self.pe_imports:
                    gen = False

                    for dll in obj['static']['pe_imports']:
                        if dll['dll'].lower() == dll_name:
                            gen = True
                            
                            imports_funs = {}
                            for f in dll['imports']:
                                imports_funs[f['name'].lower()] = int(f['address'], 16)

                            for fun in funs:
                                if fun in imports_funs:
                                    X.append(imports_funs[fun])
                                else:
                                    X.append(0)

                            break
                    
                    if not gen:
                        for fun in funs:
                            X.append(0)

                X_data.append(np.array(X))

                # check y label with virus_total submission
                if obj['virustotal']['positives'] / obj['virustotal']['total'] >= MIN_POSITIVES_RATE:
                    y_data.append(1)
                else:
                    y_data.append(0)

       return (np.array(X_data), np.array(y_data)) 
