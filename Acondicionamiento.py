import arcpy
from Generales import settings, funcionesGenerales


arcpy.env.overwriteOutput = True


conn = settings.conectionDB_pymmsql()
conexionDB = settings.conectionDB_arcpy()

# Recopilación de Ubigeos
def ubigeosNacional(conn=conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT UBIGEO FROM VW_SEGM_R_INSUMOS WHERE TB_AER = 1 AND TB_CCPP = 1 AND TB_VIVIENDA_R = 1 AND TB_CPV0301_VIVIENDA_R = 1")
    ubigeos = [x[0] for x in cursor]
    for x in ['160104', '110205', '120704', '130501']:
        ubigeos.remove(x)
    cursor.close()
    return ubigeos


def ubigeosCcpp(conn=conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT UBIGEO FROM TB_CCPP WHERE VIV_CCPP IS NULL AND AREA = 2")
    ubigeos = [x[0] for x in cursor]
    cursor.close()
    return ubigeos


def ubigeosCcppAer(conn=conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT UBIGEO FROM TB_CCPP WHERE (AER_INI IS NULL) AND (AREA = 2)")
    ubigeos = [x[0] for x in cursor]
    cursor.close()
    return ubigeos


def ubigeosDisponibles(ubigeosnacional, ubigeosccpp):
    ubigeosFinales = list(set(ubigeosccpp)&set(ubigeosnacional))
    return ubigeosFinales


# Funciones
def actualizaCpppVacios(ubigeos, conn=conn):
    for ubigeo in ubigeos:
        cursor = conn.cursor()
        cursor.execute("UPDATE TB_CCPP SET VIV_CCPP = 0 WHERE (VIV_CCPP IS NULL) AND AREA = 2".format(ubigeo))
        conn.commit()
        cursor.close()

def actualizarViviendasCcpp(ubigeos, conn=conn):
    n = 0
    for ubigeo in ubigeos:
        n = n + 1
        print n, ubigeo
        cursor = conn.cursor()
        cursor.execute("EXEC USP_ACTUALIZA_VIV_CCPP_R '{}'".format(ubigeo))
        conn.commit()
        cursor.close()


# ASIGNAR VIVIENDAS POR CADA CENTRO POBLADO

def asignarCantidadViviendas(tipo, ubigeos_input):
    if tipo == 1 and len(ubigeos_input) > 0:
        ubigeosnacional = ubigeos_input
        ubigeosccpp = ubigeos_input
    else:
        ubigeosnacional = ubigeosNacional()
        ubigeosccpp = ubigeosCcpp()
    ubigeos = ubigeosDisponibles(ubigeosnacional, ubigeosccpp)
    print ubigeos
    actualizarViviendasCcpp(ubigeos)


# ASIGNAR VALOR 0 A CENTROS POBLADOS SIN VIVIENDAS

def asignarCcppVacios(tipo, ubigeos_input):
    if tipo == 1 and len(ubigeos_input) > 0:
        ubigeosnacional = ubigeos_input
        ubigeosccpp = ubigeos_input
    else:
        ubigeosnacional = ubigeosNacional()
        ubigeosccpp = ubigeosCcpp()
    ubigeos = ubigeosDisponibles(ubigeosnacional, ubigeosccpp)
    actualizaCpppVacios(ubigeos)


def asignarAer(ubigeos, conexion=conexionDB, conn=conn):

    aers = r'{}\CPV_SEGMENTACION.dbo.TB_AER'.format(conexion)

    for ubigeo in ubigeos:
        print ubigeo
        ccppsmfl = arcpy.MakeQueryLayer_management(conexion, 'CCPP', "SELECT*FROM TB_CCPP WHERE UBIGEO = '{}' AND AREA = 2".format(ubigeo), 'LLAVE_CCPP', 'POINT', '4326', arcpy.SpatialReference(4326))
        ccpps_copy = arcpy.CopyFeatures_management(ccppsmfl, "in_memory\ccpps")
        ccpps = arcpy.MakeFeatureLayer_management(ccpps_copy, "ccpp")
        for aer in arcpy.da.SearchCursor(aers, ["SHAPE@", "AER_INI", "AER_FIN"], "UBIGEO = '{}'".format(ubigeo)):
            idaer = '{}{}{}'.format(ubigeo, aer[1], aer[2])
            seleccion = arcpy.SelectLayerByLocation_management(ccpps,"INTERSECT", aer[0], "#", "NEW_SELECTION", "NOT_INVERT")
            listaCcpps = [x[0] for x in arcpy.da.SearchCursor(seleccion, ["LLAVE_CCPP"])]
            if len(listaCcpps) > 0:
                expresion = funcionesGenerales.Expresion(listaCcpps, "#", "LLAVE_CCPP")
                cursor = conn.cursor()
                cursor.execute("UPDATE TB_CCPP SET AER_INI = '{}', AER_FIN = '{}', IDAER = '{}' WHERE {}".format(aer[1], aer[2], idaer, expresion))
                conn.commit()
                cursor.close()
            else:
                pass


# ASIGNAR AERS A LOS CENTROS POBLADOS

def asignarCCPPAER(tipo, ubigeos_input):
    if tipo == 1 and len(ubigeos_input) > 0:
        ubigeosnacional = ubigeos_input
        ubigeosccppaer = ubigeos_input
        print ubigeosnacional
        print ubigeosccppaer
    else:
        ubigeosnacional = ubigeosNacional()
        ubigeosccppaer = ubigeosCcppAer()
        print ubigeosnacional
        print ubigeosccppaer
    ubigeos = ubigeosDisponibles(ubigeosnacional, ubigeosccppaer)
    print ubigeos
    asignarAer(ubigeos)

def procesarInformacionPreSegmentacion(tipo, ubigeos_input):
    asignarCantidadViviendas(tipo, ubigeos_input)
    asignarCcppVacios(tipo, ubigeos_input)
    asignarCCPPAER(tipo, ubigeos_input)

# preparacionInformacion.procesarInformacionPreSegmentacion(1, ubigeos)
#
# acondicionamiento([])