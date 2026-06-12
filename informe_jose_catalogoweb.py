from pathlib import Path
import webbrowser

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

# =========================================================
# INFORME MENSUAL - CATALOGOWEB
# Cliente: Jose - Esencia Real Perfumeria
# Periodo trabajado: 24/05/2026 al 11/06/2026
# Objetivo: retencion, percepcion de valor y lectura humana
# =========================================================

DATA = {

    "cliente": "Jose",
    "negocio": "Esencia Real Perfumeria",
    "periodo": "24/05/2026 al 11/06/2026",
    "dias_periodo": 19,
    "fecha_emision": "11/06/2026",

    # =========================
    # METRICAS PRINCIPALES
    # =========================

    "sesiones": 31,
    "usuarios_unicos": 12,
    "usuarios_nuevos": 12,
    "usuarios_recurrentes": 3,
    "vistas_pagina": 118,
    "eventos_totales": 226,
    "sesiones_interaccion": 20,
    "porcentaje_interaccion": "64,52%",
    "tiempo_promedio_sesion": "38 segundos",
    "tiempo_promedio_usuario_activo": "1 min y 40 s",
    "duracion_media_sesion_audiencia": "3 min y 02 s",
    "vistas_por_sesion": "3,81",
    "vistas_por_usuario_activo": "9,83",
    "eventos_por_sesion": "7,29",
    "sesiones_con_interaccion_por_usuario": "1,67",
    "plataforma": "Web 100%",

    # =========================
    # LECTURA PARA EL CLIENTE
    # =========================

    "analisis_cliente": (
        "Durante el periodo analizado, el catalogo de Esencia Real Perfumeria registro movimiento real: "
        "31 visitas, 12 usuarios activos, 118 vistas de paginas y 226 acciones dentro del sitio. "
        "Lo mas importante no es solo que hayan ingresado, sino que los visitantes navegaron: entraron a la portada, "
        "revisaron categorias, vieron productos especificos, hicieron scroll, iniciaron formularios y tambien hubo "
        "acciones comerciales concretas como agregar un producto al carrito y solicitar un pedido por WhatsApp. "
        "Esto muestra que el catalogo esta cumpliendo su funcion principal: ordenar la vidriera digital, permitir que "
        "los clientes consulten productos y facilitar el contacto desde un solo enlace."
    ),

    "lectura_periodo": (
        "El catalogo no se comporto como una pagina estatica. Los datos muestran recorrido interno y consulta de secciones. "
        "La portada concentro la mayor parte de los accesos, pero tambien hubo movimiento hacia categorias como masculinos, "
        "perfumes de nicho, perfumes de disenador, Ariana Grande, Paris Hilton y Britney Spears. Ademas, se registraron vistas "
        "a productos puntuales, lo que indica que algunas personas avanzaron desde la navegacion general hacia perfumes concretos."
    ),

    "conclusion_cliente": (
        "El balance del periodo es positivo: el catalogo esta vivo, recibe visitas, genera recorrido y permite que los clientes "
        "encuentren informacion sin depender de responder todo manualmente por mensaje. Para potenciarlo aun mas, la clave del proximo "
        "mes es compartirlo con mas frecuencia y dirigir a las personas a categorias o productos especificos."
    ),

    # =========================
    # CANALES DE ADQUISICION
    # =========================

    "fuente_principal": "Trafico Directo",

    "fuentes_detalle": [
        "27 sesiones llegaron por Trafico Directo, el canal principal del catalogo.",
        "El Trafico Directo concentro el 87,1% de las sesiones y 204 acciones registradas dentro del sitio.",
        "9 usuarios nuevos llegaron por enlaces directos compartidos en conversaciones, perfiles, estados o mensajes.",
        "2 usuarios nuevos llegaron desde redes sociales organicas.",
        "1 usuario nuevo llego desde busqueda organica, senal de que el catalogo tambien puede empezar a aparecer por busquedas.",
        "En el canal directo, el tiempo medio de interaccion por usuario activo fue de 2 min y 11 s, un dato muy bueno para un catalogo comercial.",
    ],

    "canales_tabla": [
        {"canal": "Directo", "sesiones": 27, "usuarios_nuevos": 9, "detalle": "Principal fuente de movimiento. Indica links compartidos y accesos desde conversaciones."},
        {"canal": "Redes sociales", "sesiones": 2, "usuarios_nuevos": 2, "detalle": "Personas que llegaron desde actividad organica en redes."},
        {"canal": "Busqueda organica", "sesiones": 2, "usuarios_nuevos": 1, "detalle": "Primeras senales de llegada desde Google u otro buscador."},
        {"canal": "No asignado", "sesiones": 3, "usuarios_nuevos": 0, "detalle": "Trafico que Analytics no pudo clasificar con precision."},
    ],

    # =========================
    # EVENTOS DESTACADOS
    # =========================

    "eventos_destacados": [
        "118 visualizaciones de paginas dentro del catalogo.",
        "31 inicios de sesion registrados durante el periodo.",
        "25 scrolls: usuarios bajaron dentro de las paginas para seguir mirando contenido.",
        "21 eventos de interaccion activa: usuarios permanecieron y navegaron dentro del sitio.",
        "12 primeras visitas registradas.",
        "10 inicios de formulario: visitantes llegaron a una instancia de consulta o carga de datos.",
        "7 visualizaciones de productos especificos.",
        "1 producto agregado al carrito.",
        "1 solicitud de pedido por WhatsApp registrada desde el catalogo.",
    ],

    "eventos_tabla": [
        {"evento": "Vistas de pagina", "cantidad": 118, "lectura": "El catalogo fue consultado y recorrido."},
        {"evento": "Scroll", "cantidad": 25, "lectura": "Los visitantes no solo entraron: bajaron y revisaron contenido."},
        {"evento": "Interaccion activa", "cantidad": 21, "lectura": "Hubo permanencia y uso real dentro del sitio."},
        {"evento": "Inicio de formulario", "cantidad": 10, "lectura": "Varios visitantes llegaron a una accion de consulta."},
        {"evento": "Vio producto", "cantidad": 7, "lectura": "Algunos usuarios avanzaron hacia perfumes concretos."},
        {"evento": "Agrego al carrito", "cantidad": 1, "lectura": "Hubo intencion comercial dentro del catalogo."},
        {"evento": "Pedido por WhatsApp", "cantidad": 1, "lectura": "El catalogo logro llevar al usuario hasta el canal de contacto."},
    ],

    # =========================
    # PAGINAS Y PANTALLAS
    # =========================

    "paginas_principales": [
        {"pagina": "Pagina principal", "ruta": "/", "vistas": 34, "usuarios": 11, "tiempo": "25 s", "lectura": "Fue la entrada y vidriera principal del catalogo."},
        {"pagina": "Panel de productos", "ruta": "/admin/products", "vistas": 29, "usuarios": 2, "tiempo": "2 min 56 s", "lectura": "Movimiento interno de administracion y carga/edicion."},
        {"pagina": "Panel de pedidos", "ruta": "/admin/pedidos", "vistas": 12, "usuarios": 1, "tiempo": "24 s", "lectura": "Revision de pedidos o movimiento administrativo."},
        {"pagina": "Login del panel", "ruta": "/admin/login", "vistas": 9, "usuarios": 2, "tiempo": "52 s", "lectura": "Accesos al area de gestion del catalogo."},
        {"pagina": "Categoria Masculinos", "ruta": "/categoria/masculinos", "vistas": 7, "usuarios": 3, "tiempo": "45 s", "lectura": "Categoria destacada del periodo por cantidad de usuarios."},
        {"pagina": "Categoria Perfumes de Nicho", "ruta": "/categoria/perfumes-de-nicho", "vistas": 5, "usuarios": 2, "tiempo": "22 s", "lectura": "Interes en una categoria de mayor valor percibido."},
        {"pagina": "Inicio", "ruta": "/inicio", "vistas": 5, "usuarios": 1, "tiempo": "1 min 03 s", "lectura": "Recorrido adicional dentro del catalogo."},
        {"pagina": "Categoria Perfumes de Disenador", "ruta": "/categoria/perfumes-de-disenador", "vistas": 3, "usuarios": 2, "tiempo": "3 s", "lectura": "Categoria consultada por mas de un usuario."},
        {"pagina": "Categoria Ariana Grande", "ruta": "/categoria/ariana-grande", "vistas": 2, "usuarios": 1, "tiempo": "15 s", "lectura": "Interes puntual por linea/marca especifica."},
        {"pagina": "Categoria Paris Hilton", "ruta": "/categoria/paris-hilton", "vistas": 2, "usuarios": 1, "tiempo": "6 s", "lectura": "Otra categoria puntual consultada."},
    ],

    "productos_y_paginas_secundarias": [
        "Se registraron accesos a productos individuales como /product/24, /product/33, /product/38, /product/52, /product/86 y /product/89.",
        "El listado general de productos tambien recibio visitas, lo que indica exploracion fuera de la portada.",
        "La categoria Britney Spears tuvo al menos una visita, sumando otra senal de interes por lineas especificas.",
        "La categoria Masculinos fue la categoria publica con mayor cantidad de usuarios activos del periodo.",
        "Perfumes de Nicho y Perfumes de Disenador tambien fueron consultadas, lo que ayuda a detectar intereses para destacar en historias o estados.",
    ],

    "paginas_destino": [
        "23 sesiones comenzaron desde la pagina principal del catalogo.",
        "La portada concentro el 74,19% de los ingresos, funcionando como puerta de entrada principal.",
        "Tambien hubo ingresos directos al panel y a categorias especificas.",
        "1 sesion comenzo directamente en la categoria Perfumes de Disenador, senal de que los enlaces internos pueden compartirse de forma puntual.",
    ],

    # =========================
    # UBICACION Y AUDIENCIA
    # =========================

    "ubicaciones": [
        "Colombia: 5 usuarios activos, con Barranquilla como ciudad principal.",
        "Argentina: 3 usuarios activos, registrados desde Las Varillas.",
        "Tambien se observaron accesos aislados desde Suecia, Estados Unidos y Venezuela.",
        "La lectura comercial mas importante es que el catalogo puede circular fuera de una sola ciudad cuando el enlace se comparte.",
    ],

    "ciudades": [
        {"ciudad": "Barranquilla", "usuarios": 4},
        {"ciudad": "Las Varillas", "usuarios": 3},
        {"ciudad": "Medellin", "usuarios": 1},
        {"ciudad": "Guayana City", "usuarios": 1},
        {"ciudad": "Lulea", "usuarios": 1},
        {"ciudad": "Forest City", "usuarios": 1},
    ],

    # =========================
    # OBSERVACIONES HUMANAS
    # =========================

    "observaciones_positivas": [
        "El catalogo recibio movimiento en varios dias del periodo, no en un unico momento aislado.",
        "La portada funciono como vidriera principal y tuvo alcance sobre casi todos los usuarios activos.",
        "Hay navegacion real hacia categorias y productos, no solo entradas vacias.",
        "El canal directo es fuerte, lo cual suele estar relacionado con enlaces compartidos por WhatsApp, Instagram, estados o mensajes.",
        "La categoria Masculinos y la categoria Perfumes de Nicho aparecen como buenas candidatas para promocionar mas este mes.",
        "La presencia de un pedido por WhatsApp y un producto agregado al carrito muestra que el flujo comercial esta funcionando tecnicamente.",
    ],

    "recomendacion": (
        "Para el proximo mes, la recomendacion principal es compartir el catalogo de forma mas dirigida. En vez de enviar siempre "
        "solo el link general, conviene alternar entre el link de la portada, categorias especificas y productos puntuales. Por ejemplo: "
        "un dia compartir Masculinos, otro dia Perfumes de Nicho, otro dia una linea concreta como Ariana Grande o Paris Hilton. "
        "Eso ayuda a que el cliente no vea el catalogo como un link mas, sino como una vidriera activa que se renueva."
    ),

    "mejora_mes": (
        "Destacar durante el mes 2 o 3 categorias con movimiento real: Masculinos, Perfumes de Nicho y Perfumes de Disenador. "
        "La idea es usarlas en historias, estados de WhatsApp y mensajes a clientes para llevar trafico a secciones concretas del catalogo."
    ),

    "tips_marketing": [
        "Poner el link del catalogo fijo en la biografia de Instagram y tambien en el perfil de WhatsApp Business.",
        "Subir estados con una frase simple: 'Catalogo actualizado - mira precios y modelos aca' junto al link.",
        "Compartir categorias puntuales, no siempre la portada. Ejemplo: 'Te dejo directamente los perfumes masculinos'.",
        "Cuando alguien pregunte precio por mensaje, responder con el link del producto o de la categoria para que pueda seguir mirando opciones.",
        "Elegir 5 productos destacados por semana y moverlos en historias con llamado a la accion: 'pedilo desde el catalogo'.",
        "Mantener fotos, precios y disponibilidad actualizados para que el catalogo sea una herramienta confiable.",
    ],

    "frase_cierre": (
        "El catalogo ya esta funcionando como una vidriera digital consultable. El siguiente paso es darle mas visibilidad para que cada vez "
        "mas personas lo usen como referencia antes de consultar o comprar."
    ),
}

