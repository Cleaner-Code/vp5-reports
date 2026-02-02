# SOP: OpenProject Cost Report → Google Sheets Konvertierung

**Version:** 1.0  
**Erstellt:** 2026-02-02  
**Zweck:** Standardisierter Prozess zur Konvertierung von OpenProject Cost Reports in das VP5-2025 Google Sheets Format

---

## 📋 Übersicht

Dieser Prozess konvertiert OpenProject Cost Reports von einem detaillierten Format mit vielen Spalten in ein kompaktes Google Sheets Format mit gruppierten Stunden pro Tag und extrahierten Task-IDs.

**Zeitaufwand:** ~5 Minuten  
**Häufigkeit:** Monatlich oder nach Bedarf

---

## 🎯 Ziel

**Von:**
- Detaillierte OpenProject XLS-Exporte mit einzelnen Zeiteinträgen pro User/Task
- 9 Spalten mit vielen redundanten Informationen

**Zu:**
- Kompaktes Google Sheets Format
- 5 Spalten: Projekt, Datum, Stunden (Summe), Task-IDs, Manuelle Korrektur
- Gruppiert nach Tag mit summierten Stunden

---

## 📸 Screenshots

### OpenProject Cost Report

![OpenProject Report](openproject_report_screenshot.png)

**URL:** https://openproject.cleanercode.de/projects/vp5-2025/cost_reports/4

---

## 🔧 Voraussetzungen

### Software
- Python 3.11 oder höher
- Pandas, openpyxl, xlrd (bereits installiert)

### Zugriff
- OpenProject Account mit Zugriff auf VP5-2025 Projekt
- Google Sheets Zugriff auf das Ziel-Sheet

### Dateien
- `convert_openproject_report.py` im Projekt-Verzeichnis

---

## 📝 Schritt-für-Schritt Anleitung

### Schritt 1: OpenProject Cost Report exportieren

1. **Öffne OpenProject**
   - URL: https://openproject.cleanercode.de/projects/vp5-2025/cost_reports/4

2. **Konfiguriere den Report**
   - **Filter:**
     - Project: `VP5 - 2025`
     - Date (Spent): `between` → Wähle Zeitraum (z.B. 2026-01-01 bis 2026-01-31)
   
   - **Group by:**
     - Columns: `Month (Spent)`, `Year (Spent)`
     - Rows: `Project`, `Date (Spent)`, `Work package`, `User`
   
   - **Units:**
     - ☑ Labor (ausgewählt)

3. **Klicke auf "Apply"**

4. **Exportiere als XLS**
   - Klicke auf "Save" Button
   - Wähle "XLS" Format
   - Datei wird heruntergeladen (z.B. `cost-report-2026-02-02-T-11-34-4120260202-7-p8jkg3.xls`)

5. **Verschiebe die Datei**
   ```bash
   mv ~/Downloads/cost-report-*.xls ~/projects/vp5_reports/
   ```

---

### Schritt 2: Konvertierung ausführen

1. **Öffne Terminal**

2. **Navigiere zum Projekt-Verzeichnis**
   ```bash
   cd ~/projects/vp5_reports
   ```

3. **Führe das Konvertierungs-Skript aus**
   ```bash
   python3.11 convert_openproject_report.py <dateiname.xls>
   ```
   
   **Beispiel:**
   ```bash
   python3.11 convert_openproject_report.py cost-report-2026-02-02-T-11-34-4120260202-7-p8jkg3.xls
   ```

4. **Überprüfe die Ausgabe**
   - Das Skript zeigt eine Vorschau der konvertierten Daten
   - Output-Datei: `converted_report.csv` (oder mit Datum: `converted_report_20260202.csv`)

**Erwartete Ausgabe:**
```
📖 Lese Datei: cost-report-2026-02-02-T-11-34-4120260202-7-p8jkg3.xls
✅ 26 Einträge geladen
📊 12 Tage gruppiert

Vorschau:
   Projekt      Datum  Stunden (Summe)           Task-IDs  Manuelle Korrektur
VP5 - 2025 2026-01-12             5.00 VP5-2745, VP5-2762                5.00
VP5 - 2025 2026-01-13             5.00 VP5-2745, VP5-2762                5.00
...

✅ Konvertierung abgeschlossen!
📁 Ausgabe: converted_report.csv
```

