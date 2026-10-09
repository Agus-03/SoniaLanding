
# SONIA — Orquestación Conversacional Inteligente

SONIA es una propuesta de inteligencia artificial conversacional orientada a ayudar a pequeñas y medianas empresas a gestionar sus conversaciones con clientes de manera más fluida, organizada y contextual.

## Estado del proyecto

La landing page se encuentra en una etapa de validación de interés y demanda. El programa Early Adopter todavía no está habilitado.

## Tecnologías

- Python
- Streamlit
- Requests
- Supabase (opcional, para registrar clics de manera persistente)

## Estructura del repositorio

- `app.py`: aplicación principal de Streamlit.
- `requirements.txt`: dependencias de Python.
- `index.html`: versión HTML anterior de la landing.
- `styles.css`: estilos de la versión HTML anterior.
- `script.js`: interacciones de la versión HTML anterior.
- `server.py`: servidor de la versión HTML anterior.

## Ejecución local

Instalá las dependencias:

```bash
pip install -r requirements.txt
```

Iniciá la aplicación:

```bash
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Subí los archivos del proyecto a GitHub.
2. Creá o abrí la aplicación en Streamlit Community Cloud.
3. Seleccioná el repositorio y la rama correspondiente.
4. Configurá `app.py` como archivo principal.
5. Desplegá la aplicación.

## Registro de interés

La aplicación permite registrar clics en el botón Early Adopter.

Sin configurar Supabase, utiliza SQLite local como alternativa de prueba. Ese almacenamiento no debe considerarse persistente en Streamlit Community Cloud.

Para conservar métricas entre reinicios y despliegues, configurá Supabase y las variables `SUPABASE_URL` y `SUPABASE_KEY` en los Secrets de Streamlit.

## Estado de la propuesta

SONIA está en desarrollo. Las funcionalidades presentadas en la landing describen la propuesta y no implican que todas estén implementadas actualmente.