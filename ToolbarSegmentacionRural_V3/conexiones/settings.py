#   CONEXIONes a la base de datos Mysql

import arcpy
import pymssql


arcpy.env.overwriteOutput = True

ip = "172.18.1.41"
nombre = 'CPV_SEGMENTACION'





#def conectionDB_arcpy():
#    if arcpy.Exists("{}.sde".format(nombre)) == False:
#        arcpy.CreateDatabaseConnection_management("Database Connections",
#                                                  "{}.sde".format(nombre),
#                                                  "SQL_SERVER",
#                                                  ip,
#                                                  "DATABASE_AUTH",
#                                                  "us_arcgis_seg",
#                                                  "@rcMapUs3rtest",
#                                                  "#",
#                                                  nombre,
#                                                  "#",
#                                                  "#",
#                                                  "#",
#                                                  "#")
#
#    conexionDB = r'Database Connections\{}.sde'.format(nombre)
#    return conexionDB


def conectionGDB_arcpy():
    if arcpy.Exists("GEODB_CPV_SEGM.sde") == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  'GEODB_CPV_SEGM.sde',
                                                  'SQL_SERVER',
                                                  ip,
                                                  'DATABASE_AUTH',
                                                  'sde',
                                                  "$deDEs4Rr0lLo",
                                                  "#",
                                                  'GEODB_CPV_SEGM',
                                                  "#",
                                                  '#',
                                                  '#',
                                                  "#")

    conexionGDB = r'Database Connections\GEODB_CPV_SEGM.sde\GEODB_CPV_SEGM.SDE.RURAL'
    return conexionGDB




ip = "192.168.202.84"
nombre = 'INEI_BDCARTOGRAFIA_GIS'
user='sde'
password='wruvA7a*tat*'

def conectionDB_arcpy2():
    if arcpy.Exists("{}.sde".format(nombre)) == False:
        arcpy.CreateDatabaseConnection_management("Database Connections",
                                                  "{}.sde".format(nombre),
                                                  "SQL_SERVER",
                                                  ip,
                                                  "DATABASE_AUTH",
                                                  user,
                                                  password,
                                                  "#",
                                                  nombre,
                                                  "#",
                                                  "#",
                                                  "#",
                                                  "#")

    conexionDB = r'Database Connections\{}.sde'.format(nombre)
    return conexionDB



def conectionDB_pymmsql():
    user_sde = "us_arcgis_seg"     
    password_sde = "@rcMapUs3rtest"
    conexion = pymssql.connect(ip, user_sde, password_sde, nombre)
    return conexion

#conectionDB_arcpy2()