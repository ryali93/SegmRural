# -*- coding: utf-8 -*-
from Conexiones import settings
from reportlab.platypus import Image
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4, landscape                          #   ->  Importa el tamaño de hoja a utilizar
from reportlab.lib import colors                                #   ->  Importa colores
from reportlab.platypus import Table                            #   -> Importa las funcionalidades para crear tablas
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, PageBreak
from  reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

#   VARIABLE

Elementos = []
EscudoNacional = r'D:\SegmentacionAutomatizadaAmbitoRural\Isumos\Img\ENP_BW.png'
LogoInei = r'D:\SegmentacionAutomatizadaAmbitoRural\Isumos\Img\Inei_BW.png'


def cabeceraPrincipal(Elementos, EscudoNacional, LogoInei):

    Titulo = Paragraph(u'CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA Y III DE COMUNIDADES INDÍGENAS', h_sub_tile)
    Titulo2 = Paragraph(u'III Censo de Comunidades Nativas de la Amazonía Peruana y I Censo de Comunidades Campesinas', h_sub_tile)
    SubTitulo = Paragraph(u'<strong>PROGRAMACIÓN DE RUTAS DEL/ LA EMPADRONADOR/A</strong>', h_sub_tile_2)

    CabeceraPrincipal = [[Titulo, '', ''],
                         [Image(EscudoNacional, width=50, height=50), Titulo2, Image(LogoInei, width=50, height=50)],
                         ['', SubTitulo, '']]

    Tabla0 = Table(CabeceraPrincipal, colWidths=[2 * cm, 14 * cm, 2 * cm])

    Tabla0.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('SPAN', (0, 1), (0, 2)),
        ('SPAN', (2, 1), (2, 2)),
        ('SPAN', (0, 0), (2, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    Elementos.append(Tabla0)
    Elementos.append(Spacer(0, 10))
    return Elementos


def gemerarPDF(Elementos, EscudoNacional, LogoInei):

    a = cabeceraPrincipal(Elementos, EscudoNacional, LogoInei)

    PathPDF = u'D:\prueba.pdf'

    pdf = SimpleDocTemplate(PathPDF, pagesize=landscape(A4), rightMargin=65,
                            leftMargin=65,
                            topMargin=0.5 * cm,
                            bottomMargin=0.5 * cm, )

    #   GENERACION DEL PDF FISICO

    pdf.build(a)



gemerarPDF(Elementos, EscudoNacional, LogoInei)


