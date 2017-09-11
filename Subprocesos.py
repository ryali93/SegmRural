import subprocess
import sys
from datetime import *
import os
import socket

# GENERAR CROQUIS Y MERGEAR
# lista_ubigeos = ['120604','120606']
lista_ubigeos = ['130602']

lista_errores = []
for ubigeo in lista_ubigeos:
    print ubigeo
    proceso = subprocess.Popen("python main.py {}".format(ubigeo), shell=True, stderr=subprocess.PIPE)
    errores = proceso.stderr.read()
    errores_print = '{}'.format(errores)
    print errores_print
    if len(errores_print) > 0:
        lista_errores.append(ubigeo)
        print 'algo salio mal'
        # conex.actualizar_flag_proc_segm(ubigeo,zona,flag=2,equipo=equipo,fase=fase)
    else:
        print 'nada salio mal'
        # conex.actualizar_flag_proc_segm(ubigeo, zona, flag=1,equipo=equipo,fase=fase)
    # estado_dist=conex.obtener_flag_segm_u_distrito(ubigeo=el[0],fase=fase)
    # if estado_dist>0:
    #     reporte_distrital.exportar_listado_urbano_distrito(ubigeo=ubigeo,fase=fase)
    #     conex.actualizar_monitoreo_segmentacion(ubigeo=ubigeo,fase=fase)

print lista_errores