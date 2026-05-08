import ezdxf
from collections import Counter


def get_prawdziwa_nazwa(element, dokument):
    
    nazwa_robocza = element.dxf.name

    if not nazwa_robocza.startswith('*U'):
        return nazwa_robocza
    
    try:
        rekord_bloku = dokument.block_records.get(nazwa_robocza)
        ukryte_dane = rekord_bloku.get_xdata('AcDbBlockRepBTag')

        for tag in ukryte_dane:
            if tag[0] == 1005:
                uchwyt = tag[1]
                oryginalny_rekord = dokument.entitydb.get(uchwyt)
                return oryginalny_rekord.dxf.name
    except:
        pass

    return nazwa_robocza

def zlicz_bloki_w_dxf(sciezka_do_pliku):
    try:
        dokument = ezdxf.readfile(sciezka_do_pliku)
    except Exception as blad:
        print(f"blad z wczytaniem pliku; szczegoly: {blad}")
        return None

    przestrzen_modelu = dokument.modelspace()
    nazwy_znalezionych_blokow = []

    for element in przestrzen_modelu.query('INSERT'):
        
        prawdziwa_nazwa = get_prawdziwa_nazwa(element, dokument)
        nazwa_robocza = element.dxf.name
        
        wariant_z_atrybutu = None

        
        if element.attribs:
            for atrybut in element.attribs:
                if atrybut.dxf.tag == "OPIS_WARIANTU":
                    wariant_z_atrybutu = atrybut.dxf.text
                    break 

        
        if wariant_z_atrybutu:
            pelna_nazwa = f"{prawdziwa_nazwa}, wariant: {wariant_z_atrybutu}"
        else:
            if nazwa_robocza != prawdziwa_nazwa:
                pelna_nazwa = f"{prawdziwa_nazwa}, wariant: {nazwa_robocza}"
            else:
                pelna_nazwa = prawdziwa_nazwa
                
        nazwy_znalezionych_blokow.append(pelna_nazwa)

    podsumowanie = Counter(nazwy_znalezionych_blokow)
    return podsumowanie

plik = "rysunek.dxf"

print(f"start analizy pliku: {plik}...")
wyniki = zlicz_bloki_w_dxf(plik)

if wyniki:
    print("\nznalezione bloki i ich ilosc:")
    print("---------------------------------------")
    for nazwa, ilosc in wyniki.items():
        print(f"blok '{nazwa}' --- ilosc '{ilosc}'")
    print("---------------------------------")
    print("koniec, sukces")
