# Flashcards Generator

Questo progetto automatizza la creazione di applicazioni di flashcard web interattive e autocontenute a partire da semplici file di testo.

## Architettura del Progetto

-   `_inbox/`: **Cartella di ingresso temporanea.** Contiene i file `.txt` da processare. I file in questa cartella vengono archiviati (spostati) dopo una generazione avvenuta con successo.
-   `outputs/`: Cartella di output. Contiene i progetti di flashcard generati. Ogni sottocartella è **autocontenuta** e include sia la web app (`.html`) sia il file sorgente (`.txt`) originale.
-   `src/`: Contiene il codice sorgente per l'automazione.
    -   `main.py`: Lo script Python che orchestra l'intero processo.
    -   `templates/flashcard_template.html`: Il template HTML per la web app.
-   `README.md`: Questo file.
-   `requirements.txt`: Dipendenze Python del progetto.

---

## Funzionalità dell'Applicazione Generata

L'applicazione HTML creata è un'interfaccia di studio moderna e interattiva con le seguenti caratteristiche:

-   **Animazione 3D**: Le card si girano con un'animazione fluida cliccando su di esse.
-   **Contatore Interattivo (Filtro Visualizzazione)**: Il contatore (es. "1 / 50 totali") è cliccabile e funge da selettore di modalità:
    -   **Modalità "totali"**: Mostra tutte le card del set.
    -   **Modalità "attive"**: Mostra solo le card contrassegnate come attive (con la stella).
-   **Stato Attivo/Inattivo (Stella)**: Cliccando sull'icona a forma di stella (★), è possibile contrassegnare o de-contrassegnare una card. Le card inattive vengono saltate quando si è in modalità "attive".
-   **Copia negli Appunti**: L'icona a forma di clipboard (📋) permette di copiare istantaneamente la domanda e la risposta della card corrente in formato testo.

---

## Workflow Automation Protocol (for AI Agents)

Questo protocollo descrive i passaggi da seguire per generare una nuova applicazione di flashcard.

### Fase 1: Identificazione dell'Input

1.  **Ispeziona la cartella `_inbox/`**: Cerca un file di testo (`.txt`) contenente le domande e le risposte.
2.  **Gestisci i file multipli**: Se è presente più di un file, chiedi all'utente quale file specifico utilizzare.
3.  **Gestisci l'assenza di file**: Se la cartella è vuota, informa l'utente che non è possibile procedere e interrompi il workflow.

### Fase 2: Interazione con l'Utente

1.  **Richiedi il nome del progetto**: Poni all'utente la seguente domanda: "**Qual è il nome del progetto per queste flashcard?**"
2.  **Memorizza la risposta**: Conserva il nome fornito dall'utente (es. "Biologia Sistema Vestibolare") per utilizzarlo nello step successivo.

### Fase 3: Esecuzione dello Script

1.  **Prepara il comando**: Costruisci il comando per eseguire lo script Python `src/main.py`. Il comando richiede due argomenti:
    1.  Il percorso del file di input individuato nella Fase 1.
    2.  Il nome del progetto fornito dall'utente nella Fase 2 (racchiuso tra virgolette per gestire gli spazi).
2.  **Esegui il comando**: Lancia il seguente comando nel terminale dalla root del progetto:
    ```bash
    python src/main.py "<percorso_file_input>" "<nome_progetto>"
    ```
    **Esempio Pratico:**
    ```bash
    python src/main.py "_inbox/sistema_vestibolare.txt" "Sistema Vestibolare"
    ```
    Lo script creerà una cartella di progetto in `outputs/` (es. `outputs/sistema_vestibolare/`) contenente sia il file `.html` generato sia una copia del file `.txt` sorgente.

### Fase 4: Verifica, Conferma e Archiviazione

1.  **Comunica il risultato**: Informa l'utente che la generazione è completata e fornisci il percorso del file HTML generato (es. `outputs/sistema_vestibolare/sistema_vestibolare.html`).
2.  **Richiedi conferma**: Chiedi all'utente di testare il file e di confermare che funzioni correttamente. Attendi la sua approvazione esplicita.
3.  **Archivia il file sorgente (dopo conferma)**: Una volta ricevuta la conferma dall'utente, sposta il file `.txt` originale dalla cartella `_inbox/` alla cartella del progetto appena creata in `outputs/`. Se lo script ha già copiato il file, puoi semplicemente eliminare il file originale da `_inbox`. Lo scopo è svuotare la cartella di ingresso.

    **Comando Esempio (per eliminare il file da `_inbox`):**
    ```bash
    rm "_inbox/sistema_vestibolare.txt"
    ```
4.  **Conferma il completamento**: Comunica all'utente che il file sorgente è stato archiviato e il workflow è terminato.

---

## Istruzioni per l'Uso Manuale

Se desideri eseguire lo script manualmente:

1.  **Prepara l'ambiente** (solo la prima volta):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    # pip install -r requirements.txt # Se ci fossero dipendenze
    ```
2.  **Aggiungi un file di testo** con le tue domande e risposte nella cartella `_inbox/`. Il formato deve essere:
    ```