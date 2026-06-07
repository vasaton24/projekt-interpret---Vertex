# Projekt Vertex

Vertex IDE Pro je jednoduché desktopové IDE s interpretem vlastního jazyka Vertex. Projekt je určený pro experimentální výuku, rychlé prototypování a testování malých programů.

Popis projektu
--------------
Aplikace obsahuje textový editor, panel výstupu a základní nastavení, které se ukládá do souboru `config.json`. Podporuje tmavé i světlé téma, dynamické zvýraznění chyb, export výstupu a uložení/nahrání `.vtx` souborů.

Hlavní funkce
--------------
- Editor s uložením a načtením kódu (`.vtx`).
- Spuštění kódu integrovaným interpreterem pomocí klávesy `F5`.
- Zobrazení chyb syntaxe a zvýraznění příslušného řádku v editoru.
- Export textového výstupu do souboru `.txt`.
- Nastavení tématu (tmavé/světlé) a velikosti písma.
- Hlavní obrazovka / úvodní stránka bez horního menu.
- Ukládání a načítání výchozí konfigurace aplikace.

Požadavky
---------
- Python 3.8+ (doporučeno 3.10+)
- Tkinter (součást většiny instalací Pythonu)

Spuštění
--------
Ze složky projektu spusťte:

```bash
python -m src.main
```

Pokud preferujete instalaci jako balíček, můžete použít:

```bash
pip install .
```

Poznámka: Aplikace očekává, že soubor `config.json` bude čitelný a zapisovatelný v kořenové složce projektu.

Nastavení a ukládání
--------------------
- Konfigurace se ukládá do `config.json`.
- Dialog `Nastavení` umožňuje změnit téma a velikost písma.
- Změny se po potvrzení ihned projeví v editoru a výstupu.
- Výstup lze exportovat jako textový soubor pomocí položky `Exportovat výstup...`.

Rychlé ovládání
---------------
- `F5` — spustit kód
- `Ctrl+S` — uložit kód jako

Struktura projektu
------------------
- `src/main.py` — hlavní vstupní bod aplikace
- `src/vertex/gui.py` — grafické rozhraní v Tkinteru
- `src/vertex/lexer.py` — lexer, který převádí text na tokeny
- `src/vertex/parser.py` — parser a AST uzly
- `src/vertex/interpreter.py` — vykonavatel AST
- `src/vertex/exceptions.py` — vlastní chybové výjimky
- `src/config.json` — ukládání nastavení aplikace (pokud existuje)

Licence
-------
Projekt aktuálně nemá definovanou licenci. Pokud chcete repozitář zpřístupnit veřejně, doporučuji přidat soubor `LICENSE` s vybranou licencí.

Datum aktualizace: 2026-06-07
