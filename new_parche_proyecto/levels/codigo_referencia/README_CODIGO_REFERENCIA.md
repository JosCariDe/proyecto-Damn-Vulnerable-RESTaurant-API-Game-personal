# Level Codigo Referencia: Referral System Abuse (Double Vulnerability)

## 📌 Inicio Rápido

### Prerequisitos
Asegúrate de tener activado tu entorno virtual de Python:

```bash
source venv/bin/activate
```

### Comandos de Prueba

#### 1️⃣ Ejecutar script para ver las vulnerabilidades
```bash
python3 new_parche_proyecto/levels/codigo_referencia/scripts/exploit_codigo_referencia.py
```

#### 2️⃣ Aplicar parche de seguridad
```bash
sudo cp new_parche_proyecto/levels/codigo_referencia/fix/service.py app/apis/referrals/service.py
```

#### 3️⃣ Verificar que las vulnerabilidades fueron corregidas
```bash
python3 new_parche_proyecto/levels/codigo_referencia/scripts/exploit_codigo_referencia.py
```

#### 4️⃣ Revertir parche (opcional)
```bash
sudo cp new_parche_proyecto/levels/codigo_referencia/unpatch/service.py app/apis/referrals/service.py
```

---

## 📋 Clasificación OWASP

**Vulnerabilidad #1:** API6:2023 - Unrestricted Access to Sensitive Business Flows  
**Vulnerabilidad #2:** API2:2023 - Broken Authentication (Self-Referral)

---

## 🎯 Descripción de las Vulnerabilidades

Este nivel presenta **dos vulnerabilidades críticas** en el sistema de códigos de referidos que permiten a los usuarios abusar del programa de descuentos:

### Vulnerabilidad #1: Unrestricted Referral Usage

**Problema:** No hay límite de cuántas veces un usuario puede aplicar el mismo código de referido.

El endpoint `/apply-referral` no valida si el usuario ya aplicó previamente un código de referido específico. Esto permite:
- Aplicar el mismo código múltiples veces
- Acumular descuentos ilimitados (20% × N aplicaciones)
- Abusar del sistema sin restricciones

```python
@router.post("/apply-referral")
async def apply_referral_code(request, current_user, db):
    referrer = db.query(User).filter(User.referral_code == request.referral_code).first()
    
    # ❌ NO valida si ya aplicó este código antes
    # ❌ Permite múltiples aplicaciones del mismo código
    
    discount_coupon = DiscountCoupon(
        user_id=current_user.id,
        referrer_user_id=referrer.id,
        discount_percentage=20
    )
    db.add(discount_coupon)
    db.commit()
```

### Vulnerabilidad #2: Self-Referral Attack

**Problema:** Un usuario puede aplicar su propio código de referido a sí mismo.

El sistema no valida que el referidor (`referrer`) sea diferente del usuario que aplica el código (`current_user`). Esto permite:
- Auto-referirse sin referir a nadie
- Obtener descuentos sin cumplir el propósito del programa
- Abusar del sistema de incentivos

```python
@router.post("/apply-referral")
async def apply_referral_code(request, current_user, db):
    referrer = db.query(User).filter(User.referral_code == request.referral_code).first()
    
    # ❌ NO valida que referrer.id != current_user.id
    # ❌ Permite auto-referenciación
    
    discount_coupon = DiscountCoupon(
        user_id=current_user.id,
        referrer_user_id=referrer.id,  # Puede ser el mismo ID
        discount_percentage=20
    )
```

---

## 🔓 Cómo se Explotan

### Exploit Vulnerabilidad #1: Múltiples Aplicaciones

#### Paso 1: Crear dos usuarios
```bash
POST /register
{
  "username": "user_a",
  "password": "pass123",
  ...
}

POST /register
{
  "username": "user_b",
  "password": "pass456",
  ...
}
```

#### Paso 2: Usuario A obtiene su código de referido
```bash
GET /referral-code
Authorization: Bearer {user_a_token}

Response: {"code": "ABC12345"}
```

#### Paso 3: Usuario B aplica el código múltiples veces
```bash
# Primera aplicación
POST /apply-referral
Authorization: Bearer {user_b_token}
{"referral_code": "ABC12345"}
→ 200 OK, cupón 1 creado (20% descuento)

# Segunda aplicación (DEBERÍA FALLAR, PERO NO LO HACE)
POST /apply-referral
Authorization: Bearer {user_b_token}
{"referral_code": "ABC12345"}
→ 200 OK, cupón 2 creado (20% descuento)

# Tercera, cuarta, quinta... N aplicaciones
→ Acumula 20% × N en descuentos
```

#### Paso 4: Verificar cupones acumulados
```bash
GET /discount-coupons
Authorization: Bearer {user_b_token}

Response: [
  {"id": 1, "discount_percentage": 20, ...},
  {"id": 2, "discount_percentage": 20, ...},
  {"id": 3, "discount_percentage": 20, ...},
  ...
]
```

### Exploit Vulnerabilidad #2: Self-Referral

#### Paso 1: Usuario obtiene su propio código
```bash
GET /referral-code
Authorization: Bearer {token}

Response: {"code": "XYZ78910"}
```

