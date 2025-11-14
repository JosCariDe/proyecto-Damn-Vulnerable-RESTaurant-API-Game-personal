# Level 0 – Technology Details Exposed via HTTP Header

## 📌 Descripción de la Vulnerabilidad

El endpoint `/healthcheck` expone información sensible del servidor mediante el header:

```python
response.headers["X-Powered-By"] = "Python 3.10, FastAPI ^0.103.0"
```

Esto revela detalles internos como:
* Lenguaje utilizado
* Versión de Python
* Framework FastAPI
* Versión del framework

Este tipo de información permite a un atacante buscar exploits específicos y conocer el stack tecnológico del servidor, lo que facilita ataques dirigidos. La vulnerabilidad se encuentra en:

```
app/apis/healthcheck/service.py
```

##  Código Vulnerable

```python
from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/healthcheck")
def healthcheck(response: Response):
    response.headers["X-Powered-By"] = "Python 3.10, FastAPI ^0.103.0"
    return {"ok": True}
```

## 🔍 Cómo Explotarla

Un atacante puede descubrir la tecnología interna del servidor usando herramientas básicas como `curl` desde Kali Linux.

### ✔️ Obtener solo los headers

```bash
curl -I http://localhost:8091/healthcheck
```

Salida que se obtuvo:

```
HTTP/1.1 405 Method Not Allowed
date: Fri, 14 Nov 2025 01:31:29 GMT
server: uvicorn
allow: GET
content-length: 31
content-type: application/json

```

### ✔️ Ver la comunicación HTTP completa

```bash
curl -v http://localhost:8091/healthcheck
```

Salida que se obtuvo:

```
* Host localhost:8091 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8091...
* Connected to localhost (::1) port 8091
* using HTTP/1.x
> GET /healthcheck HTTP/1.1
> Host: localhost:8091
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< date: Fri, 14 Nov 2025 01:34:08 GMT
< server: uvicorn
< content-length: 11
< content-type: application/json
< x-powered-by: Python 3.10, FastAPI ^0.103.0
< 
* Connection #0 to host localhost left intact
{"ok":true}            

```

## 🛠️ Solución

Eliminar por completo el header que expone la información.

### ❌ Código vulnerable

```python
response.headers["X-Powered-By"] = "Python 3.10, FastAPI ^0.103.0"
```

### Código corregido

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthcheck")
def healthcheck():
    return {"ok": True}
```

## Validación del Fix

Ejecutar nuevamente:

```bash
curl -I http://localhost:8091/healthcheck
```

Resultado esperado:
* Ya no debe aparecer el header `X-Powered-By`.

## Conclusión

La exposición de tecnología mediante headers debilita la seguridad del servidor al permitir que un atacante conozca versiones y frameworks utilizados. Eliminar este header reduce la superficie de ataque y previene fugas de información innecesarias.