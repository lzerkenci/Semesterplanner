from datetime import datetime, timedelta


def str_to_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

def time_to_str(time_obj):
    return time_obj.strftime("%H:%M")

def generate_time_slots(start_time, end_time, duration=90, step=15):
    slots = []
    current_time = start_time
    delta_duration = timedelta(minutes=duration)
    delta_step = timedelta(minutes=step)

    while current_time + delta_duration <= end_time:
        slot_end = current_time + delta_duration
        slots.append((current_time, slot_end))
        current_time += delta_step

    return slots

def overlaps(str1, end1, str2, end2, min_minutes=15):
    fmt = "%H:%M"
    t1_start = datetime.strptime(str1, fmt)
    t1_end = datetime.strptime(end1, fmt)
    t2_start = datetime.strptime(str2, fmt)
    t2_end = datetime.strptime(end2, fmt)

    overlap_start = max(t1_start, t2_start)
    overlap_end = min(t1_end, t2_end)

    return (overlap_end - overlap_start) >= timedelta(minutes=min_minutes)