---

### Schritt 3: Import in Google Sheets

1. **Öffne das Ziel-Google Sheet**
   - URL: https://docs.google.com/spreadsheets/d/11UM8dUUrX7ZRyeexesznITPOmnk3EtOBpUB1RoFVNjc/edit

2. **Importiere die CSV**
   - Klicke auf **Datei** → **Importieren**
   - Wähle **Upload** Tab
   - Ziehe `converted_report.csv` in das Upload-Feld oder klicke "Datei auswählen"

3. **Import-Einstellungen**
   - **Importort:** "Daten ersetzen" oder "Neues Tabellenblatt"
   - **Trennzeichen:** Komma (wird automatisch erkannt)
   - **Text in Zahlen/Daten konvertieren:** ☑ Ja

4. **Klicke "Daten importieren"**

---

### Schritt 4: Manuelle Korrektur (Spalte E)

1. **Überprüfe die importierten Daten**
   - Spalte A: Projekt (VP5 - 2025)
   - Spalte B: Datum (YYYY-MM-DD)
   - Spalte C: Stunden (Summe)
   - Spalte D: Task-IDs (z.B. "VP5-2745, VP5-2762")
   - Spalte E: Manuelle Korrektur (enthält Original-Stunden)

2. **Bearbeite Spalte E nach Bedarf**
   - Enthält die Original-Stunden aus OpenProject
   - Passe die Werte an, falls nötig (z.B. auf 8h für Vollzeit-Tage)
   - Dies ist die Spalte für manuelle Korrekturen

3. **Speichern**
   - Google Sheets speichert automatisch

---

## ✅ Qualitätskontrolle

### Checkliste nach jedem Import

- [ ] Alle Tage aus dem OpenProject Report sind vorhanden
- [ ] Stunden-Summen pro Tag sind korrekt
- [ ] Task-IDs sind sauber extrahiert (Format: VP5-XXXX)
- [ ] Keine Duplikate in den Task-IDs
- [ ] Spalte E (Manuelle Korrektur) hat Original-Werte
- [ ] Datum-Format ist YYYY-MM-DD

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| **"No module named 'pandas'"** | `pip3 install pandas openpyxl xlrd` |
| **"File not found"** | Überprüfe Dateinamen und Pfad |
| **Keine Task-IDs extrahiert** | Task-Beschreibungen müssen "VP5-XXXX" Format enthalten |
| **Falsche Stunden-Summen** | Überprüfe OpenProject Filter-Einstellungen |

---

## 🔄 Automatisierung (Optional)

### Für wiederkehrende Nutzung

**Option 1: Bash-Alias erstellen**
```bash
# In ~/.zshrc hinzufügen:
alias convert-vp5='cd ~/projects/vp5_reports && python3.11 convert_openproject_report.py'
```

**Option 2: Google Apps Script** (Zukünftig)
- Konvertierung direkt in Google Sheets
- Button-Click-Lösung
- Keine lokale Installation nötig

---

## 📊 Beispiel-Output

### Input (OpenProject XLS)
```
Date (Spent) | User          | Activity    | Logged for                    | Units
-------------|---------------|-------------|-------------------------------|------
2026-01-12   | Philipp Herda | -           | Task #6748: [VP5-2745]...     | 1
2026-01-12   | Tobias Vetter | Development | Task #6907: VP5-2762...       | 4
```

### Output (Google Sheets CSV)
```
Projekt      | Datum      | Stunden (Summe) | Task-IDs           | Manuelle Korrektur
-------------|------------|-----------------|--------------------|-----------------
VP5 - 2025   | 2026-01-12 | 5.0             | VP5-2745, VP5-2762 | 5.0
```

---

## 📞 Support

**Bei Problemen:**
1. Überprüfe die Checkliste oben
2. Schaue in die [README.md](README.md) für Details
3. Kontaktiere Marco Brinkmeier

---

## 📝 Änderungshistorie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-02-02 | Initiale SOP erstellt |

---

## 🎯 Nächste Schritte nach Import

1. **Überprüfe die Daten** auf Vollständigkeit
2. **Bearbeite Spalte E** (Manuelle Korrektur)
3. **Archiviere die XLS-Datei** (optional)
4. **Fertig!** 🎉
