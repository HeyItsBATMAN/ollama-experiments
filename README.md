## Einrichtung (Setup)

Folge diesen Schritten in deinem Terminal/Command Prompt:

### 1. Virtuelle Umgebung erstellen
Eine virtuelle Umgebung (venv) sorgt dafür, dass die installierten Bibliotheken nur für dieses Projekt gelten und dein System sauber bleibt.

*   **Windows:**
    ```bash
    python -m venv .venv
    ```
*   **MacOS / Linux:**
    ```bash
    python -m venv .venv
    # Oder
    python3 -m venv .venv
    ```

### 2. Virtuelle Umgebung aktivieren
Du musst die Umgebung aktivieren, bevor du sie nutzen kannst.

*   **Windows (Command Prompt):**
    ```cmd
    .venv\Scripts\activate
    ```
*   **Windows (PowerShell):**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
*   **MacOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```

*(Du erkennst die aktive Umgebung meist an einem `(.venv)` vor deiner Eingabeaufforderung.)*

### 3. Abhängigkeiten installieren
Installiere nun alle benötigten Bibliotheken aus der `requirements.txt`:
```bash
pip install -r requirements.txt
# Oder
pip3 install -r requirements.txt
```

---

## Vorbereitung in LM Studio

Bevor du die Skripte ausführst, musst du LM Studio vorbereiten:

1. Öffne **LM Studio**.
2. Gehe zum Tab **"Developer"** (das `< >` Symbol auf der linken Seite).
3. Stelle sicher, dass der **LM Studio Server** gestartet ist (meist auf Port 1234).
4. Das SDK verbindet sich automatisch mit diesem Server.

---

## Die Experimente ausführen

Die Dateien sind nummeriert und bauen inhaltlich aufeinander auf. Stelle sicher, dass deine virtuelle Umgebung aktiviert ist.

```bash
python name-vom-skript.py
# Oder
python3 name-vom-skript.py
```
