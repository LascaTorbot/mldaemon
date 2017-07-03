import pickle
import sys

def load_data():
    print("Loading data...")
    data = pickle.load(open('../analysis.pkl', 'rb'))
    print("Success!")

    return data

def progress(count, limit):
    sys.stdout.write('\rProgress: %d / %d' % (count, limit))
    sys.stdout.flush()

def save_data(data, name):
    print("Saving dict with %d entries..." % len(data))
    pickle.dump(data, open(name, 'wb'))
    print("Success!")
