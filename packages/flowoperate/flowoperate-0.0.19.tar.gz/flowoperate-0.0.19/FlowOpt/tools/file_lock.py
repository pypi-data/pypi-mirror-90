import os
import platform
import time


def tell_the_datetime(time_stamp=None, compact_mode=False, date_sep="-", time_sep=":"):
    time_stamp = time_stamp if time_stamp else time.time()
    if not compact_mode:
        format_str = f'%Y{date_sep}%m{date_sep}%d %H{time_sep}%M{time_sep}%S'
    else:
        format_str = f'%Y{date_sep}%m{date_sep}%d{date_sep}%H{date_sep}%M{date_sep}%S'
    tm = time.strftime(format_str, time.gmtime(time_stamp + (8 * 3600)))
    return tm


def wait_until_file_not_exists(file):
    while os.path.exists(file):
        time.sleep(0.1)
    with open(file, 'w') as rf:
        rf.write(tell_the_datetime())


class FLock(object):
    def __init__(self):
        if platform.system() == "Linux":
            self.lock_dir = "/tmp/"
        else:
            self.lock_dir = "C:\\tmp\\"
        self.lock_file = os.path.join(self.lock_dir, 'flow.lock')

    def acquire(self, block=True):
        if block:
            wait_until_file_not_exists(self.lock_file)
        else:
            with open(self.lock_file, 'w') as rf:
                rf.write(tell_the_datetime())

    def release(self):
        try:
            os.remove(self.lock_file)
        except Exception as E:
            pass

    def __del__(self):
        self.release()


if __name__ == '__main__':
    fl = FLock()
    fl.acquire()
    print("lock aq")
    fl.release()
    print("lock re")
