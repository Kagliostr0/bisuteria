# Bisutería Dorada — E-commerce Django

## Reglas del proyecto

### 1. Todo en local
Todos los cambios, pruebas y despliegues se hacen exclusivamente en local. Nada de producción ni hosting sin aprobación.

### 2. Nada a GitHub sin permiso
No se hace commit, push ni se sube nada a GitHub/repositorios sin mi consentimiento expreso y explícito.

### 3. Backup + notas siempre
Antes de cualquier cambio importante se hace un backup en `C:\Users\lomt1\AppData\Local\Temp\opencode\` y se toman notas en este archivo sobre lo que se hizo.

### Stack
- Python 3.14 + Django 6.0
- PostgreSQL 17.10 (base de datos)
- psycopg2-binary 2.9.12
- Pillow (imágenes)
- Tailwind CSS vía CDN

### Apps
- `store` — Catálogo (Categorías, Productos)
- `shopping_cart` — Carrito de compras (sesiones)
- `checkout` — Órdenes y formulario de envío
- `core` — Páginas estáticas (inicio, nosotros)

### Diseño
- **Colores**: Dorado (`#e6b800` / `amber`) + Negro
- **Modo oscuro**: Toggle con localStorage, clase `dark` en `<html>`
- **Responsive**: Tailwind breakpoints (`sm:`, `md:`, `lg:`)

### Admin
- `admin` / `admin123`
- Panel en `/admin/`

### Datos
- 25 productos semilla en 5 categorías (Collares, Aros, Pulseras, Anillos, Sets)
- 3 variantes por producto (75 total): Dorado/Oro 18K, Plateado/Plata, Rosado/Oro Rosa
- Imágenes reales descargadas de Burst (Shopify) y Pexels (fotos de joyería real)
- `store/seed_images/` contiene 31 fotos reales de collar, aros, pulseras, anillos, sets
- Comando: `python manage.py seed_products` (usa `update_or_create`, actualiza todo)
- Backup: `C:\Users\lomt1\AppData\Local\Temp\opencode\bisuteria-backup-20260605-091045`
- Backup v2: `bisuteria-backup-20260605-091045-v2` (post-variants+imagenes)
- Descargas: `downloads/` (copia de las imágenes de productos)
- Pillow queda como fallback si faltan imágenes seed

### Imágenes
- WebP y AVIF soportados (Pillow 12.2.0)
- Seed command busca SOLO en `downloads/` (cualquier extensión: jpg, png, webp, avif)
- Coincidencia exacta por slug → DOWNLOAD_MAP manual → fuzzy match
- Sin fallback a seed_images/ ni generación Pillow

### Migración a PostgreSQL
- Fecha: 2026-06-05
- Backup: `C:\Users\lomt1\AppData\Local\Temp\opencode\bisuteria-backup-20260605-postgres-migration`
- Servicio: `postgresql-x64-17` (Windows)
- DB: `bisuteria`, User: `bisuteria_user`, Pass: `admin123`, Puerto: 5432
- 203 objetos migrados desde SQLite via dumpdata/loaddata
- SQLite dump: `C:\Users\lomt1\AppData\Local\Temp\opencode\sqlite-dump-utf8.json`

### Backup estética (2026-06-05 22:02)
- Backup: `bisuteria-backup-20260605-220259`
- Estado actual: dark mode completo, oro (`#e6b800`) + grises oscuros
- Pendiente: mejoras visuales definidas por el usuario

### Cambios estética v2 (2026-06-05 ~22:00-23:30)
- Backup final: `bisuteria-backup-20260605-233049`
- **Iconos**: emojis (✨💎🎁🛒) reemplazados por Phosphor Icons vía CDN (`ph-sparkle`, `ph-diamond`, `ph-gift`, `ph-shopping-cart`, `ph-list`, `ph-x`, `ph-tag`, `ph-info`, `ph-sign-in`, `ph-sign-out`, `ph-gear-six`)
- **Barra navegación mobile**: menú hamburguesa con toggle (☰/✕), dropdown oscuro con iconos. En mobile chico muestra solo "Bisutería" en vez del nombre completo
- **Footer**: más angosto en mobile (`py-2`), icono Phosphor en vez de emoji
- **Hero banner**: más compacto en mobile (`py-6`, título `text-2xl`)
- **Imágenes productos**: cuadradas en mobile (`aspect-square`), apaisadas en desktop
- **Inputs**: ahora cuadrados (`border-radius: 0`)
- **Login**: template propio en `templates/registration/login.html`
- **Auth**: URLs de `django.contrib.auth` agregadas bajo `accounts/`
- **Login redirect**: redirige a `/admin/` en vez de `/`
- **ALLOWED_HOSTS**: cambiado a `["*"]` para acceso desde móvil
- **Firewall**: regla para puerto 8000 agregada (si hay permisos de admin)
- **Nav admin**: icono engranaje ⚙ visible cuando admin logueado, link a `/admin/`

### Próximos pasos posibles
- Autenticación de usuarios (registro/login)
- Pasarela de pago (Mercado Pago, Stripe)
- Subir a producción (hosting)
