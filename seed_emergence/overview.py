"""已有资料的描述性概览。"""
def summarize(data):
    rows = data["rows"]
    return {'climate_days': sum(row['kind'] == 'climate' for row in rows), 'inspection_records': sum(row['kind'] == 'inspection' for row in rows), 'destructive_draws': sum(row.get('destructive_removed', 0) > 0 for row in rows), 'houses': sorted(data['houses'])}
