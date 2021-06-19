from datetime import datetime, timedelta, timezone


class TimeZoneChina:
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    @classmethod
    def now(cls):
        '''
        北京时间
        '''
        return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(cls.SHA_TZ)
    
    @classmethod
    def get_now(cls, year: int, month: int, day: int):
        '''
        北京时间
        '''
        return datetime(year, month, day).replace(tzinfo=timezone.utc).astimezone(cls.SHA_TZ)

    @classmethod
    def china_now(cls, year: int, month: int, day: int):
        '''
        北京时间
        '''
        return datetime(year, month, day, 8).replace(tzinfo=timezone.utc).astimezone(cls.SHA_TZ)

    @classmethod
    def format(cls, dt: datetime, format_str: str) -> str:
        if not format_str:
            format_str = '%Y-%m-%dT%H:%M:%SZ'
        return dt.strftime(format_str)
