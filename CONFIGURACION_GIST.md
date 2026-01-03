# Configuración de Almacenamiento Persistente con GitHub Gist

## ¿Por qué usar GitHub Gist?

Streamlit Cloud tiene un sistema de archivos efímero que se reinicia cuando la app se duerme. GitHub Gist proporciona almacenamiento persistente gratuito y fácil de configurar.

## Pasos de Configuración

### 1. Crear un Token Personal de GitHub

1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre descriptivo (ej: "Calendario Asesorías")
4. Marca el permiso: **`gist`**
5. Click en "Generate token"
6. **COPIA Y GUARDA EL TOKEN** (no podrás verlo de nuevo)

### 2. Crear un Gist

1. Ve a: https://gist.github.com/
2. Click en "+" (arriba a la derecha)
3. Filename: `citas.json`
4. Contenido inicial: `{}`
5. Click en "Create secret gist" (o público si prefieres)
6. **COPIA LA ID DEL GIST** de la URL
   - Ejemplo: `https://gist.github.com/tuusuario/abc123def456`
   - La ID es: `abc123def456`

### 3. Configurar Streamlit Cloud

1. Ve a tu app en: https://share.streamlit.io/
2. Click en los tres puntos (⋮) → "Settings"
3. En la sección "Secrets", añade:

```toml
USE_GIST = true
GITHUB_TOKEN = "ghp_tu_token_aqui"
GIST_ID = "tu_gist_id_aqui"
```

4. Click en "Save"
5. La app se reiniciará automáticamente

### 4. Verificación

- La app ahora guardará todas las citas en el Gist
- Puedes ver el Gist en cualquier momento para verificar
- Las citas persisten aunque la app se duerma

## Desarrollo Local

Para desarrollo local sin Gist, simplemente no configures los secrets. La app usará el archivo `citas.json` local automáticamente.

## Solución de Problemas

### Error: "Error al cargar citas desde Gist"
- Verifica que el token tenga el permiso `gist`
- Verifica que el GIST_ID sea correcto
- Asegúrate de que el Gist existe y es accesible

### Error: "Error al guardar citas"
- Verifica que el token no haya expirado
- Verifica los permisos del token
- Revisa que USE_GIST = true esté escrito correctamente

## Migrar Citas Existentes

Si ya tienes citas en `citas.json` local:

1. Copia el contenido de tu `citas.json`
2. Ve a tu Gist en GitHub
3. Click en "Edit"
4. Pega el contenido en el archivo `citas.json`
5. Click en "Update secret gist"
