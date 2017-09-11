# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from reportlab.platypus import Image
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4, landscape                          #   ->  Importa el tamaño de hoja a utilizar
from reportlab.lib import colors                                #   ->  Importa colores
from reportlab.platypus import Table                            #   -> Importa las funcionalidades para crear tablas
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, PageBreak
from  reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from Generales import settings


# ----------------------------------------------------------------------------------------------------------------------

# PARAMETROS

ubigeo = '120704'
EscudoNacional = r'D:\SegmentacionAutomatizadaAmbitoRural\Isumos\Img\ENP_BW.png'
LogoInei = r'D:\SegmentacionAutomatizadaAmbitoRural\Isumos\Img\Inei_BW.png'
workspace = r'D:\SegmentacionRuralV2\Procesamiento\Listados'

# ----------------------------------------------------------------------------------------------------------------------



conn = settings.conectionDB_pymmsql()


def registros(rows):
    ini = 12
    rango = 18
    dato = ini

    while dato < rows:
        dato = dato + rango
    lista_ini = list(range(ini, dato - (rango - 1), rango))
    lista_fin = list(range(ini + rango, dato + 1, rango))
    lista_fin[-1] = rows
    final = zip(lista_ini, lista_fin)
    final.append((0, 12))
    final.sort(key=lambda n: n[0])
    return final


def informacionUbicacion(ubigeo, conn=conn):
    cursor = conn.cursor()
    cursor.execute(u"SELECT DEPARTAMENTO, PROVINCIA, DISTRITO FROM VW_DISTRITO WHERE UBIGEO = '{}'".format(ubigeo))
    informacion = [{'depa': x[0], 'ccdd': ubigeo[0:2], 'prov': x[1], 'ccpr': ubigeo[2:4], 'dist': x[2], 'ccdi': ubigeo[4:6]} for x in cursor]
    cursor.close()
    return informacion[0]


def informacionSeccion(ubigeo, conn=conn):
    cursor = conn.cursor()
    cursor.execute(u"SELECT IDSCR, SCR FROM SEGM_R_SCR WHERE UBIGEO = '{}'".format(ubigeo))
    informacion = [{'idscr': x[0], 'scr': x[1]} for x in cursor]
    cursor.close()
    return informacion


def informacionRutas(idscr, conn=conn):
    cursor = conn.cursor()
    cursor.execute(u"SELECT RUTA FROM SEGM_R_RUTA WHERE IDSCR = '{}' ORDER BY RUTA".format(idscr))
    informacion = [x[0] for x in cursor]
    cursor.close()
    return informacion


def informacionCcppRutas(idscr, conn=conn):
    cursor = conn.cursor()
    cursor.execute(u"SELECT CODCCPP, NOMCCPP, AER_INI, AER_FIN, VIV_CCPP FROM SEGM_R_CCPPRUTA WHERE IDSCR = '{}' ORDER BY IDRUTA, OR_CCPP".format(idscr))
    informacion = [{'cod': x[0], 'nomccpp': x[1], 'aerini': x[2], 'aerfin': x[3], 'nviv': x[4]} for x in cursor]
    cursor.close()
    return informacion


