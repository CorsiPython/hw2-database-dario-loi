"""
Test pubblici per il Classwork 2: Gestore Immobiliare con OOP e Database

Questi test verificano le funzionalità base del GestoreImmobiliare.
Gli studenti devono implementare il codice in modo che tutti i test passino.
"""

import pytest
import sqlite3
from immobiliare_manager import (
    Agenzia,
    Agente,
    Proprieta,
    GestoreImmobiliare,
)


def test_import_and_dataclasses():
    """Verifica che le dataclasses siano importabili e abbiano gli attributi corretti."""
    agenzia = Agenzia(id_agenzia=1, nome="Immobiliare Roma", indirizzo="Via Roma 1")
    assert agenzia.id_agenzia == 1
    assert agenzia.nome == "Immobiliare Roma"
    assert agenzia.indirizzo == "Via Roma 1"
    
    agente = Agente(id_agente=101, nome="Mario Rossi", email="mario@example.com", id_agenzia=1)
    assert agente.id_agente == 101
    assert agente.nome == "Mario Rossi"
    assert agente.email == "mario@example.com"
    assert agente.id_agenzia == 1
    
    proprieta = Proprieta(
        id_proprieta=1001,
        indirizzo="Via Garibaldi 10",
        prezzo=250000.0,
        stato="In vendita",
        id_agente=101
    )
    assert proprieta.id_proprieta == 1001
    assert proprieta.indirizzo == "Via Garibaldi 10"
    assert proprieta.prezzo == 250000.0
    assert proprieta.stato == "In vendita"
    assert proprieta.id_agente == 101


def test_gestore_inizializzazione(empty_db):
    """Verifica che il GestoreImmobiliare crei le tabelle correttamente."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Verifica che il database esista
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    
    # Verifica che le tabelle esistano
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    
    assert "agenzie" in tables, "La tabella 'agenzie' non esiste"
    assert "agenti" in tables, "La tabella 'agenti' non esiste"
    assert "proprieta" in tables, "La tabella 'proprieta' non esiste"
    
    conn.close()
    gestore.close()


def test_gestore_schema_agenzie(empty_db):
    """Verifica che la tabella agenzie abbia lo schema corretto."""
    gestore = GestoreImmobiliare(empty_db)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    
    # Verifica le colonne della tabella agenzie
    cursor.execute("PRAGMA table_info(agenzie)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}  # name: type
    
    assert "id_agenzia" in columns, "Colonna id_agenzia mancante"
    assert "nome" in columns, "Colonna nome mancante"
    assert "indirizzo" in columns, "Colonna indirizzo mancante"
    
    conn.close()
    gestore.close()


def test_gestore_schema_agenti(empty_db):
    """Verifica che la tabella agenti abbia lo schema corretto con chiave esterna."""
    gestore = GestoreImmobiliare(empty_db)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    
    # Verifica le colonne della tabella agenti
    cursor.execute("PRAGMA table_info(agenti)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    assert "id_agente" in columns, "Colonna id_agente mancante"
    assert "nome" in columns, "Colonna nome mancante"
    assert "email" in columns, "Colonna email mancante"
    assert "id_agenzia" in columns, "Colonna id_agenzia (FK) mancante"
    
    # Verifica la chiave esterna
    cursor.execute("PRAGMA foreign_key_list(agenti)")
    fks = cursor.fetchall()
    assert len(fks) > 0, "Nessuna chiave esterna definita per agenti"
    
    conn.close()
    gestore.close()


def test_gestore_schema_proprieta(empty_db):
    """Verifica che la tabella proprieta abbia lo schema corretto con chiave esterna."""
    gestore = GestoreImmobiliare(empty_db)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    
    # Verifica le colonne della tabella proprieta
    cursor.execute("PRAGMA table_info(proprieta)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    assert "id_proprieta" in columns, "Colonna id_proprieta mancante"
    assert "indirizzo" in columns, "Colonna indirizzo mancante"
    assert "prezzo" in columns, "Colonna prezzo mancante"
    assert "stato" in columns, "Colonna stato mancante"
    assert "id_agente" in columns, "Colonna id_agente (FK) mancante"
    
    # Verifica la chiave esterna
    cursor.execute("PRAGMA foreign_key_list(proprieta)")
    fks = cursor.fetchall()
    assert len(fks) > 0, "Nessuna chiave esterna definita per proprieta"
    
    conn.close()
    gestore.close()


def test_add_agenzia_singola(empty_db):
    """Verifica l'inserimento di una singola agenzia."""
    gestore = GestoreImmobiliare(empty_db)
    
    agenzia = Agenzia(id_agenzia=1, nome="Immobiliare Roma", indirizzo="Via Roma 1")
    gestore.add_agenzia(agenzia)
    
    # Verifica nel database
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agenzie WHERE id_agenzia = 1")
    row = cursor.fetchone()
    
    assert row is not None, "L'agenzia non è stata inserita"
    assert row[0] == 1  # id_agenzia
    assert row[1] == "Immobiliare Roma"  # nome
    assert row[2] == "Via Roma 1"  # indirizzo
    
    conn.close()
    gestore.close()


