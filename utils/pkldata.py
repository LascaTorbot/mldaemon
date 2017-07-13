import pickle

def load_data(name):
    data = pickle.load(open(name, 'rb'))

    return data


def save_data(data, name):
    pickle.dump(data, open(name, 'wb'))
