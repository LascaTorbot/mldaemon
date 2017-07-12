import utils

data = utils.load_data('../analysis.pkl')
pe_sections = utils.load_data('../dicts/pe_sections.pkl')
pe_imports_dict = utils.load_data('../dicts/pe_imports_dll.pkl')

# put the keys in order
pe_imports = []
for k in pe_imports_dict:
    pe_imports.append((k, pe_imports_dict[k]))

dataset = []
count = 0
limit = len(data)

for obj in data:
    count += 1
    utils.progress(count, limit)

    X = []
    if 'static' in obj and 'pe_sections' in obj['static']\
            and 'pe_imports' in obj['static']:

        ## pe_sections
        names = [n['name'] for n in obj['static']['pe_sections']]

        for section in pe_sections:
            X.append(1 if section in names else 0)

        ## pe_imports
        for dll_name, funs in pe_imports:
            gen = False

            for dll in obj['static']['pe_imports']:
                if dll['dll'] == dll_name:
                    gen = True
                    X.append(1)
                    
                    imports_funs = [f['name'] for f in dll['imports']]
                    for fun in funs:
                        X.append(1 if fun in imports_funs else 0)

                    break
            
            if not gen:
                X.append(0)
                for fun in funs:
                    X.append(0)

        dataset.append((X, obj['label']))

# output labeled features
features = pe_sections
for dll_name, funs in pe_imports:
    features.append(dll_name)
    for f in funs:
        features.append(f)

print()
utils.save_data(features, 'features.pkl')

print('\n')
utils.save_data(dataset, 'dataset.pkl')
