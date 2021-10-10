from behave import *
from Principal import *

@given ('un archivo')
def step_imp(context):
    context.archivo = 'Prueba_Saber_11_2019-2.csv'


@when ('recibe el archivo')
def step_imp(context):
    context.file = Abrir_archivo(context.archivo)


@then ('abre el archivo')
def step_imp(context):
    assert verificar(context.file)
