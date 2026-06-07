from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

DATA = {

    "cliente": "Ayman",
    "negocio": "Bellaroma",
    "periodo": "09/05/2026 al 05/06/2026",
    "fecha_emision": "06/06/2026",

    # =========================
    # MÉTRICAS PRINCIPALES
    # =========================

    "sesiones": 102,
    "usuarios_unicos": 69,
    "usuarios_nuevos": 69,
    "vistas_pagina": 279,
    "eventos_totales": 708,
    "tiempo_promedio": "41 segundos",
    "sesiones_interaccion": 69,

    # =========================
    # CANALES DE ADQUISICIÓN
    # =========================

    "fuente_principal": "Tráfico Directo",

    "fuentes_detalle": [
        "58 usuarios llegaron directamente al catálogo (84% del tráfico).",
        "10 usuarios llegaron desde redes sociales orgánicas.",
        "1 usuario llegó mediante referencias externas.",
        "La mayor parte del tráfico proviene de enlaces compartidos por Instagram, WhatsApp y mensajes directos.",
    ],

    # =========================
    # EVENTOS DESTACADOS
    # =========================

    "eventos_destacados": [
        "279 visualizaciones de páginas dentro del catálogo.",
        "113 desplazamientos (scroll) registrados en distintas páginas.",
        "69 primeras visitas registradas durante el período.",
        "69 sesiones con interacción activa de usuarios.",
        "38 exploraciones de categorías de productos.",
        "20 visualizaciones de productos específicos.",
        "9 inicios de formularios dentro del sitio.",
        "6 clics registrados sobre elementos interactivos.",
        "2 productos agregados al carrito.",
    ],

    # =========================
    # CATEGORÍAS Y PÁGINAS
    # =========================

    "paginas_pantallas": [
        "Página principal del catálogo.",
        "Catálogo general de productos.",
        "Categoría Perfumes Árabes.",
        "Categoría Perfumes Árabes Hombre.",
        "Categoría Perfumes Árabes Mujer.",
        "Categoría Perfumes Tradicionales.",
        "Productos individuales consultados por visitantes.",
    ],

    # =========================
    # PÁGINAS DE DESTINO
    # =========================

    "paginas_destino": [
        "89 sesiones comenzaron desde la página principal.",
        "Ingresos directos hacia categorías específicas.",
        "Ingresos directos hacia productos individuales.",
        "Acceso desde enlaces compartidos en redes y mensajería.",
    ],

    # =========================
    # COMPORTAMIENTO OBSERVADO
    # =========================

    "resumen_tiempo_real": [
        "Los visitantes recorrieron distintas categorías del catálogo.",
        "Se registró navegación entre productos específicos.",
        "La actividad no se concentró únicamente en la portada.",
        "Hubo exploración de categorías masculinas, femeninas y tradicionales.",
        "Los usuarios interactuaron con múltiples secciones del catálogo.",
    ],

    # =========================
    # TEXTO PRINCIPAL
    # =========================

    "analisis_cliente": (
        "Durante los últimos 28 días el catálogo registró actividad constante y movimiento real de usuarios. "
        "Se contabilizaron más de 100 sesiones, 69 visitantes únicos y más de 700 acciones realizadas dentro del sitio. "
        "Los usuarios no se limitaron a ingresar y salir, sino que recorrieron categorías, visualizaron productos "
        "específicos e interactuaron con distintas secciones del catálogo. "
        "Además, una gran parte del tráfico llegó de forma directa, lo que indica que el enlace está siendo compartido "
        "y consultado a través de Instagram, WhatsApp y otros canales de contacto."
    ),

    # =========================
    # RECOMENDACIÓN
    # =========================

    "recomendacion": (
        "La recomendación para este mes es continuar compartiendo el catálogo de forma constante en historias, "
        "estados de WhatsApp, publicaciones y conversaciones con clientes. "
        "Los datos muestran que las personas están explorando categorías y productos, por lo que mantener visible "
        "el enlace ayuda a aumentar las oportunidades de consulta y fortalece la presencia digital del negocio."
    ),

    # =========================
    # MEJORA DEL MES
    # =========================

    "mejora_mes": (
        "Seguimiento mensual de categorías y productos más consultados para detectar patrones de interés "
        "y mejorar la visibilidad de los productos destacados."
    ),

}

