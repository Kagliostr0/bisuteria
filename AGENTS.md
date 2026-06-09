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

### Cambios 2026-06-07 (~21:25)
- Backup: `bisuteria-backup-20260607-212728`
- Reemplazada imagen `set-dia-a-dia-collar-y-pulsera.jpg` en `downloads/` y `media/products/`
- Ejecutado `seed_products` para copiar la imagen nueva a `media/products/`
- Commit + push a GitHub (Railway actualizado automáticamente)

### Cambios 2026-06-08 (~00:40)
- Backup: `bisuteria-backup-20260608-003927`
- Agregadas clases CSS `.gold-brillo` (shimmer + glow en fondos) y `.gold-text-brillo` (glow en texto)
- Aplicado `.gold-brillo` a header, hero, footer (metallic shimmer animado + glow)
- Aplicado `.gold-text-brillo` a títulos, precios y logo (text-shadow glow)
- Solo local, sin push

### Cambios inspirados en Swarovski (2026-06-08 ~01:01)
- Backup: `bisuteria-backup-20260608-010111`
- Agregada Google Font: Playfair Display (títulos) + Inter (cuerpo)
- Clase `.font-heading` con Playfair Display para títulos elegantes
- **Header**: cambiado de fondo dorado masivo a `bg-gray-950/80` con borde sutil dorado, texto gold-400, blur
- **Footer**: cambiado de fondo dorado a fondo oscuro con borde sutil, texto gold-400 con glow
- **Hero**: mantenido con `gold-brillo` (shimmer + sweep), más espaciado, título más grande
- **Categorías**: sidebar más sutil (`border-gold-800/30`, `text-gray-400`)
- **Tarjetas producto**: bordes más sutiles (`border-gold-800/50`), títulos con Playfair Display
- Aplicado `.font-heading` a todos los títulos principales (h1, h2, h3 clave)
- Solo local, sin push

### Carrusel + reflejo (2026-06-08 ~01:18)
- Backup: `bisuteria-backup-20260608-010111` (mismo backup anterior, no se tocó)
- Agregado **Swiper.js** vía CDN para carrusel hero
- Descargadas 2 fotos de Pexels (modelos con joyas) a `static/images/`
- Hero reemplazado por carrusel con 2 slides: fondo de modelo + overlay oscuro + texto dorado + gold-brillo
- Autoplay lento (5s), navegación con flechas y bullets dorados
- Agregado **reflejo dorado** debajo de cada card de producto (`.product-card::after` con gradiente radial)
- Clase `product-card` aplicada en home y listado de productos
- Solo local, sin push

### Cambios 2026-06-08 (~01:50)
- Reemplazado modelo-2.jpg: ahora es un primer plano de mujer con collar de cadena dorada bien visible (Pexels 32220056)
- Reemplazado modelo-3.jpg: mujer con joyería floral y tatuaje visible en el brazo (Pexels 29579373)
- Cambiado overlay del carrusel de `bg-black/30` a gradiente `from-black/60 via-black/10 to-transparent` para que las joyas y tatuajes se vean sin oscurecer la parte superior
- Reemplazado modelo-3.jpg: mujer con tatuaje visible y aros grandes (Pexels 16135565, "Portrait of Beautiful Woman Wearing Earrings and Tattoo")

### Cambios 2026-06-08 (~02:40-02:50)
- Backup: `bisuteria-backup-20260608-0247`
- Arregladas posiciones de fondo para slides 2 y 3
- Reemplazados modelo-2.jpg y modelo-3.jpg varias veces hasta ajustar
- modelo-2.jpg final: primer plano mujer con collar cadena dorada (Pexels 32220056)
- modelo-3.jpg final: primer plano con set de joyería dorada (collar, aros, anillo) (Pexels 10944923)
- Overlay cambiado a gradiente `from-black/60 via-black/10 to-transparent`
- Altura carrusel reducida (`py-10 sm:py-16`) para menos zoom
- Commit + push a GitHub (autorizado por usuario)

### Cambios 2026-06-08 (~04:08)
- Backup: `bisuteria-backup-20260608-0408`
- Agregado `.slide-reflejo` (reflejo dorado animado con sweep) sobre los 3 slides del carrusel
- Solo CSS + HTML, sin tocar funcionalidad ni BD
- Commit + push a GitHub (autorizado por usuario)

### Próximos pasos posibles
- Autenticación de usuarios (registro/login)
- Pasarela de pago (Mercado Pago, Stripe)
- Subir a producción (hosting)
