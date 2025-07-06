
def count_slots_for_course(calendar, lehrkraft, kurstitel):
    count = 0
    for tag in calendar[lehrkraft]:
        count += calendar[lehrkraft][tag].count(kurstitel)
    return count

def assign_course(calendar, lehrkraft, tag, slot_index, kurstitel, sws):
    if calendar[lehrkraft][tag][slot_index]:
        return False, "Slot bereits belegt"

    belegt = count_slots_for_course(calendar, lehrkraft, kurstitel)
    must_slots = sws // 2

    if belegt >= must_slots:
        return False, f"Kurs hat bereits {must_slots} slots"

    calendar[lehrkraft][tag][slot_index] = kurstitel
    belegt +=1

    if belegt < must_slots:
        return True, f"Kurs hat bereits {must_slots} slot vergeben! Bitte noch einen auswählen."

    return True, "Kurs vollständig eingetragen"

def release_slot(calendar, lehrkraft, tag, slot_index, kurstitel=None):
    aktueller_kurs = calendar[lehrkraft][tag][slot_index]

    if aktueller_kurs and aktueller_kurs == kurstitel:
        calendar[lehrkraft][tag][slot_index] = None
        return True
    return False