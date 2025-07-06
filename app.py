import streamlit as st
import pandas as pd
from planner import TIME_SLOTS, WEEKDAYS, create_teacher_calendar
from scheduler import assign_course, release_slot

st.title("📚 Semesterplanung: Kursübersicht pro Lehrkraft")

uploaded_file = st.file_uploader("Excel-Datei mit Kursdaten hochladen", type=["xlsx"])

if "update_trigger" not in st.session_state:
    st.session_state.update_trigger = 0

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_cols = {"Kursnummer", "Kursname", "Lehrkraft", "SWS"}
    if not required_cols.issubset(set(df.columns)):
        st.error("❌ Die Datei muss die Spalten: Kursnummer, Kursname, Lehrkraft, SWS enthalten.")
    else:
        # Kurse und Lehrkräfte vorbereiten
        courses = df.rename(columns={
            "Kursnummer": "nummer",
            "Kursname": "name",
            "Lehrkraft": "lehrkraft",
            "SWS": "sws"
        })[["nummer", "name", "lehrkraft", "sws"]].to_dict(orient="records")

        lehrkraefte = sorted(set(df["Lehrkraft"].dropna()))

        # Kalender vorbereiten
        if "calendar" not in st.session_state:
            st.session_state.calendar = create_teacher_calendar(lehrkraefte)

        calendar = st.session_state.calendar

        selected_teacher = st.selectbox("Lehrkraft wählen", lehrkraefte)

        # Wochenübersicht als Tabelle anzeigen
        def render_schedule_table(calendar, selected_teacher, weekdays, time_slots):
            html = "<table style='width:100%; border-collapse: collapse;'>"
            html += "<tr><th style='border: 1px solid black;'>Zeit</th>"
            for tag in weekdays:
                html += f"<th style='border: 1px solid black;'>{tag}</th>"
            html += "</tr>"

            for i, (start, end) in enumerate(time_slots):
                html += f"<tr><td style='border: 1px solid black; padding:4px;'>{start} – {end}</td>"
                for tag in weekdays:
                    kurs = calendar[selected_teacher][tag][i]
                    text = kurs if kurs else "–"
                    html += f"<td style='border: 1px solid black; padding:4px; text-align:center;'>{text}</td>"
                html += "</tr>"

            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)

        calendar_placeholder = st.empty()

        def show_calendar():
            with calendar_placeholder:
                st.markdown(f"🔄 Änderung #{st.session_state.update_trigger}")
                render_schedule_table(calendar, selected_teacher, WEEKDAYS, TIME_SLOTS)

        st.subheader(f"📅 Wochenübersicht – {selected_teacher}")
        show_calendar()

        # Kursauswahl
        st.subheader("📝 Kurs zuweisen")
        teacher_courses = [k for k in courses if k["lehrkraft"] == selected_teacher]
        kurs_options = [f'{k["nummer"]} – {k["name"]} ({k["sws"]} SWS)' for k in teacher_courses]
        kurs_selection = st.selectbox("Kurs auswählen", kurs_options)

        selected_kurs = next(k for k in teacher_courses if str(k["nummer"]) in kurs_selection)

        kursname = selected_kurs["name"]
        sws = selected_kurs["sws"]

        # Slot auswählen
        tag = st.selectbox("Wochentag", WEEKDAYS)
        slot_index = st.selectbox("Zeitslot", list(enumerate([f"{s}–{e}" for s, e in TIME_SLOTS])))

        if st.button("✅ Kurs zuweisen"):
            success, message = assign_course(calendar, selected_teacher, tag, slot_index[0], kursname, sws)
            if success:
                st.success(message)
                st.session_state.update_trigger += 1
                show_calendar()
            else:
                st.warning(message)

        st.subheader("🧹 Slot löschen")
        if st.button("🗑️ Slot freigeben"):
            released = release_slot(calendar, selected_teacher, tag, slot_index[0], kursname)
            if released:
                st.success("Slot wurde gelöscht.")
                st.session_state.update_trigger += 1
                show_calendar()
            else:
                st.warning("Slot gehört nicht zu diesem Kurs oder war leer.")
else:
    st.info("⬆️ Bitte lade zuerst eine gültige Excel-Datei hoch.")
