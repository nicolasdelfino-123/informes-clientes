from pathlib import Path
import webbrowser

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

# =========================================================
# INFORME BREVE - CATALOGOWEB
# Cliente: Romina - Danna Decants
# Periodo: 18/05/2026 al 14/06/2026
# Objetivo: reporte breve, positivo, real y comercial.
# Regla madre: mostrar datos reales, seleccionar solo lo que suma,
# excluir /admin y evitar metricas debiles o poco representativas.
# =========================================================

DATA = {
    "cliente": "Romina",
    "negocio": "Danna Decants",
    "periodo": "18/05/2026 al 14/06/2026",
    "dias_periodo": 28,
    "fecha_emision": "15/06/2026",

    # METRICAS PRINCIPALES REALES - GOOGLE ANALYTICS
    "sesiones": 369,
    "usuarios_activos": 259,
    "usuarios_nuevos": 259,
    "usuarios_recurrentes": 32,
    "vistas_pagina": 1164,
    "eventos_totales": 2506,
    "sesiones_interaccion": 300,
    "porcentaje_interaccion": "81,3%",
    "tiempo_promedio_usuario_activo": "1 min y 21 s",
    "duracion_media_sesion": "3 min y 28 s",
    "vistas_por_sesion": "3,15",
    "vistas_por_usuario": "4,49",

    # EVENTOS PUBLICOS DESTACADOS - NO INCLUIR ADMIN
    "eventos_destacados": [
        ("Vistas de pagina", 1164, "El catalogo tuvo un volumen claro de consulta y recorrido."),
        ("Scrolls", 295, "Los visitantes bajaron dentro de la pagina para seguir mirando contenido."),
        ("Productos vistos", 158, "Hubo interes directo en productos concretos del catalogo."),
        ("Interacciones activas", 71, "Usuarios que permanecieron y siguieron usando la pagina."),
        ("Selecciones de tamano", 69, "Dato clave para decants: hubo eleccion activa de presentaciones."),
        ("Agregados al carrito", 58, "Senal comercial positiva: personas avanzaron hacia una posible compra."),
        ("Inicios de formulario", 40, "Usuarios que llegaron a una instancia de consulta o carga de datos."),
        ("Categorias exploradas", 15, "Los visitantes compararon secciones del catalogo."),
        ("Pedidos por WhatsApp", 7, "Aunque es un numero menor, es importante porque muestra llegada al canal final de contacto."),
    ],

    # PAGINAS PUBLICAS PRINCIPALES - SIN /ADMIN
    "paginas_principales": [
        ("Pagina principal", 314, 202, "Fue la vidriera principal y concentro el mayor alcance."),
        ("Listado de productos", 217, 126, "Muchos usuarios avanzaron a revisar la oferta completa."),
        ("Categoria Femeninos", 116, 58, "Categoria con buen movimiento e interes claro."),
        ("Inicio", 114, 69, "Recorrido importante dentro de la estructura principal."),
        ("Categoria Masculinos", 83, 57, "Interes parejo y buena cantidad de usuarios."),
    ],

    # CANALES CON DATOS FUERTES
    "canales": [
        ("Redes sociales organicas", 286, "77,51%", "Principal fuente de movimiento. El link esta funcionando desde redes."),
        ("Trafico directo", 80, "21,68%", "Accesos desde enlaces compartidos, WhatsApp, estados o personas que vuelven al link."),
    ],

    # UBICACIONES LATAM/AMERICA RELEVANTES - EXCLUIR EEUU, IRLANDA, INDONESIA, ETC.
    "ciudades": [
        ("Punta Arenas", 137),
        ("Santiago", 56),
        ("Puerto Natales", 27),
        ("Concepcion", 13),
    ],

    "resumen": (
        "Durante el periodo analizado, el catalogo registro 369 visitas, 259 usuarios activos, "
        "1.164 vistas de pagina y 2.506 acciones dentro del sitio. Esto muestra que la pagina "
        "esta funcionando como una vidriera digital activa: las personas entran, recorren productos, "
        "exploran categorias, seleccionan tamanos, agregan productos al carrito y llegan al contacto por WhatsApp."
    ),

    "lectura": (
        "Lo mas positivo es la calidad del uso: el 81,3% de las visitas tuvo interaccion, con 300 sesiones activas "
        "y un promedio de 3,15 paginas vistas por visita. Esto indica que el catalogo no solo recibe ingresos, sino que "
        "tambien retiene la atencion y ayuda a ordenar la consulta de productos antes de pasar a WhatsApp."
    ),

    "recomendaciones": [
        "Mantener el link del catalogo fijo en la biografia de Instagram, Facebook y WhatsApp Business.",
        "Compartir una categoria distinta por dia en historias o estados: Femeninos, Masculinos y listado general.",
        "Cuando consulten por un producto, responder con el link directo para que la persona siga mirando opciones.",
        "Usar estados con frases simples: 'Catalogo actualizado', 'Elegis el tamano y pedis por WhatsApp', 'Mira los productos disponibles'.",
        "Revisar cada semana fotos, precios y disponibilidad para sostener confianza y evitar consultas repetidas.",
    ],

    "cierre": (
        "En resumen, el catalogo esta teniendo movimiento real y cumple su funcion principal: mostrar la oferta, "
        "ordenar las consultas y llevar a los visitantes hacia acciones comerciales concretas. Si se comparte de forma "
        "constante, puede seguir ganando recorrido y convertirse cada vez mas en una herramienta diaria de venta."
    ),
}

