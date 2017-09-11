#!/usr/bin/python
# -*- coding: utf-8 -*-

import arcpy
import os
from AppPresegmentacion import preparacionInformacion
from AppModuloRural import ActualizarModuloSegmRural, InsertarData
from AppCroquis import CroquisEmpadronador, CroquisSeccion
from AppSegmentacion import Segmentacion_2, polThiessen
from AppListados import Listado001, Listado002, Listado003, Listado004, Listado005, Listado006
from AppMerge import MergePDF
from AppConsistencia import vivConsistencia, ccppConsistencia
from Generales import settings, funcionesGenerales
from datetime import datetime
from AppCalidad import actualizarCalidad
from ProgramacionRutas import ExtraeTabla, ProgramacionRutasResumen
import sys


startTime = datetime.now()
print startTime

ubigeo_procesar = '{}'.format(sys.argv[1])

arcpy.env.overwriteOutput = True

# DECLARANDO VARIABLES

# CONEXIONES

conexionDB = settings.conectionDB_arcpy()
conexionGDB = settings.conectionGDB_arcpy()
conn2 = settings.conectionDB_pymmsql()

nombreconexionDB = (os.path.basename(conexionDB)).split(".")[0]
nombreconexionGDB = (os.path.basename(conexionGDB)).split(".")[0]

nombreBD = "CPV_SEGMENTACION"


# ESPACIOS DE TRABAJPOS PARA DISTINTAS FUNCIONES
WorkSpaceSegmentacion = r'D:\SegmentacionRuralV2\Procesamiento\Segmentacion'
WorkSpaceCroquis = r'D:\SegmentacionRuralV2\Procesamiento\Croquis'
WorkSpaceListado = r'D:\SegmentacionRuralV2\Procesamiento\Listados'
WorkSpaceProgRutas = r'D:\SegmentacionRuralV2\Procesamiento\ProgRutas'


FILESERVER_CROQUIS = r'\\192.168.201.115\cpv2017\croquis-listado'


# SELECCIONAR EL TIPO DE SEGMENTACION |||||| CENSO : 1 |||||| FEN : 2

tipo = 1


# TABLAS UTILIZADAS
VW_DISTRITO = r'{}\{}.dbo.VW_DISTRITO'.format(conexionDB, nombreconexionDB) #
SEGM_R_RUTA = r'{}\{}.dbo.SEGM_R_RUTA'.format(conexionDB, nombreconexionDB) #
SEGM_R_CCPPRUTA = r'{}\{}.dbo.SEGM_R_CCPPRUTA'.format(conexionDB, nombreconexionDB) #
VW_SEGM_R_AER_VIV = r'{}\{}.dbo.VW_SEGM_R_AER_VIV'.format(conexionDB, nombreconexionDB) #
SEGM_R_EMP = r'{}\{}.dbo.SEGM_R_EMP'.format(conexionDB, nombreconexionDB)   #
SEGM_R_SCR = r'{}\{}.dbo.SEGM_R_SCR'.format(conexionDB, nombreconexionDB)   #
SEGM_R_AER_POST = r'{}\{}.dbo.SEGM_R_AER_POST'.format(conexionDB, nombreconexionDB) #
CCPP_INDIGENAS_U = r'{}\{}.dbo.CCPP_INDIGENAS'.format(conexionDB, nombreconexionDB) #


# TABLAS DE GDB  ---->  MODIFICAR LOS NOMBRES
SEGM_R_AER = r'{}\{}.SDE.SEGM_R_AER_TMP'.format(conexionGDB, nombreconexionGDB)
SEGM_R_CCPP = r'{}\{}.SDE.SEGM_R_CCPP_TMP'.format(conexionGDB, nombreconexionGDB)
SEGM_R_VIV = r'{}\{}.SDE.SEGM_R_VIV_TMP'.format(conexionGDB, nombreconexionGDB)
CALIDAD_CCPP_PRESEGM = r'Database Connections\CPV_SEGMENTACION_GDB.sde\CPV_SEGMENTACION_GDB.SDE.CALIDAD_RURAL\CPV_SEGMENTACION_GDB.SDE.CALIDAD_CCPP_PRESEGM'
CALIDAD_VIV_PRESEGM = r'Database Connections\CPV_SEGMENTACION_GDB.sde\CPV_SEGMENTACION_GDB.SDE.CALIDAD_RURAL\CPV_SEGMENTACION_GDB.SDE.CALIDAD_VIV_PRESEGM'

# Back Up
# CALIDAD_CCPP_PRESEGM = r'Database Connections\GEODB_CPV_SEGM.sde\GEODB_CPV_SEGM.SDE.CALIDAD_RURAL\GEODB_CPV_SEGM.SDE.CALIDAD_CCPP_PRESEGM'
# CALIDAD_VIV_PRESEGM = r'Database Connections\GEODB_CPV_SEGM.sde\GEODB_CPV_SEGM.SDE.CALIDAD_RURAL\GEODB_CPV_SEGM.SDE.CALIDAD_VIV_PRESEGM'


