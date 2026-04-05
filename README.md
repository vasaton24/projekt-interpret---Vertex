# Projekt Vertex

Tohle je můj projekt vlastního programovacího jazyka. Jmenuje se Vertex. 
Chtěl jsem udělat něco, co vypadá jako moderní JavaScript nebo Python, ale je to jednodušší a přehlednější.

## Co je nového (Level 2)
- **Bezklíčová syntaxe**: Už nemusíte psát `var`. Stačí rovnou napsat `x = 10 ;`.
- **Aritmetika**: Vertex už umí počítat! Podporuje sčítání, odčítání, násobení i dělení.
- **Syntaktická kontrola**: Pokud uděláte chybu (např. dělení nulou nebo neexistující proměnná), program vám to slušně nahlásí v poli VÝSTUP.
- **Profi vzhled**: IDE má nyní tmavý režim (Dark Mode) a používá programátorské písmo Consolas.

## Jak to funguje
1. **Editor**: Horní šedé pole slouží pro psaní kódu.
2. **RUN**: Tlačítko (nebo klávesa **F5**) spustí váš program.
3. **Výstup**: Spodní černé pole ukazuje výsledky příkazů `print` nebo chyby v kódu.

## Příklad kódu
moje_cislo = 10 ;
dalsi_cislo = 20 ;
vysledek = moje_cislo + dalsi_cislo * 2 ;
print vysledek ;

## Instalace a spuštění

Tento projekt používá standard `pyproject.toml`, takže ho lze snadno nainstalovat do systému.

### Instalace
Otevřete terminál v hlavní složce projektu a spusťte:
```bash
pip install .
