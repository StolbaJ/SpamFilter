# Filtrace textu podle seznamu tokenů

Tento projekt implementuje jednoduchou filtraci textového korpusu na základě zadaného seznamu tokenů.
Projekt je součástí semestrální práce z předmĞtu na zpracování přirozeného jazyka.

## Struktura projektu

* `corpus.py` — Načítá textový korpus z daného souboru, předzpracovává ho a rozděluje na tokeny.
* `filter.py` — Obsahuje hlavní logiku pro filtrování tokenů podle zadaného whitelistu nebo blacklistu.
* `utils.py` — Obsahuje pomocné funkce pro čtení a zápis souborů, logování a kontrolu typů.
* `options.txt` — Textový soubor obsahující konfigurační parametry (např. vstupní soubory, typ filtrace, seznam tokenů).

## Požadavky

* Python 3.6+
* žádné externí knihovny nejsou potřeba (pouze standardní knihovna).

## Použití

1. Upravte `options.txt` dle potřeby:

```
input_file=./data/input.txt
output_file=./data/output.txt
mode=whitelist
filter_file=./data/whitelist.txt
```

2. Spusťte skript `filter.py`:

```bash
python3 filter.py
```

Skript načte vstupní soubor, aplikuje zvolenou filtraci a zapíše výsledky do zadaného výstupního souboru.

## Podporované režimy filtrace

* **Whitelist**: ponechá pouze tokeny, které se nacházejí ve `filter_file`.
* **Blacklist**: odstraní tokeny, které se nacházejí ve `filter_file`.
