# Projekt Vertex

Vertex IDE Pro — jednoduché desktopové IDE s interpretem vlastního jazyka Vertex.

Krátký popis
------------
Vertex je lehký experimentální programovací jazyk a interpret s jednoduchou syntaxí, určený pro učení a rychlé prototypování. Aplikace obsahuje textový editor, panel výstupu a nastavení (téma, velikost písma), která se ukládají do `config.json`.

Hlavní vlastnosti
------------------
- Editor s podporou uložení a načtení kódu (`.vtx`).
- Spouštění kódu v integrovaném interpreteru (klávesa `F5`).
- Nastavení tématu (tmavé/světlé) a velikosti písma, které se ukládají na disk.
- Reset prostředí i reset nastavení na výchozí hodnoty.

Požadavky
---------
- Python 3.8+ (doporučeno 3.10+)
- Tkinter (součást běžné instalace Pythonu)

Spuštění
--------
Ze složky projektu spusťte:

```bash
python -m src.main
```

Pokud chcete nainstalovat balíček lokálně (volitelné):

```bash
pip install .
```

Konfigurace a ukládání
----------------------
- Aplikace ukládá nastavení do `config.json` v kořenové složce projektu (odkud spouštíte aplikaci).
- V dialogu `Nastavení` můžete změnit téma a velikost písma. Po potvrzení se nastavení okamžitě použije a uloží na disk — zobrazí se informační dialog.
- Po uložení kódu pomocí `Uložit kód jako...` se zobrazí potvrzení o úspěšném uložení.

Krátké ovládání
---------------
- `F5` — spustit kód
- `Ctrl+S` — Uložit kód jako

Struktura projektu
------------------
- `src/main.py` — vstupní bod aplikace
- `src/vertex/gui.py` — grafické rozhraní (Tkinter)
- `src/vertex/lexer.py` — lexer (tokenizér)
- `src/vertex/parser.py` — parser a AST
- `src/vertex/interpreter.py` — vykonavatel AST
- `src/vertex/exceptions.py` — vlastní výjimky

Přispívání
----------
Rád přijmu PR nebo issue. Pro jednoduché příspěvky stačí upravit kód a poslat pull request. Pokud chcete, přidejte i jednoduché testy pro novou funkcionalitu.

Licence
-------
Projekt momentálně nemá explicitně přidanou licenci. Pokud chcete projekt otevřít pro jiné, přidejte prosím soubor `LICENSE` s požadovanou licencí.


Datum aktualizace: 2026-06-01