def titulo(Elementos):

    h_sub_tile = PS(
        name='Heading1',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )
    h_sub_tile_2 = PS(
        name='Heading1',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER
    )

    Titulo = Paragraph(u'CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA Y III DE COMUNIDADES INDÍGENAS', h_sub_tile)
    Titulo2 = Paragraph(u'III Censo de Comunidades Nativas de la Amazonía Peruana y I Censo de Comunidades Campesinas', h_sub_tile)
    SubTitulo = Paragraph(u'<strong>PROGRAMACIÓN DE RUTAS  DEL JEFE/A DE SECCIÓN</strong>', h_sub_tile_2)

    CabeceraPrincipal = [[Image(EscudoNacional, width=50, height=50), Titulo, Image(LogoInei, width=50, height=50)],
                         ['', Titulo2, ''],
                         ['', SubTitulo, '']]

    Tabla0 = Table(CabeceraPrincipal, colWidths=[2 * cm, 22 * cm, 2 * cm])

    Tabla0.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('SPAN', (0, 0), (0, 2)),
        ('SPAN', (2, 0), (2, 2)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    Elementos.append(Tabla0)
    Elementos.append(Spacer(0, 10))
    return Elementos


def cabeceraPrincipal(Elementos, ccdd, ccpr, ccdi, depa,prov, dist, scr, ruta):
    h1 = PS(
        name='Heading1',
        fontSize=7,
        leading=8
        )

    h11 = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
        )

    h111 = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_RIGHT
        )

    Filas = [
        ['', '', '', '', '', '', '', '', Paragraph('<b>Doc.CPV.03.116</b>', h111)],
        [Paragraph(u'<b>UBICACIÓN GEOGRÁFICA</b>', h11), '', '', '', Paragraph(u'<b>SEDE OPERATIVA</b>', h1), ccdd, depa, '', Paragraph(u'<b>NOMBRE Y APELLIDO DEL JEFE / A DE SECCIÓN</b>', h11)],
        [Paragraph(u'<b>DEPARTAMENTO</b>', h1), u'{}'.format(ccdd), u'{}'.format(depa), '', Paragraph(u'<b>SECCIÓN</b>', h1), u'{}'.format(scr), '', '', u'{}'.format('')],
        [Paragraph(u'<b>PROVINCIA</b>', h1), u'{}'.format(ccpr), u'{}'.format(prov), '', Paragraph(u'<b>RUTAS</b>', h1), u'{}'.format(ruta), '', '', ''],
        [Paragraph(u'<b>DISTRITO</b>', h1), u'{}'.format(ccdi), u'{}'.format(dist), '', '', '', '', '', ''],
    ]

    Tabla = Table(Filas, colWidths=[3 * cm, 1 * cm, 4.7 * cm, 1.35 * cm, 3 * cm, 1 * cm, 4.7 * cm, 1.35 * cm, 8.4 * cm],
                  rowHeights=[0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm])

    Tabla.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (8, 0), colors.black),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (5, 2), (6, 2)),
        ('SPAN', (5, 3), (6, 3)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 1), (2, 1), 'CENTER'),
        ('ALIGN', (1, 2), (1, 4), 'CENTER'),
        ('ALIGN', (5, 1), (6, 3), 'CENTER'),
        ('ALIGN', (8, 1), (8, 1), 'CENTER'),
        ('ALIGN', (6, 1), (6, 1), 'LEFT'),
        ('ALIGN', (2, 2), (2, 4), 'LEFT'),
        ('ALIGN', (0, 2), (0, 4), 'LEFT'),
        ('ALIGN', (2, 2), (2, 4), 'LEFT'),
        ('ALIGN', (4, 1), (4, 3), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 1), (2, 4), 1, colors.black),
        ('GRID', (4, 1), (6, 3), 1, colors.black),
        ('GRID', (8, 1), (8, 2), 1, colors.black),
        ('BACKGROUND', (0, 1), (2, 1), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255)),
        ('BACKGROUND', (0, 2), (0, 4), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255)),
        ('BACKGROUND', (4, 1), (4, 3), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255)),
        ('BACKGROUND', (8, 1), (8, 1), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255)),
    ]))

    # AGREGANDO LAS TABLAS A LA LISTA DE ELEMENTOS DEL PDF

    Elementos.append(Tabla)
    Elementos.append(Spacer(0, 10))


def cabeceraSecundaria(Elementos):
    h3 = PS(
        name='Normal',
        fontSize=5,
        leading=10,
        alignment=TA_CENTER
        )

    Filas2 = [
        [Paragraph(e, h3) for e in [u"N°", u"COD.", u"CENTRO POBLADO", u"UBICACION CENSAL", "", u"VIV.", u"DÍAS DE TRABAJO", "", u"FECHAS DE TRABAJO", "", u"DIAS DE OPERACION DE CAMPO", "", "", "", "", "", "", "", u"ASIGNACIÓN DE FONDOS", "", "", "", "", "", u"OBS."]],
        [Paragraph(e, h3) for e in ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", u"PSJ.", u"MOV. LOCAL", u"VIATICOS S/", "", "", u"TOT. GEN.", ""]],
        [Paragraph(e, h3) for e in ["", "", "", u"AER INI", u"AER FIN", "", u"DIA<br/>INI", u"DIA FIN", u"FECH. INI", u"FECH. FIN", u"VIAJE", u"TRAS.", u"EMP", u"CONT. CAL.", u"GAB.", u"DESC.", u"DIAS. OPER.", u"TOT. DIAS", "", "", "100", "120", u"TOT.", "", ""]],
    ]

    Tabla2 = Table(Filas2, colWidths=[0.67 * cm, 0.9 * cm, 4.33 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.21 * cm])

    Tabla2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('SPAN', (0, 0), (0, 2)),
        ('SPAN', (1, 0), (1, 2)),
        ('SPAN', (2, 0), (2, 2)),
        ('SPAN', (3, 0), (4, 1)),
        ('SPAN', (5, 0), (5, 2)),
        ('SPAN', (6, 0), (7, 1)),
        ('SPAN', (8, 0), (9, 1)),
        ('SPAN', (10, 0), (17, 1)),
        ('SPAN', (18, 0), (23, 0)),
        ('SPAN', (18, 1), (18, 2)),
        ('SPAN', (19, 1), (19, 2)),
        ('SPAN', (20, 1), (22, 1)),
        ('SPAN', (23, 1), (23, 2)),
        ('SPAN', (24, 0), (24, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255)),
        ]))

    Elementos.append(Tabla2)
    return Tabla2


