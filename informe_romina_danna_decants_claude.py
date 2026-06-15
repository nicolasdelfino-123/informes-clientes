from pathlib import Path
import webbrowser

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

# =========================================================
# INFORME MENSUAL - CATALOGOWEB
# Cliente: Romina - Danna Decants
# Periodo: 18/05/2026 al 14/06/2026
# Objetivo: retencion, percepcion de valor, lectura humana
# Una sola carilla, ultra positivo y comercial
# =========================================================

DATA = {
    "cliente": "Romina",
    "negocio": "Danna Decants",
    "periodo": "18/05/2026 al 14/06/2026",
    "dias_periodo": 28,
    "fecha_emision": "15/06/2026",

    # Metricas principales (reales, de las capturas)
    "sesiones": 369,
    "usuarios_activos": 259,
    "usuarios_nuevos": 259,
    "usuarios_recurrentes": 32,
    "vistas_pagina": 1164,
    "eventos_totales": 2506,
    "sesiones_interaccion": 300,
    "porcentaje_interaccion": "81,3%",
    "vistas_por_sesion": "3,15",
    "duracion_media_sesion": "3 min 28 s",

    # Eventos destacados (solo los que suman)
    "vio_producto": 158,
    "selecciono_tamano": 69,
    "agrego_al_carrito": 58,
    "exploro_categoria": 15,
    "solicito_pedido_whatsapp": 7,
    "scroll": 295,
    "user_engagement": 71,

    # Canales
    "fuente_principal": "Redes sociales organicas",
    "sesiones_social": 286,
    "sesiones_direct": 80,

    # Ciudades LATAM relevantes (>= 10 usuarios)
    "ciudades": [
        {"ciudad": "Punta Arenas", "usuarios": 137},
        {"ciudad": "Santiago",     "usuarios": 56},
        {"ciudad": "Puerto Natales","usuarios": 27},
        {"ciudad": "Concepcion",   "usuarios": 13},
    ],

    # Paginas publicas con mas movimiento (sin admin)
    "paginas": [
        {"pagina": "Portada",                     "vistas": 314,  "lectura": "La entrada principal del catalogo. El link funciona."},
        {"pagina": "Listado de productos",         "vistas": 217,  "lectura": "Las personas avanzan a explorar toda la oferta."},
        {"pagina": "Categoria Fragancias Femeninas","vistas": 116, "lectura": "Una de las secciones mas consultadas del periodo."},
        {"pagina": "Inicio",                       "vistas": 114,  "lectura": "Recorrido fuerte dentro de la estructura del sitio."},
        {"pagina": "Categoria Fragancias Masculinas","vistas": 83, "lectura": "Gran interes parejo entre masculino y femenino."},
    ],

    # Textos
    "resumen": (
        "Durante los ultimos 28 dias, el catalogo recibio 259 personas reales "
        "que navegaron, miraron productos, eligieron presentaciones y llegaron hasta el pedido por WhatsApp. "
        "Esas 259 personas generaron 369 visitas en total, lo que significa que muchos volvieron mas de una vez "
        "a revisar opciones antes de decidir. Eso es exactamente lo que tiene que hacer una vidriera digital: "
        "estar disponible, mostrar bien los productos y acompañar al cliente hasta la compra."
    ),

    "destacado": (
        "El 81% de las visitas fueron activas: las personas no solo entraron y salieron, sino que "
        "navegaron, bajaron el scroll, vieron productos y tomaron decisiones dentro del catalogo. "
        "En promedio, cada visita recorrio mas de 3 pantallas y paso casi 3 minutos y medio explorando."
    ),

    "flujo_comercial": (
        "Lo mas valioso del periodo es el recorrido comercial que se registra: 158 veces alguien miro "
        "un producto en detalle, 69 veces eligio la presentacion o tamano, 58 veces agrego un producto "
        "al carrito y 7 personas llegaron a solicitar el pedido por WhatsApp. Ese es el camino completo "
        "desde la vidriera hasta la venta, y el catalogo lo esta cumpliendo."
    ),

    "canales": (
        "La gran mayoria del trafico llego desde redes sociales organicas: 286 sesiones de Instagram y "
        "links compartidos. Otras 80 sesiones llegaron de forma directa, lo que indica clientes que "
        "guardan el link o lo reciben por WhatsApp y vuelven a consultarlo. La pagina esta circulando "
        "en los canales correctos."
    ),

    "recomendaciones": [
        "Compartir el link del catalogo todos los dias en historias o estados, aunque sea con una frase corta.",
        "Usar links directos a categorias: un dia Femeninos, otro Masculinos, otro el listado completo.",
        "Cuando alguien pregunte por un perfume, responder con el link del producto en vez de solo describirlo.",
        "Mantener el link fijo en la bio de Instagram y en el perfil de WhatsApp Business.",
        "Actualizar fotos, precios y disponibilidad seguido: los datos muestran que la gente consulta de verdad.",
    ],

    "cierre": (
        "El catalogo ya es una herramienta que trabaja sola las 24 horas: "
        "recibe visitas, muestra productos y lleva a los clientes hasta el pedido. "
        "Cuanto mas se comparta, mas crece ese movimiento."
    ),
}