VERDE = colors.HexColor("#168765")
VERDE_CLARO = colors.HexColor("#E4F5EE")
GRIS_OSCURO = colors.HexColor("#252525")
GRIS_MEDIO = colors.HexColor("#666666")
GRIS_CLARO = colors.HexColor("#F5F3EE")
AZUL_CLARO = colors.HexColor("#EAF1FA")
AZUL = colors.HexColor("#285C8E")
BLANCO = colors.white

W, H = A4


def fmt_num(n):
    if isinstance(n, int):
        return f"{n:,}".replace(",", ".")
    return str(n)


def build_pdf(data, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )

    styles = {
        "marca": ParagraphStyle(
            "marca", fontName="Helvetica-Bold", fontSize=11,
            textColor=VERDE, leading=14
        ),
        "fecha": ParagraphStyle(
            "fecha", fontName="Helvetica", fontSize=9,
            textColor=GRIS_MEDIO, alignment=TA_RIGHT, leading=12
        ),
        "titulo": ParagraphStyle(
            "titulo", fontName="Helvetica-Bold", fontSize=22,
            textColor=GRIS_OSCURO, leading=26
        ),
        "subtitulo": ParagraphStyle(
            "subtitulo", fontName="Helvetica", fontSize=11,
            textColor=GRIS_MEDIO, leading=15
        ),
        "seccion": ParagraphStyle(
            "seccion", fontName="Helvetica-Bold", fontSize=10,
            textColor=VERDE, leading=13, spaceBefore=10, spaceAfter=5
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=10,
            textColor=GRIS_OSCURO, leading=15, spaceAfter=5
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=8.5,
            textColor=GRIS_MEDIO, leading=11
        ),
        "metric_num": ParagraphStyle(
            "metric_num", fontName="Helvetica-Bold", fontSize=21,
            textColor=VERDE, alignment=TA_CENTER, leading=24
        ),
        "metric_lbl": ParagraphStyle(
            "metric_lbl", fontName="Helvetica", fontSize=8,
            textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=10
        ),
        "box_title": ParagraphStyle(
            "box_title", fontName="Helvetica-Bold", fontSize=10,
            textColor=GRIS_OSCURO, leading=13
        ),
        "box_text": ParagraphStyle(
            "box_text", fontName="Helvetica", fontSize=9.5,
            textColor=GRIS_OSCURO, leading=14
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Helvetica", fontSize=8,
            textColor=GRIS_MEDIO, alignment=TA_CENTER, leading=10
        ),
    }

    story = []

    def header():
        t = Table([[
            Paragraph("catalogoweb.ar", styles["marca"]),
            Paragraph(f"Emitido: {data['fecha_emision']}", styles["fecha"]),
        ]], colWidths=[90 * mm, 82 * mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(HRFlowable(width="100%", thickness=1.4, color=VERDE, spaceAfter=10))

    def footer():
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=0.4, color=GRIS_MEDIO, spaceBefore=6, spaceAfter=6))
        story.append(Paragraph(
            "Informe mensual de actividad del catálogo - catalogoweb.ar",
            styles["footer"]
        ))

    def bullet_table(title, items, bg=GRIS_CLARO, accent=VERDE):
        rows = [[Paragraph(title, styles["box_title"])]]
        for item in items:
            rows.append([Paragraph(f"• {item}", styles["box_text"])])
        table = Table(rows, colWidths=[172 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ]))
        story.append(table)
        story.append(Spacer(1, 7))

    header()

    story.append(Paragraph("Informe mensual de actividad", styles["titulo"]))
    story.append(Paragraph(f"{data['negocio']} · {data['periodo']}", styles["subtitulo"]))
    story.append(Spacer(1, 10))

    metrics = [
        (data["sesiones"], "Visitas / sesiones"),
        (data["sesiones_interaccion"], "Visitas con interacción"),
        (data["vistas_pagina"], "Vistas de página"),
        (data["eventos_totales"], "Acciones registradas"),
    ]

    metric_rows = [
        [Paragraph(fmt_num(m[0]), styles["metric_num"]) for m in metrics],
        [Paragraph(m[1], styles["metric_lbl"]) for m in metrics],
    ]

    table = Table(metric_rows, colWidths=[43 * mm] * 4)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
        ("LINEAFTER", (0, 0), (2, 1), 0.4, VERDE),
    ]))
    story.append(table)
    story.append(Spacer(1, 9))

    story.append(Paragraph("Resumen general", styles["seccion"]))
    story.append(Paragraph(data["analisis_cliente"], styles["body"]))

    destaque = Table([[
        Paragraph("<b>Dato importante:</b>", styles["box_title"]),
        Paragraph(
            f"La fuente principal fue <b>{data['fuente_principal']}</b>. "
            "Esto indica que el enlace está circulando por canales donde el negocio ya conversa "
            "con sus clientes: Instagram, WhatsApp, estados, mensajes privados o links compartidos.",
            styles["box_text"]
        )
    ]], colWidths=[38 * mm, 132 * mm])
    destaque.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AZUL),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(destaque)
    story.append(Spacer(1, 7))

    bullet_table("Actividad detectada dentro del catálogo", data["eventos_destacados"])
    bullet_table("Páginas y secciones consultadas", data["paginas_pantallas"])

    story.append(Paragraph("Lectura del período", styles["seccion"]))
    story.append(Paragraph(
        "Los datos muestran que el catálogo no está funcionando solamente como una portada estática. "
        "Hay navegación interna, visualización de productos y recorrido por distintas secciones. "
        "Esto es positivo porque significa que las personas que ingresan tienen algún nivel de interés "
        "y están usando el catálogo para consultar información.",
        styles["body"]
    ))

    story.append(Spacer(1, 8))

    story.append(Paragraph("Detalle de circulación y oportunidades", styles["titulo"]))
    story.append(Paragraph(f"{data['negocio']} · análisis complementario", styles["subtitulo"]))
    story.append(Spacer(1, 10))

    bullet_table("Origen del tráfico", data["fuentes_detalle"], bg=AZUL_CLARO, accent=AZUL)
    bullet_table("Páginas de destino observadas", data["paginas_destino"])
    bullet_table("Resumen en tiempo real / comportamiento", data["resumen_tiempo_real"])

    story.append(Paragraph("Interpretación comercial", styles["seccion"]))
    story.append(Paragraph(
        "El objetivo del catálogo no es solamente recibir visitas, sino ayudar a que más personas "
        "puedan ver productos, consultar precios, recorrer categorías y tener un canal más ordenado "
        "para decidir qué pedir. Por eso, cada visita y cada interacción dentro del sitio suma: "
        "muestra que el catálogo está disponible, circulando y acompañando el proceso de consulta.",
        styles["body"]
    ))

    mejora = Table([[
        Paragraph("Mejora / seguimiento del mes", styles["box_title"]),
        Paragraph(data["mejora_mes"], styles["box_text"])
    ]], colWidths=[50 * mm, 120 * mm])
    mejora.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, VERDE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(mejora)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Recomendación para el próximo mes", styles["seccion"]))
    story.append(Paragraph(data["recomendacion"], styles["body"]))

    story.append(Spacer(1, 8))
    cierre = Table([[
        Paragraph(
            "Conclusión",
            styles["box_title"]
        ),
        Paragraph(
            "El catálogo está generando movimiento real. La recomendación es mantenerlo visible "
            "y seguir compartiéndolo de forma constante para aumentar el volumen de consultas.",
            styles["box_text"]
        )
    ]], colWidths=[35 * mm, 135 * mm])
    cierre.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_CLARO),
        ("LINEBEFORE", (0, 0), (0, -1), 3, VERDE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(cierre)

    footer()
    doc.build(story)
    print(f"PDF generado: {output_path}")


if __name__ == "__main__":
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "informe.pdf"
    build_pdf(DATA, str(output))