def informacionEspecificaInferior(Elementos, ccpps):
    h4 = PS(name='Normal', fontSize=5, leading=10, alignment=TA_LEFT)
    n = 0
    for x in ccpps:
        n = n + 1
        registros = [[n, x['cod'], Paragraph(u'{}'.format(x['nomccpp']), h4), u'{}'.format(x['aerini']), u'{}'.format(x['aerfin']), x['nviv'],
                      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

        RegistrosIngresados = Table(registros,
                                    colWidths=[0.67 * cm, 0.9 * cm, 4.33 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.21 * cm],
                                    rowHeights=[1 * cm])

        RegistrosIngresados.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 0), (2, 0), 'LEFT'),
            ('ALIGN', (24, 0), (24, 0), 'LEFT'),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (3, 0), (23, 0), 'CENTER'),
        ]))

        Elementos.append(RegistrosIngresados)


def informacionEspecificaSuperior(Elementos, ccpps, cab, rows):
    h4 = PS(name='Normal', fontSize=5, leading=10, alignment=TA_LEFT)
    rang = registros(rows)
    n = 0
    for m in rang:
        for x in ccpps[m[0]: m[1]]:
            n = n + 1
            reg = [[n, x['cod'], Paragraph(u'{}'.format(x['nomccpp']), h4), u'{}'.format(x['aerini']), u'{}'.format(x['aerfin']), x['nviv'],
                          "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

            RegistrosIngresados = Table(reg,
                                        colWidths=[0.67 * cm, 0.9 * cm, 4.33 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm, 1.14 * cm,
                                          1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm,
                                          1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.21 * cm],
                                        rowHeights=[1 * cm])

            RegistrosIngresados.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 5),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (2, 0), (2, 0), 'LEFT'),
                ('ALIGN', (24, 0), (24, 0), 'LEFT'),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('ALIGN', (3, 0), (23, 0), 'CENTER'),
            ]))

            Elementos.append(RegistrosIngresados)
        Elementos.append(PageBreak())
        Elementos.append(cab)
    del Elementos[-1]
    del Elementos[-1]



def piePagina(Elementos, tipo, scr=None):
    if tipo == 1 and scr == None:
        registros = [["TOTAL", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]
    else:
        registros = [["TOTAL DE LA SECCION '{}'".format(scr), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

    RegistrosPiepagina = Table(registros,
                                colWidths=[7.9 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.14 * cm,
                                      1 * cm, 1 * cm, 1 * cm, 1 * cm, 1.21 * cm],
                                rowHeights=[0.6 * cm])

    colores = ('BACKGROUND', (0, 0), (21, 0), colors.Color(235.0 / 255, 235.0 / 255, 235.0 / 255)) if tipo == 1 else ('BACKGROUND', (0, 0), (21, 0), colors.Color(220.0 / 255, 220.0 / 255, 220.0 / 255))

    RegistrosPiepagina.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        colores,
    ]))

    Elementos.append(RegistrosPiepagina)


def gemerarPDF(Elementos, workspace, ubigeo, idscr):
    destino = r'{}\rural\{}\{}-PR.pdf'.format(workspace, ubigeo, idscr)
    pdf = SimpleDocTemplate(destino, pagesize=landscape(A4), rightMargin=0.5 * cm, leftMargin=0.5 * cm, topMargin=0.5 * cm, bottomMargin=0.5 * cm, showBoundary=0)
    pdf.build(Elementos)


def main(ubigeo, workspace):
    info = informacionUbicacion(ubigeo)
    secciones = informacionSeccion(ubigeo)
    for x in secciones:
        Elementos = []
        titulo(Elementos)
        rutasScr = informacionRutas(x['idscr'])
        rutas = ', '.join(rutasScr)
        cabeceraPrincipal(Elementos, info['ccdd'], info['ccpr'], info['ccdi'], info['depa'], info['prov'], info['dist'], x['scr'], rutas)
        cab = cabeceraSecundaria(Elementos)
        ccpps = informacionCcppRutas(x['idscr'])
        nrows = len(ccpps)
        if nrows <= 11:
            informacionEspecificaInferior(Elementos, ccpps)
            piePagina(Elementos, 1)
            piePagina(Elementos, 2, x['scr'])
        else:
            if nrows == 12:
                informacionEspecificaInferior(Elementos, ccpps)
                piePagina(Elementos, 1)
                piePagina(Elementos, 2, x['scr'])
            else:
                informacionEspecificaSuperior(Elementos, ccpps, cab, nrows)
                piePagina(Elementos, 1)
                piePagina(Elementos, 2, x['scr'])

        gemerarPDF(Elementos, workspace, ubigeo, x['idscr'])

main(ubigeo, workspace)

