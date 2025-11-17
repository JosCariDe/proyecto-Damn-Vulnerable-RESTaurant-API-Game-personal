# New Parche Proyecto - Damn Vulnerable RESTaurant API Game

Este proyecto contiene el desarrollo completo de parches y análisis de vulnerabilidades para la API vulnerable **Damn Vulnerable RESTaurant**, organizado por niveles de dificultad y tipo de vulnerabilidad según OWASP API Security Top 10.

## Estructura del Proyecto

```
new_parche_proyecto/levels
├── nivel_1/          # API5:2023 - Broken Function Level Authorization (BFLA)
├── nivel_2/          # API1:2023 - Broken Object Level Authorization (BOLA)
├── nivel_3/          # API5:2023 - Broken Function Level Authorization (BFLA)
├── nivel_4/          # API10:2023 - Unsafe Consumption of APIs
├── codigo_referencia/ # API6:2023 - Unrestricted Access to Sensitive Business Flows y API2:2023 - Broken Authentication (Self-Referral)
├── nuevo_nivel/      # API3:2023 - Broken Object Property Level Authorization
└── README.md         # Este archivo
```

## Objetivos del Proyecto

1. **Identificar** vulnerabilidades en una API REST real
2. **Explotar** cada vulnerabilidad con pruebas de concepto (PoC)
3. **Mitigar** aplicando parches de seguridad
4. **Documentar** el proceso completo para aprendizaje

## Inicio Rápido

### Requisitos previos
- Docker y Docker Compose instalados
- Python 3.8+ (para scripts de prueba)
- Burp Suite Community (opcional, para interceptar tráfico)

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/JosCariDe/proyecto-Damn-Vulnerable-RESTaurant-API-Game-personal.git

# Levantar la API vulnerable
docker compose up -d

# Acceder a la documentación
# http://localhost:8091/docs
```

## Niveles o Vulnerabilidades Disponibles

| Vulnerabilidad | Vulnerabilidad | OWASP API Top 10 |
|-------|---------------|------------|------------------|
| 1 | Broken Function Level Authorization (BFLA)|  API5:2023 
| 2 | Broken Object Level Authorization (BOLA) | API1:2023 |
| 3 | Broken Function Level Authorization (BFLA) |   API5:2023 |
| 4 | Unsafe Consumption of APIs |  API10:2023 |
| codigo_referencia |  Unrestricted Access to Sensitive Business Flows y Broken Authentication (Self-Referral) | API6:2023 - API2:2023  |
| new_lvl | Broken Object Property Level Authorization (vulnerabilidad inyectada) |  API3:2023 | 

## Uso

Cada nivel contiene:
- `README.md` - Descripción de la vulnerabilidad o nivel
- `exploit.py` - Script de explotación (PoC)
- `patch.py` - Vulnerabilidad expuesta
- `fix.py` - Solución propuesta

### Workflow recomendado:
1. Lee el README del nivel
2. Explora la API vulnerable
3. Intenta explotar la vulnerabilidad
4. Revisa el exploit de ejemplo
5. Aplica el parche sugerido (ejecutar los comando cp descrito al comienzo de cada README.md)
6. Valida que la vulnerabilidad esté corregida

## Recursos

- [OWASP API Security Project](https://owasp.org/API-Security/)
- [Damn Vulnerable RESTaurant Original](https://github.com/theowni/Damn-Vulnerable-RESTaurant-API-Game)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)

