from Principal import *

def test_abrir_archivo():
    file = Abrir_archivo("Prueba_Saber_11_2019-2.csv")
    assert verificar(file)