# PROYECTOS MXD

if tipo == 1:
    mxd_croquis_emp = os.path.join(os.path.dirname(__file__), 'insumos', 'mxd', 'AERCroquisA3.mxd')
else:
    mxd_croquis_emp = os.path.join(os.path.dirname(__file__), 'insumos', 'mxd', 'AERCroquisA3_FEN.mxd')


mxd_croquis_scr = r'D:\SegmentacionRuralV2\Insumos\mxd\SeccionCroquisA3.mxd'


# SIMBOLOGIAS
TRACKS_LYR = r'D:\SegmentacionRuralV2\Insumos\layers\Tracks.lyr'
SCR_LYR = r'D:\SegmentacionRuralV2\Insumos\layers\SCR.lyr'

# IMAGENES LISTADOS

EscudoNacional = r'D:\SegmentacionRuralV2\Insumos\Img\ENP_BW.png'
LogoInei = r'D:\SegmentacionRuralV2\Insumos\Img\Inei_BW.png'



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::PRIMERA FASE:::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def acondicionamiento(ubigeos):
    preparacionInformacion.procesarInformacionPreSegmentacion(1, ubigeos)

def consistencia(ubigeos):
    vivConsistencia.consistenciaVIV(CALIDAD_VIV_PRESEGM, ubigeos)
    ccppConsistencia.consistenciaCCPP(CALIDAD_CCPP_PRESEGM, ubigeos)
    ccppConsistencia.generarTablaConsistencia(ubigeos)

def moduloSegmentacionRural(ubigeos):
    ActualizarModuloSegmRural.actualizar()

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::   SEGUNDA FASE  ::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def CargarInformacionRutas(ubigeos):
    InsertarData.insertarInformacion(ubigeos)

def segmentacionmain(ubigeos):
    #### PROCESAMIENTO DE INFORMACION
    fase = 'CPV2017'
    # UBIGEOS
    # sql = funcionesGenerales.Expresion(ubigeos, "#", 'UBIGEO')
    # Distritos_tmp = arcpy.MakeQueryLayer_management(conexionDB, 'DistritosTMP', "SELECT*FROM VW_DISTRITO where {}".format(sql), 'UBIGEO', 'POLYGON', '4326', arcpy.SpatialReference(4326))

    # SEGMENTACION
    print "SEGMENTACION"
    # arcpy.AddMessage("SEGMENTACION")
    # Segmentacion_2.SegmentacionRural(WorkSpaceSegmentacion, Distritos_tmp, conexionDB, conexionGDB, SEGM_R_AER, SEGM_R_CCPP, SEGM_R_VIV, SEGM_R_AER_POST)
    # #--------------------------#--------------------------#--------------------------#--------------------------#--------------------------
    # AL FINALIZAR LA GENERACIÓN DE TOD O
    print "POLIGONOS MONITOREO"
    for ubigeo in ubigeos:
        Segmentacion_2.ActualizarFlagSegmRural(ubigeo, conn2)
        # Segmentacion_2.actualizarAsignacion(ubigeo, conn2)
        Segmentacion_2.actualizarRegistrosRuralMonitoreo(conn2)
        polThiessen.crearThiessen(ubigeo, fase)
        print ubigeo
    # --------------------------#--------------------------#--------------------------#--------------------------#--------------------------

def calidad(ubigeo):
    print "CALIDAD"
    actualizarCalidad(ubigeo)