def test_add_multiple_agenzie(empty_db):
    """Verifica l'inserimento di più agenzie."""
    gestore = GestoreImmobiliare(empty_db)
    
    agenzie = [
        Agenzia(1, "Immobiliare Roma", "Via Roma 1"),
        Agenzia(2, "Casa & Appartamenti", "Piazza Milano 5"),
        Agenzia(3, "Ville di Lusso", "Corso Napoli 100"),
    ]
    
    for agenzia in agenzie:
        gestore.add_agenzia(agenzia)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM agenzie")
    count = cursor.fetchone()[0]
    
    assert count == 3, f"Dovrebbero esserci 3 agenzie, trovate {count}"
    
    conn.close()
    gestore.close()


def test_add_agente_singolo(empty_db):
    """Verifica l'inserimento di un singolo agente."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Prima aggiungi un'agenzia
    agenzia = Agenzia(1, "Immobiliare Roma", "Via Roma 1")
    gestore.add_agenzia(agenzia)
    
    # Poi aggiungi un agente
    agente = Agente(101, "Mario Rossi", "mario@example.com", 1)
    gestore.add_agente(agente)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agenti WHERE id_agente = 101")
    row = cursor.fetchone()
    
    assert row is not None, "L'agente non è stato inserito"
    assert row[0] == 101  # id_agente
    assert row[1] == "Mario Rossi"  # nome
    assert row[2] == "mario@example.com"  # email
    assert row[3] == 1  # id_agenzia
    
    conn.close()
    gestore.close()


def test_add_proprieta_singola(empty_db):
    """Verifica l'inserimento di una singola proprietà."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup: agenzia e agente
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    
    # Aggiungi proprietà
    proprieta = Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101)
    gestore.add_proprieta(proprieta)
    
    conn = sqlite3.connect(empty_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proprieta WHERE id_proprieta = 1001")
    row = cursor.fetchone()
    
    assert row is not None, "La proprietà non è stata inserita"
    assert row[0] == 1001  # id_proprieta
    assert row[1] == "Via Garibaldi 10"  # indirizzo
    assert abs(row[2] - 250000.0) < 0.01  # prezzo (float comparison)
    assert row[3] == "In vendita"  # stato
    assert row[4] == 101  # id_agente
    
    conn.close()
    gestore.close()


def test_get_proprieta_per_agente_vuoto(empty_db):
    """Verifica che un agente senza proprietà restituisca lista vuota."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    
    proprieta = gestore.get_proprieta_per_agente(101)
    assert isinstance(proprieta, list), "Deve restituire una lista"
    assert len(proprieta) == 0, "La lista deve essere vuota"
    
    gestore.close()


def test_get_proprieta_per_agente_singola(empty_db):
    """Verifica il recupero di una proprietà per un agente."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    
    proprieta = gestore.get_proprieta_per_agente(101)
    
    assert len(proprieta) == 1, f"Dovrebbe esserci 1 proprietà, trovate {len(proprieta)}"
    assert isinstance(proprieta[0], Proprieta), "Deve restituire oggetti Proprieta"
    assert proprieta[0].id_proprieta == 1001
    assert proprieta[0].indirizzo == "Via Garibaldi 10"
    assert abs(proprieta[0].prezzo - 250000.0) < 0.01
    assert proprieta[0].stato == "In vendita"
    assert proprieta[0].id_agente == 101
    
    gestore.close()


def test_get_proprieta_per_agente_multiple(empty_db):
    """Verifica il recupero di più proprietà per un agente."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    
    # Aggiungi 3 proprietà per lo stesso agente
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Piazza Duomo 5", 180000.0, "In affitto", 101))
    gestore.add_proprieta(Proprieta(1003, "Corso Italia 22", 320000.0, "In vendita", 101))
    
    proprieta = gestore.get_proprieta_per_agente(101)
    
    assert len(proprieta) == 3, f"Dovrebbero esserci 3 proprietà, trovate {len(proprieta)}"
    ids = {p.id_proprieta for p in proprieta}
    assert ids == {1001, 1002, 1003}, "IDs delle proprietà non corrispondono"
    
    gestore.close()


def test_get_agenti_per_agenzia_vuoto(empty_db):
    """Verifica che un'agenzia senza agenti restituisca lista vuota."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    
    agenti = gestore.get_agenti_per_agenzia(1)
    assert isinstance(agenti, list), "Deve restituire una lista"
    assert len(agenti) == 0, "La lista deve essere vuota"
    
    gestore.close()


def test_get_agenti_per_agenzia_singolo(empty_db):
    """Verifica il recupero di un agente per un'agenzia."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    
    agenti = gestore.get_agenti_per_agenzia(1)
    
    assert len(agenti) == 1, f"Dovrebbe esserci 1 agente, trovati {len(agenti)}"
    assert isinstance(agenti[0], Agente), "Deve restituire oggetti Agente"
    assert agenti[0].id_agente == 101
    assert agenti[0].nome == "Mario Rossi"
    assert agenti[0].email == "mario@example.com"
    assert agenti[0].id_agenzia == 1
    
    gestore.close()


def test_get_agenti_per_agenzia_multiple(empty_db):
    """Verifica il recupero di più agenti per un'agenzia."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(102, "Laura Bianchi", "laura@example.com", 1))
    gestore.add_agente(Agente(103, "Giuseppe Verdi", "giuseppe@example.com", 1))
    
    agenti = gestore.get_agenti_per_agenzia(1)
    
    assert len(agenti) == 3, f"Dovrebbero esserci 3 agenti, trovati {len(agenti)}"
    ids = {a.id_agente for a in agenti}
    assert ids == {101, 102, 103}, "IDs degli agenti non corrispondono"
    
    gestore.close()


def test_get_proprieta_per_agenzia_con_join(empty_db):
    """Verifica il recupero di proprietà per agenzia tramite JOIN."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup: 1 agenzia, 2 agenti, 3 proprietà
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(102, "Laura Bianchi", "laura@example.com", 1))
    
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Piazza Duomo 5", 180000.0, "In affitto", 101))
    gestore.add_proprieta(Proprieta(1003, "Corso Italia 22", 320000.0, "In vendita", 102))
    
    proprieta = gestore.get_proprieta_per_agenzia(1)
    
    assert len(proprieta) == 3, f"Dovrebbero esserci 3 proprietà, trovate {len(proprieta)}"
    ids = {p.id_proprieta for p in proprieta}
    assert ids == {1001, 1002, 1003}, "IDs delle proprietà non corrispondono"
    
    gestore.close()


def test_get_proprieta_per_agenzia_filtra_altre_agenzie(empty_db):
    """Verifica che vengano restituite solo le proprietà dell'agenzia specificata."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup: 2 agenzie con agenti e proprietà diverse
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agenzia(Agenzia(2, "Casa & Appartamenti", "Piazza Milano 5"))
    
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(201, "Laura Bianchi", "laura@example.com", 2))
    
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Piazza Duomo 5", 180000.0, "In affitto", 101))
    gestore.add_proprieta(Proprieta(2001, "Corso Italia 22", 320000.0, "In vendita", 201))
    
    proprieta_ag1 = gestore.get_proprieta_per_agenzia(1)
    proprieta_ag2 = gestore.get_proprieta_per_agenzia(2)
    
    assert len(proprieta_ag1) == 2, f"Agenzia 1 dovrebbe avere 2 proprietà, trovate {len(proprieta_ag1)}"
    assert len(proprieta_ag2) == 1, f"Agenzia 2 dovrebbe avere 1 proprietà, trovate {len(proprieta_ag2)}"
    
    ids_ag1 = {p.id_proprieta for p in proprieta_ag1}
    ids_ag2 = {p.id_proprieta for p in proprieta_ag2}
    
    assert ids_ag1 == {1001, 1002}, "Proprietà agenzia 1 non corrette"
    assert ids_ag2 == {2001}, "Proprietà agenzia 2 non corrette"
    
    gestore.close()


