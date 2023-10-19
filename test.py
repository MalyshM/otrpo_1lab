my_dict = {'key1': 'value1', 'key2': None, 'key3': 'value3'}

# Check if any value is None
if None in my_dict.values():
    print("None value found in the dictionary")
else:
    print("No None value found in the dictionary")