# =========================================================
# COLORES Y ESTILOS
# =========================================================

VERDE       = colors.HexColor("#168765")
VERDE_OSCURO= colors.HexColor("#0F5F49")
VERDE_CLARO = colors.HexColor("#E4F5EE")
GRIS_OSCURO = colors.HexColor("#252525")
GRIS_MEDIO  = colors.HexColor("#666666")
GRIS_CLARO  = colors.HexColor("#F5F3EE")
GRIS_LINEA  = colors.HexColor("#D9D9D9")
AZUL_CLARO  = colors.HexColor("#EAF1FA")
AZUL        = colors.HexColor("#285C8E")
AMARILLO_CLARO = colors.HexColor("#FFF5D8")
AMARILLO    = colors.HexColor("#B58110")
BLANCO      = colors.white

W, H = A4


def fmt_num(n):
    if isinstance(n, int):
        return f"{n:,}".replace(",", ".")
    return str(n)


def p(txt, style):
    txt = str(txt).replace("&", "&amp;")
    return Paragraph(txt, style)


def build_pdf(data, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=11 * mm,
        bottomMargin=11 * mm,
    )

    S = {
        "marca":      ParagraphStyle("marca",      fontName="Helvetica-Bold", fontSize=12.8, textColor=VERDE,       leading=16),
        "fecha":      ParagraphStyle("fecha",      fontName="Helvetica",      fontSize=10.4, textColor=GRIS_MEDIO,  alignment=TA_RIGHT, leading=13),
        "titulo":     ParagraphStyle("titulo",     fontName="Helvetica-Bold", fontSize=26,   textColor=GRIS_OSCURO, leading=30),
        "subtitulo":  ParagraphStyle("subtitulo",  fontName="Helvetica",      fontSize=13,   textColor=GRIS_MEDIO,  leading=17),
        "seccion":    ParagraphStyle("seccion",    fontName="Helvetica-Bold", fontSize=13.8, textColor=VERDE_OSCURO,leading=17, spaceBefore=10, spaceAfter=7),
        "body":       ParagraphStyle("body",       fontName="Helvetica",      fontSize=13.4, textColor=GRIS_OSCURO, leading=18.8, spaceAfter=8),
        "small":      ParagraphStyle("small",      fontName="Helvetica",      fontSize=10.8, textColor=GRIS_MEDIO,  leading=13.5),
        "metric_num": ParagraphStyle("metric_num", fontName="Helvetica-Bold", fontSize=28,   textColor=VERDE,       alignment=TA_CENTER, leading=31),
        "metric_lbl": ParagraphStyle("metric_lbl", fontName="Helvetica",      fontSize=10.5, textColor=GRIS_MEDIO,  alignment=TA_CENTER, leading=13),
        "box_title":  ParagraphStyle("box_title",  fontName="Helvetica-Bold", fontSize=12.8, textColor=GRIS_OSCURO, leading=16),
        "box_text":   ParagraphStyle("box_text",   fontName="Helvetica",      fontSize=12.6, textColor=GRIS_OSCURO, leading=17.4),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold", fontSize=10.8, textColor=BLANCO,      leading=13.5),
        "table_cell": ParagraphStyle("table_cell", fontName="Helvetica",      fontSize=10.7, textColor=GRIS_OSCURO, leading=14.2),
        "bullet":     ParagraphStyle("bullet",     fontName="Helvetica",      fontSize=12.2, textColor=GRIS_OSCURO, leading=16.8),
        "footer":     ParagraphStyle("footer",     fontName="Helvetica",      fontSize=8.5,  textColor=GRIS_MEDIO,  alignment=TA_CENTER, leading=11),
    }

    story = []

    # ---- HEADER ----
    def header():
        t = Table([[
            p("catalogoweb.ar", S["marca"]),
            p(f"Emitido: {data['fecha_emision']}", S["fecha"]),
        ]], colWidths=[88 * mm, 88 * mm])
        t.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(HRFlowable(width="100%", thickness=1.2, color=VERDE, spaceAfter=7))

    # ---- FOOTER ----
    def footer():
        story.append(Spacer(1, 5))
        story.append(HRFlowable(width="100%", thickness=0.3, color=GRIS_LINEA, spaceBefore=4, spaceAfter=4))
        story.append(p("Informe mensual de actividad del catalogo — catalogoweb.ar", S["footer"]))

    # ---- CAJA LATERAL ----
    def note_box(title, text, bg=AZUL_CLARO, accent=AZUL, title_width=38):
        tbl = Table([[
            p(title, S["box_title"]),
            p(text,  S["box_text"]),
        ]], colWidths=[title_width * mm, (176 - title_width) * mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), bg),
            ("LINEBEFORE",    (0, 0), (0,  -1), 3, accent),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 5))

    # ---- TABLA GENERICA ----
    def simple_table(headers, rows, col_widths):
        data_rows = [[p(h, S["table_head"]) for h in headers]]
        for row in rows:
            data_rows.append([p(cell, S["table_cell"]) for cell in row])
        tbl = Table(data_rows, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  VERDE),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
            ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
            ("BACKGROUND",    (0, 1), (-1, -1), BLANCO),
            ("ROWBACKGROUNDS",(0, 2), (-1, -1), [BLANCO, GRIS_CLARO]),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 5))

    # =========================================================
    # PAGINA 0 — GLOSARIO: que significa cada cosa
    # =========================================================

    """
    from reportlab.platypus import PageBreak

    header()

    story.append(p("Antes de leer el informe: que significa cada numero", S["titulo"]))
    story.append(p(
        "Este informe usa datos de Google Analytics. Aca te explicamos cada termino en palabras simples "
        "para que puedas leer los resultados sin necesidad de saber nada de tecnologia.",
        S["subtitulo"]
    ))
    story.append(Spacer(1, 9))

    # Glosario en tabla de dos columnas: termino | explicacion
    GLOSARIO = [
        ("Visitas / Sesiones",
         "Cada vez que alguien abre tu catalogo cuenta como una visita. Si la misma persona entra "
         "el lunes y vuelve el jueves, eso son 2 visitas. Por eso las visitas siempre son mas que las personas."),

        ("Personas alcanzadas\n(Usuarios activos)",
         "La cantidad de personas distintas que usaron el catalogo durante el mes. "
         "Una persona puede haber entrado 5 veces, pero se cuenta solo una vez aqui."),

        ("Usuarios nuevos",
         "Personas que entraron al catalogo por primera vez en el periodo. "
         "No lo habian visitado antes."),

        ("Usuarios recurrentes",
         "Personas que ya habian visitado el catalogo en otro momento y volvieron. "
         "Son clientes que recuerdan la pagina y regresan a consultar. Muy buena senal."),

        ("Pantallas consultadas\n(Vistas de pagina)",
         "Cada vez que alguien abre una seccion del catalogo -la portada, una categoria, un producto- "
         "se cuenta como una vista. Si una persona mira 4 productos distintos, eso son 4 vistas."),

        ("Acciones registradas\n(Eventos)",
         "Todo lo que hace una persona dentro del catalogo queda registrado: abrir una pagina, "
         "bajar el scroll, tocar un producto, elegir un tamano, agregar al carrito. Cada accion es un evento."),

        ("Visitas activas\n(Sesiones con interaccion)",
         "Son las visitas donde la persona realmente uso el catalogo: navego, exploro, toco algo. "
         "Si alguien solo abrio la pagina y la cerro sin interactuar, no cuenta aqui."),

        ("Tasa de interaccion",
         "El porcentaje de visitas donde hubo actividad real. Si dice 81%, significa que de cada 10 "
         "personas que entraron, 8 se quedaron a explorar. Cuanto mas alto, mejor."),

        ("Pantallas por visita",
         "Cuantas secciones recorre en promedio cada persona durante una visita. "
         "Un numero alto indica que la gente no solo mira la portada: navega y explora el catalogo."),

        ("Tiempo medio por visita",
         "Cuanto tiempo pasa en promedio cada persona dentro del catalogo por cada visita. "
         "Mas tiempo = mas interes en los productos."),

        ("Redes sociales organicas\n(Organic Social)",
         "Visitas que llegaron desde Instagram, Facebook u otras redes sociales, sin pagar publicidad. "
         "Alguien vio el link en una historia, en una publicacion o en el bio y entro."),

        ("Trafico directo\n(Direct)",
         "Visitas de personas que ya tenian el link guardado o lo recibieron por WhatsApp, "
         "por mensaje privado o por un estado. Entraron directamente sin pasar por Google ni redes."),

        ("Busqueda organica\n(Organic Search)",
         "Visitas que llegaron porque alguien busco algo en Google u otro buscador y aparecio el catalogo. "
         "Es una señal de que la pagina esta ganando presencia en internet."),
    ]

    glosario_rows = [
        [p("Termino", S["table_head"]), p("Que significa en palabras simples", S["table_head"])]
    ]
    for i, (termino, explicacion) in enumerate(GLOSARIO):
        glosario_rows.append([
            p(termino, S["box_title"]),
            p(explicacion, S["box_text"]),
        ])

    tglosario = Table(glosario_rows, colWidths=[52 * mm, 124 * mm], repeatRows=1)
    tglosario.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  VERDE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [VERDE_CLARO, BLANCO]),
        ("LINEBEFORE",    (0, 0), (0, -1),  3, VERDE),
    ]))
    story.append(tglosario)

    footer()
    story.append(PageBreak())
    """

    # =========================================================
    # CONTENIDO — una sola carilla (dos paginas si es necesario)
    # =========================================================

    header()

    # Titulo
    story.append(p("Informe mensual de actividad", S["titulo"]))
    story.append(p(
        f"{data['negocio']}  —  Periodo: {data['periodo']}  ({data['dias_periodo']} dias)",
        S["subtitulo"]
    ))
    story.append(Spacer(1, 14))
    note_box(
        "Para tener en cuenta",
        "Ningun numero por si solo dice todo. Lo importante es verlos en conjunto: "
        "cuantas personas llegaron, cuanto exploraron, que acciones tomaron y si el catalogo "
        "está funcionando con una vidriera digital las 24hs.",
        bg=AMARILLO_CLARO,
        accent=AMARILLO,
        title_width=56,
    )
    story.append(Spacer(1, 2))

    # --- BLOQUE 1: METRICAS PRINCIPALES (fila verde) ---
    m1 = [
        (data["sesiones"],           "Visitas totales"),
        (data["usuarios_activos"],   "Personas alcanzadas"),
        (data["vistas_pagina"],      "Pantallas consultadas"),
        (data["eventos_totales"],    "Acciones registradas"),
    ]
    row_nums = [p(fmt_num(m[0]), S["metric_num"]) for m in m1]
    row_lbl  = [p(m[1],          S["metric_lbl"]) for m in m1]
    t1 = Table([row_nums, row_lbl], colWidths=[44 * mm] * 4)
    t1.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), VERDE_CLARO),
        ("TOPPADDING",    (0, 0), (-1, 0),  8),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  1),
        ("TOPPADDING",    (0, 1), (-1, 1),  1),
        ("BOTTOMPADDING", (0, 1), (-1, 1),  8),
        ("LINEAFTER",     (0, 0), (2,  1),  0.4, VERDE),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4))

    # --- BLOQUE 2: METRICAS SECUNDARIAS (fila azul) ---
    m2 = [
        (data["sesiones_interaccion"],   "Visitas activas"),
        (data["porcentaje_interaccion"], "Tasa de interaccion"),
        (data["vistas_por_sesion"],      "Pantallas por visita"),
        (data["duracion_media_sesion"],  "Tiempo medio por visita"),
    ]
    row_nums2 = [p(str(m[0]), S["metric_num"]) for m in m2]
    row_lbl2  = [p(m[1],       S["metric_lbl"]) for m in m2]
    t2 = Table([row_nums2, row_lbl2], colWidths=[38 * mm, 40 * mm, 43 * mm, 55 * mm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), AZUL_CLARO),
        ("TOPPADDING",    (0, 0), (-1, 0),  7),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  1),
        ("TOPPADDING",    (0, 1), (-1, 1),  1),
        ("BOTTOMPADDING", (0, 1), (-1, 1),  7),
        ("LINEAFTER",     (0, 0), (2,  1),  0.4, AZUL),
    ]))
    story.append(t2)
    story.append(Spacer(1, 7))

    # --- RESUMEN GENERAL ---
    story.append(p("Que paso en el catalogo este mes", S["seccion"]))
    story.append(p(data["resumen"], S["body"]))

    note_box(
        "Interaccion real",
        data["destacado"],
        bg=VERDE_CLARO,
        accent=VERDE,
        title_width=46,
    )

    # --- FLUJO COMERCIAL + PAGINAS (dos columnas) ---
    story.append(p("Recorrido comercial registrado", S["seccion"]))

    # Mini tabla de eventos comerciales (izquierda) y paginas (derecha)
    eventos_rows = [
        [p("Accion", S["table_head"]), p("Veces", S["table_head"])],
        [p("Producto visto en detalle", S["table_cell"]), p(fmt_num(data["vio_producto"]),     S["table_cell"])],
        [p("Presentacion seleccionada", S["table_cell"]), p(fmt_num(data["selecciono_tamano"]),S["table_cell"])],
        [p("Producto agregado al carrito", S["table_cell"]),p(fmt_num(data["agrego_al_carrito"]),S["table_cell"])],
        [p("Categoria explorada",        S["table_cell"]), p(fmt_num(data["exploro_categoria"]),S["table_cell"])],
        [p("Pedido solicitado por WhatsApp", S["table_cell"]),p(fmt_num(data["solicito_pedido_whatsapp"]),S["table_cell"])],
    ]
    te = Table(eventos_rows, colWidths=[62 * mm, 20 * mm])
    te.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  VERDE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("BACKGROUND",    (0, 1), (-1, -1), BLANCO),
        ("ROWBACKGROUNDS",(0, 2), (-1, -1), [BLANCO, GRIS_CLARO]),
    ]))

    paginas_rows = [
        [p("Seccion del catalogo", S["table_head"]), p("Vistas", S["table_head"])],
    ]
    for pg in data["paginas"]:
        paginas_rows.append([
            p(pg["pagina"],     S["table_cell"]),
            p(fmt_num(pg["vistas"]), S["table_cell"]),
        ])
    tp = Table(paginas_rows, colWidths=[72 * mm, 18 * mm])
    tp.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  AZUL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("BACKGROUND",    (0, 1), (-1, -1), BLANCO),
        ("ROWBACKGROUNDS",(0, 2), (-1, -1), [BLANCO, AZUL_CLARO]),
    ]))

    # Dos columnas juntas
    dos_col = Table([[te, p("", S["body"]), tp]], colWidths=[82 * mm, 6 * mm, 90 * mm])
    dos_col.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(dos_col)
    story.append(Spacer(1, 5))

    story.append(p(data["flujo_comercial"], S["body"]))

    # --- CANALES Y CIUDADES (dos columnas) ---
    story.append(p("De donde llega la gente", S["seccion"]))

    canales_rows = [
        [p("Canal", S["table_head"]), p("Sesiones", S["table_head"])],
        [p("Redes sociales organicas", S["table_cell"]), p(fmt_num(data["sesiones_social"]), S["table_cell"])],
        [p("Trafico directo (WhatsApp, links)", S["table_cell"]), p(fmt_num(data["sesiones_direct"]), S["table_cell"])],
    ]
    tc = Table(canales_rows, colWidths=[68 * mm, 22 * mm])
    tc.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  VERDE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("BACKGROUND",    (0, 1), (-1, -1), VERDE_CLARO),
    ]))

    ciudad_rows = [[p("Ciudad", S["table_head"]), p("Personas", S["table_head"])]]
    for c in data["ciudades"]:
        ciudad_rows.append([
            p(c["ciudad"],         S["table_cell"]),
            p(fmt_num(c["usuarios"]), S["table_cell"]),
        ])
    tciu = Table(ciudad_rows, colWidths=[62 * mm, 22 * mm])
    tciu.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  AZUL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("GRID",          (0, 0), (-1, -1), 0.25, GRIS_LINEA),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("BACKGROUND",    (0, 1), (-1, -1), BLANCO),
        ("ROWBACKGROUNDS",(0, 2), (-1, -1), [BLANCO, AZUL_CLARO]),
    ]))

    dos_col2 = Table([[tc, p("", S["body"]), tciu]], colWidths=[90 * mm, 6 * mm, 84 * mm])
    dos_col2.setStyle(TableStyle([
        ("VALIGN",          (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",      (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 0),
        ("LEFTPADDING",     (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",    (0, 0), (-1, -1), 0),
    ]))
    story.append(dos_col2)
    story.append(Spacer(1, 4))

    story.append(p(data["canales"], S["body"]))

    # --- RECOMENDACIONES ---
    story.append(p("Que hacer este mes para seguir creciendo", S["seccion"]))
    rec_rows = [[p("Recomendaciones concretas", S["box_title"])]]
    for r in data["recomendaciones"]:
        rec_rows.append([p(f"• {r}", S["box_text"])])
    trec = Table(rec_rows, colWidths=[176 * mm])
    trec.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), AMARILLO_CLARO),
        ("LINEBEFORE",    (0, 0), (0, -1),  3, AMARILLO),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
    ]))
    story.append(trec)
    story.append(Spacer(1, 5))

    # --- CIERRE ---
    note_box(
        "Conclusion del mes",
        data["cierre"],
        bg=VERDE_CLARO,
        accent=VERDE,
        title_width=48,
    )

    footer()

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
