def seconds_to_time_str(seconds: float) -> str:
    hours = int(seconds/3600)
    seconds -= hours*3600

    minutes = int(seconds/60)
    seconds -= minutes*60

    millis = seconds - int(seconds)
    seconds = int(seconds)
    time_str = ''

    if hours > 0:
        time_str = str(hours).zfill(2)

    if minutes > 0 or len(time_str) > 0:
        if len(time_str) > 0:
            time_str += ':'

        time_str += str(minutes).zfill(2)

    if seconds > 0 or len(time_str) > 0:
        if len(time_str) > 0:
            time_str += ':'

        time_str += str(seconds).zfill(2)

    if millis > 0:
        time_str += '.'

        time_str += str(int(millis*1000)).rstrip('0')

    return time_str

def time_str_to_seconds(time_str: str) -> float:
    return sum([float(c) * pow(60, i) for i, c in enumerate(reversed(time_str.split(':')))])

def is_between_hours_utc(start_h_utc: float, stop_h_utc: float) -> bool:
    return is_between_seconds_utc(start_h_utc*3600, stop_h_utc*3600)

def is_between_seconds_utc(start_s_utc: float, stop_s_utc: float) -> bool:
        s_in_day = 60*60*24

        if start_s_utc >= s_in_day:
            start_s_utc -= s_in_day

        if stop_s_utc >= s_in_day:
            stop_s_utc -= s_in_day

        now_s = current_sec_utc()

        if start_s_utc < stop_s_utc:
            return now_s >= start_s_utc and now_s < stop_s_utc
        elif start_s_utc > stop_s_utc:
            return now_s < start_s_utc or now_s >= stop_s_utc

        return False

def hours_till(h_utc: float) -> float:
    return seconds_till(h_utc*3600)/3600

def seconds_till(s_utc: float) -> float:
    now_s = current_sec_utc()

    if s_utc >= now_s:
        return s_utc - now_s

    return 24*3600 - now_s + s_utc

def current_hour_utc() -> float:
    return current_sec_utc() / 3600

def current_sec_utc() -> float:
    from datetime import datetime

    now = datetime.utcnow()

    return now.hour*3600 + now.minute*60 + now.second