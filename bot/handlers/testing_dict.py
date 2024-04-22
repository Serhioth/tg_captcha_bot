data = {
    'category_1': ['service_1', 'service_2'],
    'category_2': ['service_3', 'service_4'],
}

for category in data.keys():
    print(f'{category}')
    for service in data[category]:
        print(f'\t{service}')
