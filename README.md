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

Syntaxe jazyka Vertex
--------------------
- Každý příkaz musí končit středníkem `;`.
- Přiřazení proměnné: `x = 10 ;`
- Výpis hodnoty: `print x ;`
- Řetězce se zapisují v uvozovkách: `print "Ahoj svět" ;`
- Podporované operátory: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`.
- Podmínky a smyčky mají zápis jako v C:
  - `if (x < 10) { print x ; }`
  - `while (x < 5) { x = x + 1 ; print x ; }`
  - `for (i = 0; i < 3; i = i + 1) { print i ; }`
- Komentáře lze psát jako `// jednorádkový komentář`, `# také jednorádkový komentář` nebo blok `/* víceřádkový komentář */`.

Příklad
-------
```text
x = 10 ;
y = 20 ;
print "Součet je:" ;
print x + y ;

for (i = 0; i < 3; i = i + 1) {
    print i ;
}
```

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
Tento projekt je licencován pod MIT licencí. Podrobnosti jsou v souboru `LICENSE`.
=======

Datum aktualizace: 2026-06-07
