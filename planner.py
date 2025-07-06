from collections import defaultdict


TIME_SLOTS = [
    ("09:45", "11:15"),
    ("11:30", "13:00"),
    ("13:15", "14:45"),
    ("15:00", "16:30"),
    ("16:45", "18:15"),
    ("18:30", "20:00"),
    ("20:15", "21:45")
]

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

def create_teacher_calendar(lehrkraefte):
    return defaultdict(lambda: defaultdict(lambda: [None] * len(TIME_SLOTS)))