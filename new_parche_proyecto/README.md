# Damn Vulnerable RESTaurant API Game (DVRAPI)

Este repositorio contiene el código, documentación, pruebas, parches y extensiones para el proyecto de análisis y explotación de vulnerabilidades en la API DRMAPI. Está basado en la aplicación vulnerable de seguridad web y API construida en Python con FastAPI y PostgreSQL.

---

## Estructura del Repositorio

### docs/
Contiene la documentación técnica del proyecto:

- `INFORME_FINAL.md`: El informe completo del proyecto con análisis de vulnerabilidades, pruebas, soluciones y conclusiones.
- `INSTALACION.md`: Guía paso a paso para instalar y configurar la API vulnerable en ambiente local utilizando Docker.
- `VULNERABILIDADES.md`: Descripción detallada de cada vulnerabilidad analizada, incluyendo la nueva descubierta o creada para el proyecto.
- `REFERENCIAS.md`: Bibliografía y fuentes utilizadas, formateadas en APA o IEEE.

### scripts/
Scripts en Python para automatizar la explotación de vulnerabilidades y pruebas:

- `exploit_bola.py`: Script que demuestra la vulnerabilidad de Broken Object Level Authorization (BOLA).
- `exploit_sqli.py`: Script para probar inyección SQL en endpoints vulnerables.
- `exploit_auth.py`: Scripts para probar bypass o fallos en autenticación.
- `exploit_custom.py`: Script para explotar la nueva vulnerabilidad descubierta o creada.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar los scripts Python.

### poc/
Pruebas de concepto y evidencias obtenidas:

- `postman_collection.json`: Colección configurada para Postman con pruebas y endpoints.
- `burp_requests.txt`: Requests capturadas y preparadas para usar en Burp Suite.
- `screenshots/`: Capturas de pantalla de resultados de pruebas, exploits y validaciones.
  - Ejemplo: `bola_exploit.png`, `sqli_bypass.png`, etc.

### patches/
Parchea el código para remediar las vulnerabilidades detectadas:

- `fix_bola.py`: Correcciones para arreglar Broken Object Level Authorization.
- `fix_sqli.py`: Parches para proteger contra inyección SQL.
- `fix_auth.py`: Mejoras y correcciones para el sistema de autenticación.
- `fix_custom.py`: Corrección implementada para la vulnerabilidad nueva creada.

### levels/
Extensiones para agregar nuevos niveles o retos de vulnerabilidad al juego DVRAPI:

- `level_7_custom.py`: Nuevo nivel que introduce una vulnerabilidad de Mass Assignment para explorar.
- `test_level_7.py`: Tests automatizados para validar la resolución del nivel 7.
- `README_LEVEL7.md`: Documentación específica del nivel 7, cómo explotarlo y resolverlo.

---

## Cómo usar este repositorio

1. Consulta la documentación en `docs/` para entender el contexto y el marco teórico.
2. Configura el entorno según `docs/INSTALACION.md` para levantar la API vulnerable.
3. Usa los scripts de `scripts/` para ejecutar ataques de prueba.
4. Visualiza y valida las pruebas y capturas en `poc/`.
5. Aplica los parches desde `patches/` para corregir las vulnerabilidades.
6. Explora y resuelve nuevos retos usando los niveles en `levels/`.
7. Consulta el informe final y referencias para completar el marco académico del proyecto.

---

## Licencia

Este proyecto está bajo la licencia GPL v3 - vea el archivo [LICENSE](LICENSE) para más detalles.

---

## Contacto

Para dudas o sugerencias, favor de contactarme por correo o abrir un issue en este repositorio.

---

¡Gracias por tu interés en seguridad de APIs y Happy Hacking!  
