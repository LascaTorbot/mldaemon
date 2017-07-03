import utils

# load data
data = utils.load_data()

dlls = {}
count = 0
limit = len(data)

for obj in data:
    count += 1
    utils.progress(count, limit)

    if 'static' in obj and 'pe_imports' in obj['static']:
        for imp in obj['static']['pe_imports']:
            dll = imp['dll'].lower()

            if dll and dll not in dlls:
                dlls[dll] = []

            for i in imp['imports']:
                if i['name'] and not i['name'].lower() in dlls[dll]:
                    dlls[dll].append(i['name'].lower())

print()
utils.save_data(dlls, 'pe_imports_dll.pkl')
