import re
import time

from BaseColor.base_colors import hred


def tell_the_datetime(time_stamp=None, compact_mode=False, date_sep="-", time_sep=":"):
    time_stamp = time_stamp if time_stamp else time.time()
    if not compact_mode:
        format_str = f'%Y{date_sep}%m{date_sep}%d %H{time_sep}%M{time_sep}%S'
    else:
        format_str = f'%Y{date_sep}%m{date_sep}%d{date_sep}%H{date_sep}%M{date_sep}%S'
    tm = time.strftime(format_str, time.gmtime(time_stamp + (8 * 3600)))
    return tm


def tell_timestamp(time_str=None, str_format='%Y-%m-%d-%H-%M-%S'):
    if time_str:
        time_lis = re.findall(r'\d+', time_str)
        sep_list = re.findall(r"[^\d]+", time_str)
        str_format = ''
        format_base = ["%Y", "%m", "%d", "%H", "%M", "%S"]
        for i in range(len(time_lis)):
            if i < len(sep_list):
                str_format += format_base[i] + sep_list[i]
            else:
                str_format += format_base[i]
    else:
        time_str = tell_the_datetime(compact_mode=True)
    try:
        return int(time.mktime(time.strptime(time_str, str_format)))
    except ValueError as V:
        print(f"[ tell_timestamp ] Error: {V}")
        raise KeyboardInterrupt


def waiting(reset_time, warning, stop_wait_warning, wait_only=True, print_out=False):
    rs_t = int(time.mktime(time.strptime(reset_time, "%Y-%m-%d %H:%M:%S")))
    reset_wait = rs_t + 1 - int(time.time())

    def func(rw):
        print()
        print(warning)
        while rw >= 0:
            if print_out:
                m, s = divmod(rw, 60)
                h, m = divmod(m, 60)
                print(f'warning: which is [ \033[1;31;48m{h}:{m}:{s}\033[0m ] later\r', end='')
            rw -= 1
            time.sleep(1)
        print()

    try:
        if wait_only:
            func(reset_wait)
        else:
            mi, sc = divmod(reset_wait, 60)
            ho, mi = divmod(mi, 60)
            print(f'warning: which is [ {hred(f"{ho}:{mi}:{sc}")} ] later')
            time.sleep(reset_wait)
        return True
    except KeyboardInterrupt:
        print()
        print(stop_wait_warning)
        count_down = 10
        wait_for(count_down)
        print()
        return False


def wait_for(t, head="wait for"):
    count_down = t
    while count_down >= 0:
        print(f"{head}: [ \033[1;31;48m{count_down}\033[0m ]\r", end='')
        time.sleep(1)
        count_down -= 1
