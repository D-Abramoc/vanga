import datetime as dt


def get_end_of_period(start_date: str, time_delta: int) -> str:
    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_time = start + dt.timedelta(days=time_delta)
    return end_time.strftime('%Y-%m-%d')


def get_query_params(query_params) -> list[str]:
    res = dict(
        [
            (key, query_params.getlist(key))
            for key in query_params
        ]
    )
    end_time = get_end_of_period(
        res['start_date'][0], int(res['time_delta'][0])
    )
    res.pop('time_delta')
    res['end_date'] = end_time
    return res