def productosSegmentacion(ubigeos):

    fase = 'CPV2017'
    # fase = 'III-EXPERIMENTAL'

    # CREACION DE DIRECTORIOS
    # funcionesGenerales.Crear_Carpetas_Croquis_AER(WorkSpaceProgRutas, ubigeos, tipo)
    # funcionesGenerales.Crear_Carpetas_Croquis_AER(WorkSpaceListado, ubigeos, tipo)
    # funcionesGenerales.Crear_Carpetas_Croquis_AER(WorkSpaceCroquis, ubigeos, tipo)
    # funcionesGenerales.Crear_Carpetas_FileServer(FILESERVER_CROQUIS, ubigeos, fase, tipo)
    # funcionesGenerales.Crear_Carpetas_Croquis_AER(FILESERVER_CROQUIS, ubigeos, tipo)


    # LISTADOS
    # print "LISTADOS"
    # arcpy.AddMessage("LISTADOS")
    # for x in ubigeos:
    #     print "Ubigeo: " + str(x)
    #     Listado001.Listado001ViviendasAer(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_RUTA, SEGM_R_CCPPRUTA, SEGM_R_AER, VW_SEGM_R_AER_VIV, EscudoNacional, LogoInei, tipo)
    #     Listado002.Listado002ccppAer(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_RUTA, SEGM_R_CCPPRUTA, SEGM_R_AER, EscudoNacional, LogoInei, tipo, SEGM_R_EMP)
    #     Listado003.Listado003ccppSeccion(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_RUTA, SEGM_R_CCPPRUTA, EscudoNacional, LogoInei)
    #     Listado004.Listado004Distrital(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_RUTA, SEGM_R_CCPPRUTA, SEGM_R_AER, EscudoNacional, LogoInei, tipo)
    #     Listado005.listado005ComunidadesIndigenas(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_CCPPRUTA, SEGM_R_EMP, SEGM_R_AER, EscudoNacional, LogoInei)
    #     Listado006.listado006ComunidadesIndigenasDistrital(x, WorkSpaceListado, VW_DISTRITO, SEGM_R_CCPPRUTA, CCPP_INDIGENAS_U, SEGM_R_EMP, SEGM_R_AER, EscudoNacional, LogoInei)
    #     ExtraeTabla.programacionRutas(x, WorkSpaceProgRutas)
        # ProgramacionRutasResumen.tablaResumen(x, WorkSpaceProgRutas)

    # CROQUIS
    print "CROQUIS DE EMPADRONADOR"
    arcpy.AddMessage("CROQUIS DE EMPADRONADOR")
    CroquisEmpadronador.CroquisEmpadronador(ubigeos, WorkSpaceCroquis, mxd_croquis_emp, tipo)
    # #
    # print "CROQUIS DE SECCION"
    # arcpy.AddMessage("CROQUIS DE SECCION")
    # CroquisSeccion.CroquisSeccion(ubigeos, WorkSpaceCroquis, SEGM_R_AER, SCR_LYR, mxd_croquis_scr)

    # MERGE
    print "MERGE DE PDFs"
    arcpy.AddMessage("MERGE DE PDFs")
    MergePDF.mergePDF(FILESERVER_CROQUIS, WorkSpaceListado, WorkSpaceCroquis, WorkSpaceProgRutas, ubigeos, fase, tipo)
    MergePDF.mergeFinal(FILESERVER_CROQUIS, ubigeos, fase)


def ubigeosProcesarValidacion(ubigeos, conn=conn2):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT UBIGEO FROM CPV_SEGMENTACION_GDB.sde.SEGM_R_RUTA WHERE IDSCR IS NOT NULL OR IDSCR <> '' OR IDRUTA IS NOT NULL OR IDRUTA <> ''")
    inforutas = [x[0] for x in cursor]
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT UBIGEO FROM CPV_SEGMENTACION_GDB.sde.SEGM_R_CCPPRUTA WHERE IDSCR IS NOT NULL OR IDSCR <> '' OR IDRUTA IS NOT NULL OR IDRUTA <> ''")
    infoccpps = [x[0] for x in cursor]
    cursor.close()
    cursor = conn.cursor()
    ubigeossinaer = "('{}')".format("','".join(ubigeos))
    cursor.execute("SELECT DISTINCT UBIGEO FROM CPV_SEGMENTACION_GDB.sde.TB_CCPP WHERE UBIGEO IN {} AND (AREA = 2) AND ((AER_INI IS NULL) OR (IDAER IS NULL) OR (IDAER = ''))".format(ubigeossinaer))
    infovacios = [x[0] for x in cursor]
    cursor.close()
    informacion = list((set(inforutas)&set(infoccpps)&set(ubigeos))-set(infovacios))
    print list(set(ubigeos) - (set(infoccpps)&set(inforutas)))
    print infovacios
    # informacion.remove('150711')
    return informacion

def main():

    # ETAPA 1
    # acondicionamiento([])
    # consistencia(['080608','080604','080502'])
    # moduloSegmentacionRural(['090723','040106', '040111', '040306', '040507', '040508', '040510', '040603', '040607', '040802', '040806', '040811', '050104', '050201', '050205', '050401', '050404', '050407', '050408', '050410', '050507', '050601', '050616', '051102', '051108', '090204', '090206', '090301', '090607', '090704', '090705', '190109', '190113', '190206', '190301', '190305', '190306', '190307', '190308', '210102', '210106', '210201', '210207', '210309', '210401', '210403', '210404', '210405', '210406', '210407', '210502', '210503', '210602', '210605', '210710', '210803', '210805', '210807', '211002', '211101', '211301', '211304'])
    # ETAPA 2
    # ubigeos_tmp = preparacionInformacion.leerExcel(tipo)

    ubigeos = [ubigeo_procesar]
    # print ubigeos_tmp
    # ubigeos = ubigeosProcesarValidacion(ubigeos_tmp)

    print ubigeos

    # CargarInformacionRutas(ubigeos)
    # segmentacionmain(ubigeos)
    productosSegmentacion(ubigeos)
    # segmentacionmain(ubigeos)
    # calidad(ubigeos)

if __name__ == '__main__':
    main()

print datetime.now() - startTime
print "FINALIZADO"