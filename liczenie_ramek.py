import ezdxf
import math
import pandas as pd
from collections import Counter

def oblicz_odleglosc(punkt1, punkt2):
    return math.hypot(punkt1.x - punkt2.x, punkt1.y - punkt2.y)

def zlicz_ramki_w_dxf(sciezka_do_pliku, nazwa_warstwy, max_odleglosc):
    try:
        dokument = ezdxf.readfile(sciezka_do_pliku)
    except Exception as blad:
        print(f"blad z wczytaniem pliku: {blad}")
        return None

    przestrzen_modelu = dokument.modelspace()

    punkty_blokow =[]
    for element in przestrzen_modelu.query('INSERT'):
        if element.dxf.layer == nazwa_warstwy:
            punkty_blokow.append(element.dxf.insert)
    if not punkty_blokow:
        print(f"nie ma blokow na warstwie: {nazwa_warstwy}")
        return Counter()
    
    odwiedzone = set()
    znalezione_ramki = []

    for i in range(len(punkty_blokow)):
        if i in odwiedzone:
            continue
        
        wielkosc_aktualnej_ramki = 0
        kolejka_do_sprawdzenia = [i]
        odwiedzone.add(i)

        while kolejka_do_sprawdzenia:
            aktualny_index = kolejka_do_sprawdzenia.pop(0)
            aktualny_punkt = punkty_blokow[aktualny_index]
            wielkosc_aktualnej_ramki += 1

            for j in range(len(punkty_blokow)):
                if j not in odwiedzone:
                    odleglosc = oblicz_odleglosc(aktualny_punkt, punkty_blokow[j])

                    if odleglosc <= max_odleglosc:
                        odwiedzone.add(j)
                        kolejka_do_sprawdzenia.append(j)

        znalezione_ramki.append(wielkosc_aktualnej_ramki)
    
    podsumowanie = Counter(znalezione_ramki)
    return podsumowanie


plik = "rysunek.dxf"
warstwa_elektryczna = "11_printing_sockets"

tolerancja_odleglosci = 16.4916

print(f"Start analizy ramek w {plik} ...")
wyniki = zlicz_ramki_w_dxf(plik, warstwa_elektryczna, tolerancja_odleglosci)

if wyniki:
    print(f"\nZestawienie potrzebnych ramek:")
    print("---------------------------------")

    for wielkosc, ilosc in sorted(wyniki.items()):
        if wielkosc == 1:
            typ = "pojedyncza"
        elif wielkosc == 2:
            typ = "podwójna"
        elif wielkosc == 3:
            typ = "potrójna"
        elif wielkosc == 4:
            typ = "poczwórna"
        elif wielkosc == 5:
            typ = "pięciokrotna"
        else:
            typ = f"{wielkosc}-krotna"
    
        print(f"ramka {typ} --- ilosc: {ilosc}")

    print("----------------------------------")
    print("koniec, sukces")
