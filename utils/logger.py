from datetime import datetime
import os

class Logger:
    def __init__(self, path):
        # creates the file
        self.filename = os.path.join(path, datetime.now().strftime('%Y-%m-%d.%H:%M:%S.log'))
        self.queue = []

        with open(self.filename, 'w') as f:
            f.write('')

    def log(self, s):
        self.queue.append('[%s]: %s' % (datetime.now().strftime('%H:%M:%S'), s))

    def flush(self):
        with open(self.filename, 'a') as f:
            f.write('\n'.join(self.queue) + '\n')
            self.queue = []
