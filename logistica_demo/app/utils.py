import re
from functools import wraps
from flask import abort, request
from flask_login import current_user
from urllib.parse import urlparse, urljoin

def role_required(role):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def roles_accepted(*roles):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def parsear_mensaje(texto):
    resultado = {'dia': None, 'cliente': None, 'productos': [], 'lugar_entrega': None, 'comentario': None}
    texto = texto.strip()
    match_dia = re.search('[📅]?\\s*[Dd][ií]a[:\\s]+(.+?)(?:\\n|$)', texto)
    if match_dia:
        resultado['dia'] = match_dia.group(1).strip()
    match_cliente = re.search('[👤]?\\s*[Cc]liente[:\\s]+(.+?)(?:\\n|$)', texto)
    if match_cliente:
        resultado['cliente'] = match_cliente.group(1).strip()
    match_productos = re.search('[📦]?\\s*[Pp]roductos?[:\\s]*\\n(.*?)(?=\\n[📍]|\\n[Cc]omentario|\\n[Ll]ugar|$)', texto, re.DOTALL)
    if match_productos:
        lineas = match_productos.group(1).strip().split('\n')
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            match_prod = re.match('^(\\d+(?:[.,]\\d+)?)\\s*([a-zA-Z]+)?\\s*(?:de\\s+)?(.+)$', linea, re.IGNORECASE)
            if match_prod:
                resultado['productos'].append({'cantidad': float(match_prod.group(1).replace(',', '.')), 'unidad': match_prod.group(2) or 'unidades', 'nombre': match_prod.group(3).strip()})
            else:
                resultado['productos'].append({'cantidad': 1, 'unidad': 'unidades', 'nombre': linea})
    match_lugar = re.search('[📍]?\\s*[Ll]ugar\\s*(?:de\\s*)?[Ee]ntrega[:\\s]+(.+?)(?:\\n|$)', texto)
    if match_lugar:
        resultado['lugar_entrega'] = match_lugar.group(1).strip()
    match_comentario = re.search('[Cc]omentario[:\\s]+(.+?)(?:\\n|$)', texto, re.DOTALL)
    if match_comentario:
        resultado['comentario'] = match_comentario.group(1).strip()
    return resultado

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def escape_like_pattern(text):
    if not text:
        return text
    return text.replace('%', '\\%').replace('_', '\\_')

def is_safe_filename(filename):
    return bool(re.match('^[a-f0-9]{32}\\.(csv|CSV)$', filename))