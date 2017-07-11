import pickle

def load_data(name):
    print("Loading %s..." % name)
    data = pickle.load(open(name, 'rb'))
    print("Success!")

    return data


def save_data(data, name):
    print("Saving dict with %d entries..." % len(data))
    pickle.dump(data, open(name, 'wb'))
    print("Success!")
