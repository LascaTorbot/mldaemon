import utils

# load data
data = utils.load_data()

pe_sections = []
count = 0
limit = len(data)

for obj in data:
    count += 1
    utils.progress(count, limit)

    if 'static' in obj and 'pe_sections' in obj['static']:
        for section in obj['static']['pe_sections']:
            if section['name'].lower() and section['name'].lower() not in pe_sections:
                pe_sections.append(section['name'].lower())

print()

utils.save_data(pe_sections, 'pe_sections.pkl')
