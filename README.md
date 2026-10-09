# SONIA — Landing de validación

Landing orientada a validar interés por el programa Early Adopter.

## Diseño

La implementación toma del Manual de Marca:
- Verde Bosque Profundo `#0E311F`
- Menta Suave `#DDF4ED`
- Turquesa `#3FD0D5`
- Azul Noche `#01111D`
- Blanco Nieve `#F5FFF9`
- Clear Sans para títulos/cuerpo
- Flatory Serif reservado para el lenguaje visual del logotipo

## Ejecutar localmente

Requiere Python 3:

```bash
python server.py
```

Abrir `http://localhost:8080`.

## Métrica principal

Cada clic sobre "Quiero ser Early Adopter" genera un evento:
`early_adopter_cta_click`

El prototipo lo guarda en SQLite y devuelve el total acumulado.

Para producción:
1. integrar `/api/early-adopter-click` en el backend real;
2. agregar rate limiting/anti-bot;
3. almacenar únicamente los datos de atribución necesarios;
4. mantener el mensaje de cierre del programa explícito, evitando un error técnico falso.

## Experimento recomendado

Medir:
- visitas;
- clics CTA;
- tasa visita → clic;
- origen/UTM;
- fecha/hora;
- eventualmente, formulario de contacto cuando el programa se habilite.

No conviene presentar un "error" técnico falso: para validación es más transparente indicar que el acceso todavía no está habilitado y que el interés quedó registrado.
