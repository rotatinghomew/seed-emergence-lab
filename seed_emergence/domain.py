"""独立业务规则，仅依赖冻结资料。"""
def quote(data, request):
    house = request['house']
    start, end = int(request['start_day']), int(request['end_day'])
    if house not in data['houses'] or start < 0 or end < start or end > 35:
        raise ValueError('温室或积温区间非法')
    observations = [row for row in data['rows'] if row['kind'] == 'climate' and row['house'] == house and start <= row['day'] < end]
    covered = len(observations)
    degree_days = sum(max(0, row['temperature_c'] - data['base_temperature_c']) for row in observations if not row['offline'])
    offline = [row['day'] for row in observations if row['offline']]
    return {'degree_days': round(degree_days, 4), 'covered_days': covered,
            'expected_days': end - start, 'offline_days': offline,
            'base_temperature_c': data['base_temperature_c'],
            'climate_version': data['climate_version']}

def capacity(data, request):
    house = request['house']
    if house not in data['houses']:
        raise ValueError('温室不存在')
    return {'house': house, 'cells_per_tray': data['houses'][house]['cells_per_tray'],
            'post_emergence_days': data['houses'][house]['post_emergence_days'],
            'order_deadlines': data['order_deadlines']}

detail = capacity
