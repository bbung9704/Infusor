from datetime import datetime, timezone, timedelta

def get_time():
    KST = timezone(timedelta(hours=9))
    time_record = datetime.now(KST)
    _day = str(time_record)[:10]
    _time = str(time_record.time())[:8]

    return _day + ' ' + _time   # 2023-11-18 14:35:36