# =========================================================
# ESTILOS
# =========================================================

VERDE = colors.HexColor("#168765")
VERDE_OSCURO = colors.HexColor("#0F5F49")
VERDE_CLARO = colors.HexColor("#E4F5EE")
AZUL = colors.HexColor("#285C8E")
AZUL_CLARO = colors.HexColor("#EAF1FA")
AMARILLO = colors.HexColor("#B58110")
AMARILLO_CLARO = colors.HexColor("#FFF5D8")
GRIS_OSCURO = colors.HexColor("#252525")
GRIS_MEDIO = colors.HexColor("#666666")
GRIS_CLARO = colors.HexColor("#F6F6F3")
GRIS_LINEA = colors.HexColor("#D9D9D9")
BLANCO = colors.white


def fmt_num(n):
    if isinstance(n, int):
        return f"{n:,}".replace(",", ".")
    return str(n)


def safe_text(txt):
    return str(txt).replace("&", "&amp;")


def p(txt, style):
    return Paragraph(safe_text(txt), style)


def filtrar_items_fuertes(items, min_num=10, excepciones=None):
    """
    Deja afuera metricas bajas por defecto.
    excepciones permite mostrar un dato menor a 10 cuando es comercialmente clave,
    por ejemplo pedidos por WhatsApp.
    """
    excepciones = excepciones or set()
    filtrados = []
    for item in items:
        nombre = item[0]
        numero = item[1]
        if numero >= min_num or nombre in excepciones:
            filtrados.append(item)
    return filtrados


