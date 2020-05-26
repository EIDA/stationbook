import threading


class BackgroundThread(object):
    def __init__(self, target_method):
        self.thread = threading.Thread(target=target_method, args=())
        self.thread.daemon = True

    def run(self):
        self.thread.start()

    def is_alive(self):
        if self.thread.isAlive():
            return True
        else:
            return False
