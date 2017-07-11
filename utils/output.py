import sys

def progress(count, limit):
    sys.stdout.write('\rProgress: %d / %d' % (count, limit))
    sys.stdout.flush()
