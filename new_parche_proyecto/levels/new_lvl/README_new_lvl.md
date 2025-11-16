# Ejecutar script para ver la vulnerabilidad 
python3 new_parche_proyecto/levels/new_lvl/scripts/exploit_new_lvl.py

# Hacer Parche (Inyectar Vulnerabilidad)
sudo cp new_parche_proyecto/levels/new_lvl/unpatch/reset_password_service.py app/apis/auth/services/reset_password_service.py  

# Ejecutar script de nuevo para verificar que se inyectó bien (cambiar el username y phone si da error en crear users) 
python3 new_parche_proyecto/levels/new_lvl/scripts/exploit_new_lvl.py


# Quitar Fixear la vulnerabilidad 
sudo cp new_parche_proyecto/levels/new_lvl/fix/reset_password_service.py app/apis/auth/services/reset_password_service.py   


# Nueo lvl: Information Disclosure via Response Headers

## 📋 Clasificación OWASP
**API3:2023 - Broken Object Property Level Authorization**

## 🎯 Descripción de la Vulnerabilidad

### Caso Hipotético

Un desarrollador identificó una vulnerabilidad crítica en el endpoint `/reset-password`: cualquier usuario autenticado podía solicitar el restablecimiento de contraseña de **otro usuario** simplemente proporcionando su `username` en el body de la petición.

Para solucionar esto, el desarrollador agregó una validación para verificar que el `username` proporcionado coincidiera con el usuario autenticado (`current_user`). Si no coincidía, el sistema rechazaría la petición con un error 403.

Sin embargo, durante el proceso de debugging y testing, el desarrollador agregó headers HTTP personalizados (`X-User-*`) para inspeccionar rápidamente los datos del usuario objetivo sin necesidad de consultar la base de datos manualmente. La intención era verificar que el sistema estaba identificando correctamente al usuario antes de bloquear la petición.

**El problema:** Estos headers de debug nunca fueron removidos del código en producción. Ahora, aunque la petición es rechazada correctamente, los headers de respuesta **filtran información sensible** del usuario objetivo antes de lanzar la excepción HTTP 403.

### Información Expuesta

Cuando un atacante solicita el reset de password de otro usuario, aunque recibe un error 403, los siguientes datos son filtrados en los headers de respuesta:

- `X-User-Id`: ID interno del usuario
- `X-User-Phone`: Número de teléfono (PII)
- `X-User-Role`: Rol del usuario en el sistema
- `X-User-FirstName`: Nombre
- `X-User-LastName`: Apellido

## 🔓 Cómo se Explota

### Paso 1: Autenticación del Atacante
El atacante crea una cuenta legítima o compromete una existente para obtener un token de acceso válido.

### Paso 2: Enumeración de Usuarios
El atacante realiza peticiones al endpoint `/reset-password` con diferentes usernames de víctimas potenciales:

```bash
POST /reset-password
Authorization: Bearer {attacker_token}
Content-Type: application/json

{
  "username": "victim_username"
}
```

### Paso 3: Extracción de Información
Aunque la respuesta es un error 403, el atacante inspecciona los headers HTTP:

```
HTTP/1.1 403 Forbidden
X-User-Id: 42
X-User-Phone: 555-1234
X-User-Role: Customer
X-User-FirstName: John
X-User-LastName: Doe
```

## 🛡️ Cómo Solucionarlo

### Solución: Eliminar Headers de Debug

**Código Vulnerable:**
```python
def reset_password(data, response, current_user, db):
    user = db.query(User).filter(User.username == data.username).first()
    
    if current_user.username != data.username:
        headers = {}

        if user:
            headers = {
                "X-User-Id": str(user.id),
                "X-User-Phone": str(user.phone_number),
                "X-User-Role": str(user.role.value),
                "X-User-FirstName": user.first_name,
                "X-User-LastName": user.last_name,
            }

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "El username ingresado no coincide con la sesión actual"},
            headers=headers
        )
```

**Código Seguro:**
```python
if current_user.username != data.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El username ingresado no coincide con la sesión actual"
        )
```

### Principios de Seguridad Aplicados

1. **Fail Securely**: Lanzar la excepción inmediatamente sin procesar datos adicionales
2. **Minimal Information Disclosure**: No exponer información innecesaria en respuestas de error
3. **Remove Debug Code**: Eliminar todo código de debugging antes de producción
4. **Response Inspection**: Auditar headers de respuesta en endpoints sensibles

## 🔬 Prueba de Concepto

Ejecutar el exploit:

El script creará dos usuarios, autenticará al atacante e intentará solicitar el reset de password del usuario víctima, capturando la información filtrada en los headers de respuesta.
