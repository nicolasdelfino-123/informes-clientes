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
# Cliente: Victor - VJ Parfum & Decants
# Periodo trabajado: 16/05/2026 al 12/06/2026
# Objetivo: retencion, percepcion de valor y lectura humana
# =========================================================

DATA = {

    "cliente": "Victor",
    "negocio": "VJ Parfum & Decants",
    "periodo": "16/05/2026 al 12/06/2026",
    "dias_periodo": 28,
    "fecha_emision": "13/06/2026",

    # =========================
    # METRICAS PRINCIPALES
    # =========================

    "sesiones": 1067,
    "usuarios_unicos": 538,
    "usuarios_nuevos": 545,
    "usuarios_recurrentes": 148,
    "vistas_pagina": 4489,
    "eventos_totales": 10387,
    "sesiones_interaccion": 784,
    "porcentaje_interaccion": "73,48%",
    "tiempo_promedio_sesion": "1 min y 55 s",
    "tiempo_promedio_usuario_activo": "3 min y 49 s",
    "duracion_media_sesion_audiencia": "5 min y 42 s",
    "vistas_por_sesion": "4,21",
    "vistas_por_usuario_activo": "8,34",
    "eventos_por_sesion": "9,73",
    "sesiones_con_interaccion_por_usuario": "1,46",
    "plataforma": "Web 100%",

    # =========================
    # LECTURA PARA EL CLIENTE
    # =========================

    "analisis_cliente": (
        "Durante el periodo analizado, el catalogo de VJ Parfum & Decants registro un movimiento muy fuerte y sostenido: "
        "1.067 sesiones, 538 usuarios activos, 545 usuarios nuevos, 148 usuarios recurrentes, 4.489 vistas de paginas y "
        "10.387 acciones registradas dentro del sitio. Estos numeros muestran que el catalogo no esta funcionando solo como una "
        "pagina de presentacion, sino como una vidriera digital activa: los usuarios entran, recorren categorias, ven productos, "
        "seleccionan tamanos, agregan productos al carrito y llegan hasta el pedido por WhatsApp. Para un catalogo comercial, este "
        "nivel de uso es una señal muy positiva porque combina alcance, navegacion interna e intencion de compra."
    ),

    "lectura_periodo": (
        "El comportamiento del periodo fue muy completo. La portada fue la puerta principal, pero tambien hubo movimiento fuerte hacia "
        "el listado de productos, inicio, perfumes de nicho, fragancias femeninas, perfumes arabes, fragancias masculinas, perfumes de "
        "disenador, mas vendidos, combos y productos individuales. Ademas, se registraron 1.349 eventos de producto visto, 1.049 selecciones "
        "de tamano, 477 agregados al carrito y 76 solicitudes de pedido por WhatsApp. Esto indica que los visitantes no solo miraron: "
        "avanzaron dentro del flujo comercial del catalogo."
    ),

    "conclusion_cliente": (
        "El balance del periodo es excelente: el catalogo esta vivo, recibe trafico constante, concentra usuarios reales de Argentina, "
        "tiene fuerte llegada desde redes sociales y mantiene una tasa alta de interaccion. La pagina ya cumple su funcion central: "
        "ordenar la oferta, reducir consultas repetidas, mostrar productos de forma clara y llevar al cliente desde la navegacion hasta WhatsApp. "
        "El siguiente paso es seguir usandolo como herramienta diaria de venta, compartiendo categorias y productos especificos para multiplicar el recorrido."
    ),

    # =========================
    # CANALES DE ADQUISICION
    # =========================

    "fuente_principal": "Redes sociales organicas",

    "fuentes_detalle": [
        "675 sesiones llegaron desde Redes sociales organicas, el canal principal del catalogo durante el periodo.",
        "Las redes sociales organicas concentraron el 63,26% de las sesiones y 6.932 eventos registrados dentro del sitio.",
        "417 usuarios nuevos llegaron desde redes sociales, señal de que Instagram está empujando trafico real hacia el catalogo.",
        "381 sesiones llegaron por Trafico Directo, con 123 usuarios nuevos y 3.381 eventos registrados.",
        "El Trafico Directo tuvo una tasa de evento clave de sesion de 6,04%, superior al promedio general, lo que indica visitantes con buena intencion.",
        "Tambien hubo 8 sesiones desde Busqueda organica, una señal inicial de aparicion por Google u otros buscadores.",
        "La combinacion de redes sociales y trafico directo es muy buena para un catalogo de perfumes, porque muestra que el link circula en canales donde ya existe conversacion comercial.",
    ],

    "canales_tabla": [
        {"canal": "Redes sociales organicas", "sesiones": 675, "usuarios_nuevos": 417, "detalle": "Principal fuente de movimiento. Indica fuerte circulacion desde Instagram y enlaces compartidos en redes."},
        {"canal": "Directo", "sesiones": 381, "usuarios_nuevos": 123, "detalle": "Accesos desde enlaces enviados por WhatsApp, perfiles, estados, mensajes o clientes que vuelven al link."},
        {"canal": "Busqueda organica", "sesiones": 8, "usuarios_nuevos": 5, "detalle": "Primeras señales de llegada desde buscadores. Todavia es bajo, pero suma presencia digital."},
       
    ],

    # =========================
    # EVENTOS DESTACADOS
    # =========================

    "eventos_destacados": [
        "4.489 visualizaciones de paginas dentro del catalogo.",
        "1.349 eventos de producto visto: los usuarios entraron a perfumes concretos.",
        "1.063 inicios de sesion registrados durante el periodo.",
        "1.049 selecciones de tamano, un dato clave para un negocio de decants.",
        "842 scrolls: los visitantes bajaron dentro de las paginas para seguir mirando contenido.",
        "545 primeras visitas registradas, señal de llegada constante de nuevos usuarios.",
        "477 productos agregados al carrito, una señal comercial muy fuerte dentro del catalogo.",
        "270 eventos de interaccion activa: usuarios permanecieron y siguieron usando el sitio.",
        "137 exploraciones de categoria, mostrando recorrido por secciones del catalogo.",
        "76 solicitudes de pedido por WhatsApp generadas desde el catalogo.",
        "46 clicks adicionales registrados en elementos del sitio.",
        "44 inicios de formulario registrados.",
    ],

    "eventos_tabla": [
        {"evento": "Vistas de pagina", "cantidad": 4489, "lectura": "El catalogo tuvo alto volumen de consulta y recorrido."},
        {"evento": "Vio producto", "cantidad": 1349, "lectura": "Los usuarios avanzaron desde la vidriera hacia perfumes concretos."},
        {"evento": "Selecciono tamano", "cantidad": 1049, "lectura": "Dato muy importante para decants: hubo eleccion activa de presentaciones."},
        {"evento": "Scroll", "cantidad": 842, "lectura": "Los visitantes no solo entraron: bajaron y revisaron contenido."},
        {"evento": "Agrego al carrito", "cantidad": 477, "lectura": "Hubo intencion comercial repetida dentro del catalogo."},
        {"evento": "Exploro categoria", "cantidad": 137, "lectura": "Los usuarios compararon secciones y familias de productos."},
        {"evento": "Pedido por WhatsApp", "cantidad": 76, "lectura": "El catalogo logro llevar usuarios hasta el canal final de contacto."},
        {"evento": "Click", "cantidad": 46, "lectura": "Hubo acciones adicionales sobre elementos del sitio."},
        {"evento": "Inicio de formulario", "cantidad": 44, "lectura": "Varios visitantes llegaron a una instancia de consulta o carga de datos."},
    ],

    # =========================
    # PAGINAS Y PANTALLAS
    # =========================

    "paginas_principales": [
        {"pagina": "Pagina principal", "ruta": "/", "vistas": 950, "usuarios": 398, "tiempo": "13 s", "lectura": "Fue la vidriera principal y concentro el mayor alcance del catalogo."},
        {"pagina": "Listado de productos", "ruta": "/products", "vistas": 460, "usuarios": 187, "tiempo": "1 min 12 s", "lectura": "Mucha gente avanzo a mirar el listado completo de productos."},
        {"pagina": "Inicio", "ruta": "/inicio", "vistas": 263, "usuarios": 117, "tiempo": "52 s", "lectura": "Recorrido importante dentro de la estructura principal del sitio."},
        {"pagina": "Categoria Perfumes de Nicho", "ruta": "/categoria/perfumes-de-nicho", "vistas": 240, "usuarios": 82, "tiempo": "1 min 30 s", "lectura": "Categoria de alto valor percibido con excelente movimiento."},
        {"pagina": "Categoria Fragancias Femeninas", "ruta": "/categoria/fragancias-femeninas", "vistas": 201, "usuarios": 88, "tiempo": "1 min 08 s", "lectura": "Categoria muy consultada y con buena cantidad de usuarios."},
        {"pagina": "Categoria Perfumes Arabes", "ruta": "/categoria/perfumes-arabes", "vistas": 177, "usuarios": 74, "tiempo": "1 min 35 s", "lectura": "Categoria fuerte para seguir impulsando en historias y estados."},
        {"pagina": "Categoria Fragancias Masculinas", "ruta": "/categoria/fragancias-masculinas", "vistas": 176, "usuarios": 88, "tiempo": "1 min 16 s", "lectura": "Interes muy parejo con fragancias femeninas, buen rubro para destacar."},
        {"pagina": "Categoria Perfumes de Disenador", "ruta": "/categoria/perfumes-de-disenador", "vistas": 164, "usuarios": 80, "tiempo": "1 min 42 s", "lectura": "Categoria con tiempo de consulta alto y buen interes."},
        {"pagina": "Panel de productos", "ruta": "/admin/products", "vistas": 147, "usuarios": 7, "tiempo": "15 min 27 s", "lectura": "Movimiento interno de administracion, carga y mantenimiento del catalogo."},
        {"pagina": "Categoria Mas Vendidos", "ruta": "/categoria/mas-vendidos", "vistas": 102, "usuarios": 62, "tiempo": "1 min 02 s", "lectura": "Seccion comercialmente muy valiosa para orientar compras rapidas."},
        {"pagina": "Categoria Combos", "ruta": "/categoria/combos", "vistas": 84, "usuarios": 40, "tiempo": "58 s", "lectura": "Buena oportunidad para empujar promociones y packs."},
        {"pagina": "Panel de pedidos", "ruta": "/admin/pedidos", "vistas": 63, "usuarios": 5, "tiempo": "4 min 38 s", "lectura": "Revision de pedidos y movimiento administrativo."},
        {"pagina": "Producto 270", "ruta": "/product/270", "vistas": 60, "usuarios": 37, "tiempo": "1 min 01 s", "lectura": "Producto individual con fuerte consulta; conviene identificarlo para destacarlo."},
        {"pagina": "Panel de cupones", "ruta": "/admin/coupons", "vistas": 43, "usuarios": 7, "tiempo": "2 min 07 s", "lectura": "Uso de herramienta promocional para acciones comerciales."},
        {"pagina": "Login del panel", "ruta": "/admin/login", "vistas": 36, "usuarios": 8, "tiempo": "2 min 29 s", "lectura": "Accesos al area de gestion del catalogo."},
        {"pagina": "Producto 295", "ruta": "/product/295", "vistas": 29, "usuarios": 22, "tiempo": "18 s", "lectura": "Producto con consulta puntual para revisar y potenciar."},
        {"pagina": "Producto 308", "ruta": "/product/308", "vistas": 28, "usuarios": 19, "tiempo": "1 min 12 s", "lectura": "Producto con buen tiempo de consulta."},
        {"pagina": "Producto 101", "ruta": "/product/101", "vistas": 27, "usuarios": 21, "tiempo": "1 min 09 s", "lectura": "Producto con 4 eventos clave, señal destacada de interes."},
        {"pagina": "Producto 110", "ruta": "/product/110", "vistas": 24, "usuarios": 19, "tiempo": "45 s", "lectura": "Producto con movimiento y evento clave registrado."},
        {"pagina": "Producto 296", "ruta": "/product/296", "vistas": 23, "usuarios": 15, "tiempo": "16 s", "lectura": "Producto consultado por varios usuarios."},
    ],

    "productos_y_paginas_secundarias": [
        "Se registraron accesos destacados a productos individuales como /product/270, /product/295, /product/308, /product/101, /product/110 y /product/296.",
        "Tambien tuvieron movimiento /product/65, /product/298, /product/163, /product/299, /product/97, /product/134, /product/293, /product/74 y /product/116.",
        "El producto /product/101 registro 4 eventos clave, un dato muy bueno para identificar interes comercial.",
        "El producto /product/163 registro 2 eventos clave y buen tiempo de consulta.",
        "Las categorias con mejor señal publica fueron Perfumes de Nicho, Fragancias Femeninas, Perfumes Arabes, Fragancias Masculinas, Perfumes de Disenador, Mas Vendidos y Combos.",
        "La categoria Mas Vendidos recibio 102 vistas y 62 usuarios activos; es una seccion ideal para compartir con clientes indecisos.",
        "La categoria Combos recibio 84 vistas y 40 usuarios activos; puede usarse para promociones, regalos o ventas por pack.",
        "La categoria Fragancias Unisex tambien aparecio con 21 vistas y 13 usuarios activos.",
        "El listado general /products tuvo 460 vistas y 187 usuarios, lo que muestra que muchas personas prefieren explorar la oferta completa.",
    ],

    "paginas_destino": [
        "626 sesiones comenzaron desde la pagina principal del catalogo, que concentro el 58,67% de las entradas.",
        "La portada genero 52 eventos clave desde pagina de destino, confirmando que funciona como entrada comercial principal.",
        "142 sesiones comenzaron desde /inicio, con 93 usuarios activos y 7 eventos clave.",
        "24 sesiones comenzaron directamente desde /products, señal de que el listado completo tambien se comparte o queda guardado.",
        "18 sesiones comenzaron desde /categoria/perfumes-de-nicho, una categoria con buen potencial para promocionar de forma directa.",
        "Tambien hubo entradas directas a productos como /product/299, /product/298, /product/295 y /product/296.",
        "Esto es positivo porque indica que el catalogo no depende solamente de la portada: tambien se puede usar para enviar links puntuales a productos o categorias.",
    ],

    # =========================
    # UBICACION Y AUDIENCIA
    # =========================

    "ubicaciones": [
        "Argentina concentro 504 usuarios activos, el 93,68% del total, con 511 usuarios nuevos y 10.193 eventos.",
        "Posadas fue la ciudad principal con 296 usuarios activos, una señal muy fuerte de alcance local real.",
        "Buenos Aires aporto 79 usuarios activos, Garupa 39, Corrientes 25, Cordoba 9, Eldorado 9 y Rosario 8.",
        "La lectura comercial principal es que el catalogo esta impactando sobre todo en Argentina y especialmente en la zona de influencia del negocio.",
    ],

    "ciudades": [
        {"ciudad": "Posadas", "usuarios": 296},
        {"ciudad": "Buenos Aires", "usuarios": 79},
        {"ciudad": "Garupa", "usuarios": 39},
        {"ciudad": "Corrientes", "usuarios": 25},
        {"ciudad": "Cordoba", "usuarios": 9},
        {"ciudad": "Eldorado", "usuarios": 9},
        {"ciudad": "Rosario", "usuarios": 8},
    ],

    # =========================
    # OBSERVACIONES HUMANAS
    # =========================

    "observaciones_positivas": [
        "El catalogo registro movimiento todos los dias del periodo, con picos fuertes de actividad y uso sostenido.",
        "538 usuarios activos y 545 usuarios nuevos muestran llegada real de publico, no solo visitas internas.",
        "La tasa de interaccion del 73,48% es muy buena: gran parte de las sesiones tuvo comportamiento activo.",
        "El promedio de 4,21 vistas por sesion muestra que los visitantes recorren mas de una pantalla antes de salir.",
        "Las 477 acciones de agregar al carrito son una señal fuerte de intencion comercial.",
        "Las 76 solicitudes de pedido por WhatsApp muestran que el flujo final del catalogo esta funcionando.",
        "La seleccion de tamano tuvo 1.049 eventos, clave para un negocio de decants porque indica comparacion y decision sobre presentaciones.",
        "Las redes sociales organicas estan funcionando muy bien como motor de trafico hacia el catalogo.",
        "El trafico directo tambien es alto, lo que suele indicar clientes que vuelven al link o lo reciben por WhatsApp, estados o mensajes.",
        "Las categorias principales tienen buen reparto de interes: nicho, femenino, arabes, masculino, disenador, mas vendidos y combos.",
        "Posadas aparece como ciudad principal, lo que confirma llegada local relevante para el negocio.",
    ],

    "recomendacion": (
        "Para el proximo mes, la recomendacion principal es usar el catalogo como herramienta activa de venta todos los dias. En vez de compartir "
        "siempre solo la portada, conviene alternar links directos a categorias y productos: un dia Mas Vendidos, otro dia Combos, otro dia Perfumes "
        "de Nicho, otro dia Fragancias Femeninas, otro dia Perfumes Arabes. Tambien conviene identificar los productos con mas visitas, como /product/270, "
        "/product/101, /product/308 y /product/295, para destacarlos en historias o estados con una frase directa y el link al producto."
    ),

    "mejora_mes": (
        "Destacar durante el proximo mes 4 bloques con movimiento real: Mas Vendidos, Combos, Perfumes de Nicho y Perfumes Arabes. "
        "La idea es que cada bloque tenga publicaciones o estados propios, usando el catalogo como destino final. Tambien conviene revisar los productos "
        "con mas vistas y ponerles foto, precio y descripcion bien prolijos, porque ya demostraron recibir atencion."
    ),

    "tips_marketing": [
        "Mantener el link del catalogo fijo en la biografia de Instagram y en el perfil de WhatsApp Business.",
        "Compartir una categoria distinta por dia en historias o estados: Mas Vendidos, Combos, Nicho, Arabes, Femeninos y Masculinos.",
        "Cuando una persona pregunte por un perfume, responder con el link directo del producto o de la categoria para que pueda seguir mirando opciones.",
        "Crear historias con llamados simples: 'Mira los mas vendidos aca', 'Elegis el tamano y pedis por WhatsApp', 'Catalogo actualizado'.",
        "Aprovechar los productos mas vistos para armar publicaciones: /product/270, /product/101, /product/308, /product/295, /product/110 y /product/163.",
        "Usar la categoria Combos para fechas especiales, regalos o promociones por pack.",
        "Revisar cada semana que precios, fotos y disponibilidad esten actualizados para sostener confianza.",
        "Enviar el catalogo a clientes recurrentes cuando haya novedades, no solo a clientes nuevos.",
    ],

    "frase_cierre": (
        "El catalogo de VJ Parfum & Decants ya funciona como una vidriera digital fuerte, con trafico real, recorrido interno, carritos y pedidos por WhatsApp. "
        "Los datos muestran que la herramienta esta siendo usada por los clientes y que puede seguir creciendo si se comparte de forma constante y dirigida."
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

    note_box(
    "Guia para interpretar este informe",
    """
    <b>Antes de analizar los numeros, te explico que significa cada indicador:</b>

    <br/><br/>

    <b>Visitas / Sesiones</b><br/>
    Muestran cuántas veces fue utilizado el catálogo durante el período analizado. Cada vez que alguien entra para mirar productos, consultar precios o volver a revisar información, se registra una nueva visita. Este dato permite medir el nivel de actividad y movimiento que tuvo la página.

    <br/><br/>

    <b>Usuarios activos</b><br/>
    Representan la cantidad de personas que utilizaron el catálogo durante el período analizado. Este indicador permite conocer cuántos potenciales clientes alcanzó la página, mientras que las visitas muestran cuántas veces esos usuarios regresaron o continuaron navegando.

    <br/><br/>

    <p>
    Durante el período analizado, más de 500 personas utilizaron el catálogo y se registraron más de 1.000 visitas, lo que indica que muchos usuarios regresaron a consultar productos en más de una ocasión.
    </p>

    <br/><br/>

    <b>Vistas de pagina</b><br/>
    Es la cantidad total de paginas consultadas dentro del catalogo. Incluye portada, categorias, productos y otras secciones.

    <br/><br/>

    <b>Acciones registradas</b><br/>
    Son todos los movimientos detectados por Analytics dentro del catalogo: abrir paginas, ver productos, desplazarse con scroll, seleccionar variantes, agregar productos al carrito o solicitar pedidos.

    <br/><br/>

    <b>Visitas con interaccion</b><br/>
    Son visitas donde el usuario realmente utilizo el catalogo. No solo entro y salio, sino que navego, exploro contenido o realizo alguna accion.

    <br/><br/>

    <b>Porcentaje de interaccion</b><br/>
    Indica que porcentaje de las visitas generaron actividad real dentro del sitio. Cuanto mayor sea este numero, mayor es el interes que despierta el catalogo en los visitantes.

    <br/><br/>

    <b>Vistas por sesion</b><br/>
    Muestra cuantas paginas recorre en promedio cada visitante durante una visita. Un valor elevado suele indicar interes por explorar categorias y productos.

    <br/><br/>

    <b>Usuarios recurrentes</b><br/>
    Son personas que ya habian visitado el catalogo anteriormente y decidieron volver. Esto suele ser una muy buena señal porque indica que utilizan la pagina como referencia para consultar productos, precios o disponibilidad.

    <br/><br/>

    <b>¿Como interpretar el informe?</b><br/>
    Ningun numero por si solo determina el resultado de una pagina. Lo importante es observar el conjunto de indicadores para entender como las personas utilizan el catalogo.

    <br/><br/>

    Cuando vemos usuarios recurrentes, multiples paginas vistas por visita, exploracion de categorias, consultas de productos y acciones comerciales registradas, podemos concluir que el catalogo esta siendo utilizado activamente y esta cumpliendo su funcion como vidriera digital disponible las 24 horas.
    """,
    bg=AMARILLO_CLARO,
    accent=AMARILLO,
)




    

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
    output = output_dir / "informe_victor_vj_parfum_decants.pdf"
    build_pdf(DATA, str(output))
    try:
        webbrowser.open(output.resolve().as_uri())
    except Exception:
        pass