# =========================================================
# ESTILOS
# =========================================================

VERDE = colors.HexColor("#168765")
VERDE_OSCURO = colors.HexColor("#0F5F49")
VERDE_CLARO = colors.HexColor("#E4F5EE")
GRIS_OSCURO = colors.HexColor("#252525")
GRIS_MEDIO = colors.HexColor("#666666")
GRIS_CLARO = colors.HexColor("#F5F3EE")
GRIS_LINEA = colors.HexColor("#D9D9D9")
AZUL_CLARO = colors.HexColor("#EAF1FA")
AZUL = colors.HexColor("#285C8E")
AMARILLO_CLARO = colors.HexColor("#FFF5D8")
AMARILLO = colors.HexColor("#B58110")
BLANCO = colors.white

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
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=13 * mm,
        bottomMargin=13 * mm,
    )

    styles = {
        "marca": ParagraphStyle("marca", fontName="Helvetica-Bold", fontSize=11, textColor=VERDE, leading=14),
        "fecha": ParagraphStyle("fecha", fontName="Helvetica", fontSize=8.5, textColor=GRIS_MEDIO, alignment=TA_RIGHT, leading=11),
        "titulo": ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=21, textColor=GRIS_OSCURO, leading=25),
        "titulo2": ParagraphStyle("titulo2", fontName="Helvetica-Bold", fontSize=18, textColor=GRIS_OSCURO, leading=22),
        "subtitulo": ParagraphStyle("subtitulo", fontName="Helvetica", fontSize=10.5, textColor=GRIS_MEDIO, leading=14),
        "seccion": ParagraphStyle("seccion", fontName="Helvetica-Bold", fontSize=10.5, textColor=VERDE_OSCURO, leading=13, spaceBefore=8, spaceAfter=5),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, textColor=GRIS_OSCURO, leading=14.2, spaceAfter=5),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.2, textColor=GRIS_MEDIO, leading=10.5),
        "metric_num": ParagraphStyle("metric_num", fontName="Helvetica-Bold", fontSize=20, textColor=VERDE, alignment=TA_CENTER, leading=23),
        "metric_lbl": ParagraphStyle("metric_lbl", fontName="Helvetica", fontSize=7.7, textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=9.5),
        "box_title": ParagraphStyle("box_title", fontName="Helvetica-Bold", fontSize=9.7, textColor=GRIS_OSCURO, leading=12.5),
        "box_text": ParagraphStyle("box_text", fontName="Helvetica", fontSize=9.0, textColor=GRIS_OSCURO, leading=13.2),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold", fontSize=8.2, textColor=BLANCO, leading=10),
        "table_cell": ParagraphStyle("table_cell", fontName="Helvetica", fontSize=8.1, textColor=GRIS_OSCURO, leading=10.5),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=7.5, textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=9),
    }

    story = []

    def header():
        t = Table([[
            p("catalogoweb.ar", styles["marca"]),
            p(f"Emitido: {data['fecha_emision']}", styles["fecha"]),
        ]], colWidths=[90 * mm, 90 * mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(HRFlowable(width="100%", thickness=1.3, color=VERDE, spaceAfter=9))

    def footer():
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=0.35, color=GRIS_LINEA, spaceBefore=5, spaceAfter=5))
        story.append(p("Informe mensual de actividad del catalogo - catalogoweb.ar", styles["footer"]))

    def bullet_table(title, items, bg=GRIS_CLARO, accent=VERDE):
        rows = [[p(title, styles["box_title"])]]
        for item in items:
            rows.append([p(f"• {item}", styles["box_text"])])
        table = Table(rows, colWidths=[180 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 5.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 6))

    def note_box(title, text, bg=AZUL_CLARO, accent=AZUL):
        table = Table([[
            p(title, styles["box_title"]),
            p(text, styles["box_text"])
        ]], colWidths=[42 * mm, 136 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 7))

    def simple_table(headers, rows, col_widths):
        data_rows = [[p(h, styles["table_head"]) for h in headers]]
        for row in rows:
            data_rows.append([p(cell, styles["table_cell"]) for cell in row])
        table = Table(data_rows, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), VERDE),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLANCO),
            ("GRID", (0, 0), (-1, -1), 0.3, GRIS_LINEA),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ]))
        story.append(table)
        story.append(Spacer(1, 7))

    # =========================
    # PAGINA 1
    # =========================

    header()
    story.append(p("Informe mensual de actividad", styles["titulo"]))
    story.append(p(f"{data['negocio']} - Periodo: {data['periodo']} ({data['dias_periodo']} dias)", styles["subtitulo"]))
    story.append(Spacer(1, 9))

    metrics = [
        (data["sesiones"], "Visitas / sesiones"),
        (data["usuarios_unicos"], "Usuarios activos"),
        (data["vistas_pagina"], "Vistas de pagina"),
        (data["eventos_totales"], "Acciones registradas"),
    ]
    metric_rows = [
        [p(fmt_num(m[0]), styles["metric_num"]) for m in metrics],
        [p(m[1], styles["metric_lbl"]) for m in metrics],
    ]
    table = Table(metric_rows, colWidths=[45 * mm] * 4)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
        ("LINEAFTER", (0, 0), (2, 1), 0.4, VERDE),
    ]))
    story.append(table)
    story.append(Spacer(1, 8))

    metrics2 = [
        (data["sesiones_interaccion"], "Visitas con interaccion"),
        (data["porcentaje_interaccion"], "Porcentaje de interaccion"),
        (data["vistas_por_sesion"], "Vistas por sesion"),
        (data["usuarios_recurrentes"], "Usuarios recurrentes"),
    ]
    metric_rows2 = [
        [p(fmt_num(m[0]), styles["metric_num"]) for m in metrics2],
        [p(m[1], styles["metric_lbl"]) for m in metrics2],
    ]
    table2 = Table(metric_rows2, colWidths=[45 * mm] * 4)
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ("LINEAFTER", (0, 0), (2, 1), 0.4, AZUL),
    ]))
    story.append(table2)
    story.append(Spacer(1, 8))

    story.append(p("Resumen general", styles["seccion"]))
    story.append(p(data["analisis_cliente"], styles["body"]))

    note_box(
        "Dato importante",
        f"La fuente principal fue {data['fuente_principal']}. Esto indica que el enlace esta circulando por canales donde el negocio ya conversa con sus clientes: WhatsApp, Instagram, estados, mensajes privados o links compartidos.",
        bg=AZUL_CLARO,
        accent=AZUL,
    )

    bullet_table("Actividad destacada dentro del catalogo", data["eventos_destacados"])
    story.append(p("Lectura del periodo", styles["seccion"]))
    story.append(p(data["lectura_periodo"], styles["body"]))

    footer()
    story.append(PageBreak())

    # =========================
    # PAGINA 2
    # =========================

    header()
    story.append(p("Que se consulto dentro del catalogo", styles["titulo2"]))
    story.append(p("Detalle de paginas, categorias y productos con movimiento", styles["subtitulo"]))
    story.append(Spacer(1, 8))

    simple_table(
        ["Seccion", "Vistas", "Usuarios", "Lectura comercial"],
        [[x["pagina"], fmt_num(x["vistas"]), fmt_num(x["usuarios"]), x["lectura"]] for x in data["paginas_principales"][:8]],
        [47 * mm, 20 * mm, 22 * mm, 89 * mm],
    )

    bullet_table("Productos y secciones secundarias observadas", data["productos_y_paginas_secundarias"], bg=GRIS_CLARO, accent=VERDE)
    bullet_table("Paginas de destino", data["paginas_destino"], bg=AZUL_CLARO, accent=AZUL)

    footer()
    story.append(PageBreak())

    # =========================
    # PAGINA 3
    # =========================

    header()
    story.append(p("Eventos con lectura humana", styles["titulo2"]))
    story.append(p("Acciones registradas dentro del catalogo", styles["subtitulo"]))
    story.append(Spacer(1, 8))
    simple_table(
        ["Evento", "Cantidad", "Que indica"],
        [[x["evento"], fmt_num(x["cantidad"]), x["lectura"]] for x in data["eventos_tabla"]],
        [48 * mm, 24 * mm, 106 * mm],
    )
    note_box(
        "Lectura simple",
        "Estos eventos muestran comportamiento real: personas que abrieron paginas, bajaron para seguir mirando, revisaron productos, iniciaron consultas y llegaron hasta acciones comerciales dentro del catalogo.",
        bg=VERDE_CLARO,
        accent=VERDE,
    )

    footer()
    story.append(PageBreak())

    # =========================
    # PAGINA 4
    # =========================

    header()
    story.append(p("Circulacion, oportunidades y recomendaciones", styles["titulo2"]))
    story.append(p(f"{data['negocio']} - Analisis complementario", styles["subtitulo"]))
    story.append(Spacer(1, 8))

    bullet_table("Origen del trafico", data["fuentes_detalle"], bg=AZUL_CLARO, accent=AZUL)

    simple_table(
        ["Canal", "Sesiones", "Usuarios nuevos", "Lectura"],
        [[x["canal"], fmt_num(x["sesiones"]), fmt_num(x["usuarios_nuevos"]), x["detalle"]] for x in data["canales_tabla"]],
        [38 * mm, 24 * mm, 30 * mm, 86 * mm],
    )

    bullet_table("Ubicacion de usuarios", data["ubicaciones"], bg=GRIS_CLARO, accent=VERDE)
    bullet_table("Lo positivo que muestran los datos", data["observaciones_positivas"], bg=VERDE_CLARO, accent=VERDE)

    note_box("Mejora del mes", data["mejora_mes"], bg=VERDE_CLARO, accent=VERDE)
    note_box("Recomendacion", data["recomendacion"], bg=AMARILLO_CLARO, accent=AMARILLO)
    bullet_table("Tips concretos para aprovechar mas el catalogo", data["tips_marketing"], bg=GRIS_CLARO, accent=VERDE)

    note_box("Conclusion", data["frase_cierre"], bg=VERDE_CLARO, accent=VERDE)

    footer()
    doc.build(story)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "informe_jose_esencia_real.pdf"
    build_pdf(DATA, str(output))
    try:
        webbrowser.open(output.resolve().as_uri())
    except Exception:
        pass