#### Paso 2: Usuario aplica SU PROPIO código
```bash
POST /apply-referral
Authorization: Bearer {token}
{
  "referral_code": "XYZ78910"  # ← Su propio código
}

Response: {
  "message": "Referral code XYZ78910 applied successfully",
  "discount": 20.0
}
```

#### Paso 3: Obtiene descuento sin referir a nadie
```bash
GET /discount-coupons
Authorization: Bearer {token}

Response: [
  {
    "id": 1,
    "discount_percentage": 20,
    "user_id": 42,
    "referrer_user_id": 42  # ← Mismo usuario
  }
]
```

---

## 🛡️ Cómo Solucionarlo

### Solución Completa: Dos Validaciones

**Código Vulnerable:**
```python
@router.post("/apply-referral")
async def apply_referral_code(request, current_user, db):
    referrer = db.query(User).filter(
        User.referral_code == request.referral_code
    ).first()
    
    if referrer is None:
        return {"message": "Invalid referral code", "discount": 0.0}
    
    # ❌ Sin validaciones de seguridad
    
    discount_coupon = DiscountCoupon(
        user_id=current_user.id,
        referrer_user_id=referrer.id,
        discount_percentage=20
    )
    db.add(discount_coupon)
    db.commit()
    
    return {"message": "Applied successfully", "discount": 20.0}
```

**Código Seguro:**
```python
@router.post("/apply-referral")
async def apply_referral_code(request, current_user, db):
    referrer = db.query(User).filter(
        User.referral_code == request.referral_code
    ).first()
    
    if referrer is None:
        raise HTTPException(status_code=400, detail="Invalid referral code")
    
    # ✅ FIX #1: Prevenir self-referral
    if referrer.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot apply your own referral code"
        )
    
    # ✅ FIX #2: Validar uso único por usuario
    existing_coupon = db.query(DiscountCoupon).filter(
        DiscountCoupon.user_id == current_user.id,
        DiscountCoupon.referrer_user_id == referrer.id
    ).first()
    
    if existing_coupon:
        raise HTTPException(
            status_code=400,
            detail="You have already applied this referral code"
        )
    
    # Si pasa todas las validaciones, crear cupón
    discount_coupon = DiscountCoupon(
        user_id=current_user.id,
        referrer_user_id=referrer.id,
        discount_percentage=20
    )
    db.add(discount_coupon)
    db.commit()
    
    return {"message": "Applied successfully", "discount": 20.0}
```

### Principios de Seguridad Aplicados

1. **Business Logic Validation**: Validar reglas de negocio antes de procesar
2. **Uniqueness Constraints**: Garantizar que las relaciones sean únicas
3. **Self-Reference Prevention**: Evitar que usuarios se referencien a sí mismos
4. **Rate Limiting**: Limitar acciones sensibles del negocio
5. **Fail Securely**: Rechazar con error explícito en lugar de permitir silenciosamente

---

## 💡 Lecciones Aprendidas

- ❌ **No asumir comportamiento honesto**: Los usuarios pueden intentar abusar del sistema
- ❌ **Validar lógica de negocio**: No solo validar tipos de datos, sino reglas del negocio
- ✅ **Implementar restricciones de unicidad**: Prevenir relaciones duplicadas en DB
- ✅ **Testing de edge cases**: Probar escenarios de abuso y límites
- ✅ **Monitoreo de patrones**: Detectar uso anormal del sistema

---

## 📊 Impacto

### Impacto Combinado

Cuando ambas vulnerabilidades se explotan juntas:
- Usuario puede auto-referirse Y aplicar múltiples veces
- Acumulación ilimitada de descuentos sin referir a nadie
- Colapso completo del programa de incentivos


## 🔬 Prueba de Concepto

Ejecutar el exploit:
```bash
python3 new_parche_proyecto/levels/lvl_5/scripts/exploit_lvl5.py
```

El script:
1. Creará dos usuarios (atacante y víctima)
2. Obtendrá código de referido del atacante
3. **Probará self-referral**: Atacante aplica su propio código
4. **Probará aplicación legítima**: Víctima aplica código del atacante (control)
5. **Probará múltiples aplicaciones**: Víctima aplica el mismo código 5 veces
6. Mostrará cupones acumulados y descuentos totales
7. Emitirá veredicto: VULNERABLE o PROTEGIDO

### Resultados Esperados

**Sistema Vulnerable:**
```
🚨 VULNERABILIDAD #1 CONFIRMADA: Unrestricted Usage
   ❌ Se aplicó el mismo código 5 veces
   ❌ Descuento fraudulento acumulado: 100%

🚨 VULNERABILIDAD #2 CONFIRMADA: Self-Referral
   ❌ El usuario aplicó su PROPIO código
   ❌ No se valida que referrer ≠ applicant
```

**Sistema Protegido:**
```
✅ PROTEGIDO: Solo se permite una aplicación por código
✅ PROTEGIDO: Self-referral bloqueado
```


## 📚 Referencias

- OWASP API Security Top 10 2023: API6:2023, API2:2023
- CWE-840: Business Logic Errors
- CWE-841: Improper Enforcement of Behavioral Workflow
- CWE-863: Incorrect Authorization

