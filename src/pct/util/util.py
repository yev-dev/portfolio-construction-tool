def print_dictionary(d, indent=0):

    for key, value in d.items():
        print('\t' * indent + str(key) + ":")
        if isinstance(value, dict):
            print_dictionary(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))
