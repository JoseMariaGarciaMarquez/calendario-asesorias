# Configuración con Google Sheets (RECOMENDADO)

## ¿Por qué Google Sheets?

✅ **100% Gratuito** - Sin límites para este uso
✅ **Más simple que Gist** - Solo 3 pasos
✅ **Visual** - Puedes ver y editar las citas directamente
✅ **Confiable** - Google maneja la persistencia

## Pasos de Configuración (5 minutos)

### 1. Crear una Google Sheet

1. Ve a: https://sheets.google.com
2. Crea una nueva hoja
3. **COPIA LA URL** completa (ejemplo: `https://docs.google.com/spreadsheets/d/ABC123...`)
4. Comparte la hoja:
   - Click en "Compartir" (arriba derecha)
   - Cambiar a "Cualquier persona con el enlace puede editar"

### 2. Crear Service Account en Google Cloud

1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto nuevo (o usa uno existente)
3. Habilita la API:
   - Busca "Google Sheets API"
   - Click en "HABILITAR"
4. Crear credenciales:
   - Menu → "IAM y administración" → "Cuentas de servicio"
   - Click "CREAR CUENTA DE SERVICIO"
   - Nombre: `calendario-asesorias`
   - Click "CREAR Y CONTINUAR"
   - Rol: "Editor" → Click "CONTINUAR" → "LISTO"
5. Generar clave JSON:
   - Click en la cuenta de servicio creada
   - Pestaña "CLAVES"
   - "AGREGAR CLAVE" → "Crear clave nueva" → JSON
   - **Descargar el archivo JSON**

### 3. Configurar Streamlit Cloud

1. Ve a tu app en: https://share.streamlit.io/
2. Click en ⋮ → "Settings"
3. En "Secrets", pega esto:

```toml
STORAGE_TYPE = "sheets"
SHEET_URL = "https://docs.google.com/spreadsheets/d/TU_ID_AQUI/edit"

[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\nTU_CLAVE_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "calendario@tu-proyecto.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

**IMPORTANTE**: Copia todos los campos del JSON descargado. La `private_key` debe mantener los `\n`.

4. Click "Save" → La app se reiniciará

### 4. Dar acceso a la Service Account

1. Abre tu Google Sheet
2. Click en "Compartir"
3. Añade el email de la service account:
   - Email: `calendario@tu-proyecto.iam.gserviceaccount.com`
   - Rol: "Editor"
4. Click "Enviar"

### 5. Verificar

- Agenda una cita
- Abre tu Google Sheet
- Deberías ver la cita en una fila

¡Listo! Las citas se guardarán automáticamente en Google Sheets y **nunca se perderán**. 🎉

---

## Alternativa: GitHub Gist (más técnico)

Si prefieres Gist, usa `STORAGE_TYPE = "gist"` y sigue [CONFIGURACION_GIST.md](CONFIGURACION_GIST.md)

## Para desarrollo local

No configures secrets. La app usará `citas.json` local automáticamente.
