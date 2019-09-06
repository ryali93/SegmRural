import arcpy
import pythonaddins

class CargarResultados(object):
    """Implementation for addins_addin.boton6 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'CargarInfo')

class Crearcaparutas(object):
    """Implementation for addins_addin.boton2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'CrearFcRutas')

class GenerarResultados(object):
    """Implementation for addins_addin.boton5 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'GenerarTablasFinales')

class GenerarSecciones(object):
    """Implementation for addins_addin.boton4 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'CrearcapadeSecciones')

class ImportarInformacion(object):
    """Implementation for addins_addin.boton1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'ImportInfo')

class OrdenCentrosPoblados(object):
    """Implementation for addins_addin.boton3 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(r'\\192.168.201.115\cpv2017\SegmentacionRural_Procesamiento\TBX\ToolbarSegmRural.tbx', 'CrearFcCcpps')