def test_aggiorna_stato_proprieta(empty_db):
    """Verifica l'aggiornamento dello stato di una proprietà."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    
    # Aggiorna stato
    gestore.aggiorna_stato_proprieta(1001, "Venduto")
    
    # Verifica
    proprieta = gestore.get_proprieta_per_agente(101)
    assert len(proprieta) == 1
    assert proprieta[0].stato == "Venduto", f"Stato dovrebbe essere 'Venduto', trovato '{proprieta[0].stato}'"
    
    gestore.close()


def test_aggiorna_stato_proprieta_inesistente(empty_db):
    """Verifica che aggiornare una proprietà inesistente non causi errori."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Non dovrebbe sollevare eccezioni
    gestore.aggiorna_stato_proprieta(9999, "Venduto")
    
    gestore.close()


def test_get_best_agente_per_agenzia_vuoto(empty_db):
    """Verifica che restituisca dizionario vuoto se non ci sono dati."""
    gestore = GestoreImmobiliare(empty_db)
    
    result = gestore.get_best_agente_per_agenzia()
    assert isinstance(result, dict), "Deve restituire un dizionario"
    assert len(result) == 0, "Deve restituire dizionario vuoto"
    
    gestore.close()


def test_get_best_agente_per_agenzia_singolo(empty_db):
    """Verifica il best agente con una sola agenzia."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup: 1 agenzia, 2 agenti, proprietà diverse
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(102, "Laura Bianchi", "laura@example.com", 1))
    
    # Mario ha 3 proprietà
    gestore.add_proprieta(Proprieta(1001, "Via A", 100000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Via B", 150000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1003, "Via C", 200000.0, "In vendita", 101))
    
    # Laura ha 1 proprietà
    gestore.add_proprieta(Proprieta(1004, "Via D", 120000.0, "In vendita", 102))
    
    result = gestore.get_best_agente_per_agenzia()
    
    assert 1 in result, "Agenzia 1 dovrebbe essere nel risultato"
    assert isinstance(result[1], Agente), "Il valore deve essere un oggetto Agente"
    assert result[1].id_agente == 101, f"Il best agente dovrebbe essere 101, trovato {result[1].id_agente}"
    
    gestore.close()


def test_get_best_agente_per_agenzia_multiple(empty_db):
    """Verifica il best agente con più agenzie."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup: 2 agenzie
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agenzia(Agenzia(2, "Casa & Appartamenti", "Piazza Milano 5"))
    
    # Agenzia 1: 2 agenti
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(102, "Laura Bianchi", "laura@example.com", 1))
    
    # Agenzia 2: 2 agenti
    gestore.add_agente(Agente(201, "Giuseppe Verdi", "giuseppe@example.com", 2))
    gestore.add_agente(Agente(202, "Anna Neri", "anna@example.com", 2))
    
    # Proprietà agenzia 1: Mario 2, Laura 1
    gestore.add_proprieta(Proprieta(1001, "Via A", 100000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Via B", 150000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1003, "Via C", 200000.0, "In vendita", 102))
    
    # Proprietà agenzia 2: Giuseppe 3, Anna 1
    gestore.add_proprieta(Proprieta(2001, "Via D", 120000.0, "In vendita", 201))
    gestore.add_proprieta(Proprieta(2002, "Via E", 130000.0, "In vendita", 201))
    gestore.add_proprieta(Proprieta(2003, "Via F", 140000.0, "In vendita", 201))
    gestore.add_proprieta(Proprieta(2004, "Via G", 110000.0, "In vendita", 202))
    
    result = gestore.get_best_agente_per_agenzia()
    
    assert 1 in result, "Agenzia 1 dovrebbe essere nel risultato"
    assert 2 in result, "Agenzia 2 dovrebbe essere nel risultato"
    
    assert result[1].id_agente == 101, f"Best agente agenzia 1 dovrebbe essere 101, trovato {result[1].id_agente}"
    assert result[2].id_agente == 201, f"Best agente agenzia 2 dovrebbe essere 201, trovato {result[2].id_agente}"
    
    gestore.close()


def test_get_best_agente_per_agenzia_pareggio(empty_db):
    """Verifica che in caso di pareggio restituisca uno degli agenti."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_agente(Agente(102, "Laura Bianchi", "laura@example.com", 1))
    
    # Entrambi hanno 2 proprietà
    gestore.add_proprieta(Proprieta(1001, "Via A", 100000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Via B", 150000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1003, "Via C", 200000.0, "In vendita", 102))
    gestore.add_proprieta(Proprieta(1004, "Via D", 120000.0, "In vendita", 102))
    
    result = gestore.get_best_agente_per_agenzia()
    
    assert 1 in result, "Agenzia 1 dovrebbe essere nel risultato"
    assert result[1].id_agente in [101, 102], "Deve restituire uno dei due agenti in pareggio"
    
    gestore.close()


def test_integrità_referenziale_verifica_esistenza(empty_db):
    """Test che verifica l'integrità referenziale (scenario completo)."""
    gestore = GestoreImmobiliare(empty_db)
    
    # Setup completo
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_proprieta(Proprieta(1001, "Via Garibaldi 10", 250000.0, "In vendita", 101))
    
    # Verifica che tutto sia collegato correttamente
    agenti = gestore.get_agenti_per_agenzia(1)
    assert len(agenti) == 1
    assert agenti[0].id_agente == 101
    
    proprieta = gestore.get_proprieta_per_agente(101)
    assert len(proprieta) == 1
    assert proprieta[0].id_proprieta == 1001
    
    proprieta_agenzia = gestore.get_proprieta_per_agenzia(1)
    assert len(proprieta_agenzia) == 1
    assert proprieta_agenzia[0].id_proprieta == 1001
    
    gestore.close()


def test_stati_proprietà_diversi(empty_db):
    """Verifica che si possano gestire proprietà con stati diversi."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    
    # Aggiungi proprietà con stati diversi
    gestore.add_proprieta(Proprieta(1001, "Via A", 100000.0, "In vendita", 101))
    gestore.add_proprieta(Proprieta(1002, "Via B", 150000.0, "Venduto", 101))
    gestore.add_proprieta(Proprieta(1003, "Via C", 200000.0, "In affitto", 101))
    
    proprieta = gestore.get_proprieta_per_agente(101)
    stati = {p.stato for p in proprieta}
    
    assert stati == {"In vendita", "Venduto", "In affitto"}, "Gli stati non sono stati salvati correttamente"
    
    gestore.close()


def test_prezzi_float_precisi(empty_db):
    """Verifica che i prezzi float siano gestiti correttamente."""
    gestore = GestoreImmobiliare(empty_db)
    
    gestore.add_agenzia(Agenzia(1, "Immobiliare Roma", "Via Roma 1"))
    gestore.add_agente(Agente(101, "Mario Rossi", "mario@example.com", 1))
    gestore.add_proprieta(Proprieta(1001, "Via A", 123456.78, "In vendita", 101))
    
    proprieta = gestore.get_proprieta_per_agente(101)
    
    assert len(proprieta) == 1
    assert abs(proprieta[0].prezzo - 123456.78) < 0.01, "Il prezzo non è stato salvato con precisione"
    
    gestore.close()
