"""
Configurazione pytest per i test del Classwork 2.

Questo file definisce fixtures comuni utilizzate dai test.
"""

import pytest
import sqlite3
import os
from pathlib import Path


@pytest.fixture
def test_db_path(tmp_path):
    """Crea un percorso per un database temporaneo di test.
    
    Yields
    ------
    Path
        Percorso al file database temporaneo che verrà automaticamente
        rimosso dopo ogni test.
    """
    db_path = tmp_path / "test_real_estate.db"
    yield str(db_path)
    # Cleanup automatico di tmp_path da pytest


@pytest.fixture
def empty_db(test_db_path):
    """Crea un database vuoto e pulito per ogni test.
    
    Yields
    ------
    str
        Percorso al database vuoto pronto per essere utilizzato
    """
    # Il database viene creato dal GestoreImmobiliare stesso
    yield test_db_path
