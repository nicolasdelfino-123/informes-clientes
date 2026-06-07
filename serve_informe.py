#!/usr/bin/env python3
"""
Genera el PDF usando `informe.build_pdf` y sirve la carpeta `outputs/`
para que puedas abrir `http://localhost:8000/informe.pdf` en el navegador.

Uso:
  python serve_informe.py      # genera y sirve en el puerto 8000 y abre el navegador
  python serve_informe.py --port 9000 --no-open
"""
import os
import sys
import argparse
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler
import socketserver
from functools import partial

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(HERE, "outputs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "informe.pdf")


def generate_pdf():
    try:
        # import local module
        from informe import build_pdf, DATA
    except Exception as e:
        print("Error al importar 'informe'. Asegurate de ejecutar desde la carpeta del proyecto.")
        raise

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        build_pdf(DATA, OUTPUT_FILE)
    except Exception as e:
        # Si falla por dependencia, mostrar instrucción útil
        print("Error generando el PDF:", e)
        print("Si falta 'reportlab', instálalo con: pip install reportlab")
        raise


def serve(directory, port):
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    with socketserver.TCPServer(("", port), handler) as httpd:
        sa = httpd.socket.getsockname()
        print(f"Sirviendo {directory} en http://{sa[0] if sa[0] else 'localhost'}:{sa[1]}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Interrumpido. Cerrando servidor...")


def main():
    parser = argparse.ArgumentParser(description="Generar y servir el informe PDF localmente")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Puerto HTTP (default: 8000)")
    parser.add_argument("--no-open", action="store_true", help="No abrir el navegador automáticamente")
    args = parser.parse_args()

    try:
        generate_pdf()
    except Exception:
        print("No se pudo generar el PDF. Revisa el error anterior.")
        sys.exit(1)

    # Start server in a background thread
    thread = threading.Thread(target=serve, args=(OUTPUT_DIR, args.port), daemon=True)
    thread.start()

    url = f"http://localhost:{args.port}/{os.path.basename(OUTPUT_FILE)}"
    # Esperar un momento para que el servidor esté listo
    time.sleep(0.4)
    if not args.no_open:
        try:
            webbrowser.open(url)
            print(f"Abriendo navegador en {url}")
        except Exception:
            print(f"Abre manualmente: {url}")
    else:
        print(f"PDF disponible en: {url}")

    try:
        # Mantener el hilo principal vivo mientras el servidor corre
        while thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Saliendo...")


if __name__ == "__main__":
    main()