def build_pdf(data, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=13 * mm,
        rightMargin=13 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    styles = {
        "marca": ParagraphStyle("marca", fontName="Helvetica-Bold", fontSize=10.5, textColor=VERDE, leading=12),
        "fecha": ParagraphStyle("fecha", fontName="Helvetica", fontSize=8, textColor=GRIS_MEDIO, alignment=TA_RIGHT, leading=10),
        "titulo": ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=20, textColor=GRIS_OSCURO, leading=23),
        "subtitulo": ParagraphStyle("subtitulo", fontName="Helvetica", fontSize=9.5, textColor=GRIS_MEDIO, leading=12),
        "seccion": ParagraphStyle("seccion", fontName="Helvetica-Bold", fontSize=10.2, textColor=VERDE_OSCURO, leading=12, spaceBefore=5, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=8.9, textColor=GRIS_OSCURO, leading=12.2, spaceAfter=4),
        "body_bold": ParagraphStyle("body_bold", fontName="Helvetica-Bold", fontSize=8.9, textColor=GRIS_OSCURO, leading=12.2),
        "metric_num": ParagraphStyle("metric_num", fontName="Helvetica-Bold", fontSize=17, textColor=VERDE, alignment=TA_CENTER, leading=19),
        "metric_lbl": ParagraphStyle("metric_lbl", fontName="Helvetica", fontSize=7.1, textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=8.5),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold", fontSize=7.2, textColor=BLANCO, leading=8.5),
        "table_cell": ParagraphStyle("table_cell", fontName="Helvetica", fontSize=7.2, textColor=GRIS_OSCURO, leading=8.6),
        "box_title": ParagraphStyle("box_title", fontName="Helvetica-Bold", fontSize=8.6, textColor=GRIS_OSCURO, leading=10.5),
        "box_text": ParagraphStyle("box_text", fontName="Helvetica", fontSize=8.0, textColor=GRIS_OSCURO, leading=10.2),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=7, textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=8),
    }

    story = []

    # Header
    header = Table([[p("catalogoweb.ar", styles["marca"]), p(f"Emitido: {data['fecha_emision']}", styles["fecha"])]], colWidths=[90 * mm, 90 * mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(header)
    story.append(HRFlowable(width="100%", thickness=1.2, color=VERDE, spaceAfter=7))

    story.append(p("Informe breve de actividad del catalogo", styles["titulo"]))
    story.append(p(f"{data['negocio']} - Periodo: {data['periodo']} ({data['dias_periodo']} dias)", styles["subtitulo"]))
    story.append(Spacer(1, 6))

    # Metricas fuertes
    metricas = [
        (data["sesiones"], "Visitas / sesiones"),
        (data["usuarios_activos"], "Usuarios activos"),
        (data["vistas_pagina"], "Vistas de pagina"),
        (data["eventos_totales"], "Acciones registradas"),
    ]
    metricas_2 = [
        (data["sesiones_interaccion"], "Visitas con interaccion"),
        (data["porcentaje_interaccion"], "Interaccion"),
        (data["vistas_por_sesion"], "Vistas por visita"),
        (data["usuarios_recurrentes"], "Usuarios recurrentes"),
    ]

    def metric_table(metrics, bg, line_color):
        rows = [
            [p(fmt_num(m[0]), styles["metric_num"]) for m in metrics],
            [p(m[1], styles["metric_lbl"]) for m in metrics],
        ]
        t = Table(rows, colWidths=[45 * mm] * 4)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
            ("TOPPADDING", (0, 1), (-1, 1), 1),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
            ("LINEAFTER", (0, 0), (2, 1), 0.3, line_color),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    metric_table(metricas, VERDE_CLARO, VERDE)
    metric_table(metricas_2, AZUL_CLARO, AZUL)

    # Resumen humano
    resumen_box = Table([[p("Lectura general", styles["box_title"]), p(data["resumen"] + " " + data["lectura"], styles["box_text"])]], colWidths=[34 * mm, 146 * mm])
    resumen_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMARILLO_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMARILLO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(resumen_box)
    story.append(Spacer(1, 6))

    # Eventos destacados
    story.append(p("Actividad destacada", styles["seccion"]))
    eventos = filtrar_items_fuertes(data["eventos_destacados"], excepciones={"Pedidos por WhatsApp"})
    rows = [[p("Accion", styles["table_head"]), p("Cantidad", styles["table_head"]), p("Lectura comercial", styles["table_head"])]]
    for nombre, cantidad, lectura in eventos:
        rows.append([p(nombre, styles["table_cell"]), p(fmt_num(cantidad), styles["table_cell"]), p(lectura, styles["table_cell"])])
    t_eventos = Table(rows, colWidths=[42 * mm, 24 * mm, 114 * mm], repeatRows=1)
    t_eventos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERDE),
        ("GRID", (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    story.append(t_eventos)
    story.append(Spacer(1, 5))

    # Paginas principales publicas + canales en dos columnas
    story.append(p("Secciones mas consultadas", styles["seccion"]))
    rows_paginas = [[p("Seccion", styles["table_head"]), p("Vistas", styles["table_head"]), p("Usuarios", styles["table_head"]), p("Lectura", styles["table_head"])]]
    for nombre, vistas, usuarios, lectura in data["paginas_principales"]:
        rows_paginas.append([p(nombre, styles["table_cell"]), p(fmt_num(vistas), styles["table_cell"]), p(fmt_num(usuarios), styles["table_cell"]), p(lectura, styles["table_cell"])])
    t_paginas = Table(rows_paginas, colWidths=[45 * mm, 18 * mm, 20 * mm, 97 * mm], repeatRows=1)
    t_paginas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.7),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    story.append(t_paginas)
    story.append(Spacer(1, 5))

    # Canales y ciudades, compacto
    canales_txt = "<br/>".join([f"<b>{c}</b>: {fmt_num(s)} sesiones ({pct}). {lect}" for c, s, pct, lect in data["canales"]])
    ciudades_txt = "<br/>".join([f"<b>{ciudad}</b>: {fmt_num(usuarios)} usuarios" for ciudad, usuarios in data["ciudades"]])
    two_cols = Table([[
        p("Origen del movimiento", styles["box_title"]),
        p("Ciudades principales", styles["box_title"]),
    ], [
        Paragraph(canales_txt, styles["box_text"]),
        Paragraph(ciudades_txt, styles["box_text"]),
    ]], colWidths=[88 * mm, 88 * mm])
    two_cols.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), AZUL_CLARO),
        ("BACKGROUND", (1, 0), (1, -1), GRIS_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AZUL),
        ("LINEBEFORE", (1, 0), (1, -1), 3, VERDE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(two_cols)
    story.append(Spacer(1, 5))

    # Recomendaciones
    story.append(p("Recomendaciones para seguir generando movimiento", styles["seccion"]))
    recs = "<br/>".join([f"• {safe_text(x)}" for x in data["recomendaciones"]])
    rec_box = Table([[Paragraph(recs, styles["box_text"])]], colWidths=[180 * mm])
    rec_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, VERDE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(rec_box)
    story.append(Spacer(1, 5))

    cierre_box = Table([[p("Conclusion", styles["box_title"]), p(data["cierre"], styles["box_text"])]], colWidths=[28 * mm, 152 * mm])
    cierre_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, VERDE_OSCURO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(cierre_box)

    # Footer minimo: se evita agregar contenido extra para mantener el informe en una sola pagina.

    doc.build(story)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "informe_romina_danna_decants.pdf"
    build_pdf(DATA, str(output))
    try:
        webbrowser.open(output.resolve().as_uri())
    except Exception:
        pass
