import utils

# load data
data = utils.load_data()

names = []
count = 0
limit = len(data)

for obj in data:
    count += 1
    utils.progress(count, limit)

    if 'static' in obj and 'pe_imports' in obj['static']:
        for imp in obj['static']['pe_imports']:
            if 'imports' in imp:
                for i in imp['imports']:
                    if i['name'] and i['name'] not in names:
                        names.append(i['name'])

print()
utils.save_data(names, 'pe_imports_name.pkl')
