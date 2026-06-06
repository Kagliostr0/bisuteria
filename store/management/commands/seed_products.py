import random, re
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from store.models import Category, Product, Variant

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.avif'}

PRODUCTS = [
    {
        "category": "Collares",
        "slug": "collares",
        "products": [
            {
                "name": "Collar Colgante Diamante Dorado",
                "slug": "collar-colgante-diamante-dorado",
                "price": 450.00,
                "stock": 15,
                "description": (
                    "Elegante collar con colgante rectangular de diamante en baño de oro de 18 quilates.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K sobre acero quirúrgico\n"
                    "• Colgante: Diamante sintético talla princesa\n"
                    "• Cadena: 45 cm de largo\n"
                    "• Cierre: Tipo lobster\n"
                    "• Peso aproximado: 8.5 g\n\n"
                    "Perfecto para ocasiones especiales o para regalar."
                ),
            },
            {
                "name": "Collar Cadena Dorada Clásica",
                "slug": "collar-cadena-dorada-clasica",
                "price": 320.00,
                "stock": 20,
                "description": (
                    "Collar de cadena clásica con dije de diamante.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero inoxidable bañado en oro 18K\n"
                    "• Dije: Diamante sintético 0.5 ct\n"
                    "• Cadena: 50 cm de largo\n"
                    "• Acabado: Brillante\n"
                    "• Hipoalergénico\n\n"
                    "Un básico que no puede faltar en tu colección."
                ),
            },
            {
                "name": "Collar Colgante Redondo Dorado",
                "slug": "collar-colgante-redondo-dorado",
                "price": 280.00,
                "stock": 25,
                "description": (
                    "Collar con colgante redondo dorado, diseño minimalista.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Colgante: Círculo de 2 cm de diámetro\n"
                    "• Cadena: 42 cm ajustable\n"
                    "• Acabado: Pulido espejo\n\n"
                    "Ideal para uso diario, combina con cualquier outfit."
                ),
            },
            {
                "name": "Collar Capa Dorado con Flores",
                "slug": "collar-capa-dorado-con-flores",
                "price": 520.00,
                "stock": 10,
                "description": (
                    "Collar tipo capa con diseño floral bañado en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K\n"
                    "• Diseño: Flores grabadas en placas entrelazadas\n"
                    "• Largo: 40 cm\n"
                    "• Cierre: Mosquetón\n"
                    "• Peso: 18 g\n\n"
                    "Una pieza llamativa para ocasiones especiales."
                ),
            },
            {
                "name": "Collar Gargantilla Dorada Delicada",
                "slug": "collar-gargantilla-dorada-delicada",
                "price": 360.00,
                "stock": 18,
                "description": (
                    "Gargantilla dorada delgada con dije minimalista.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero quirúrgico bañado en oro\n"
                    "• Largo: 38 cm + 5 cm extensión\n"
                    "• Dije: Círculo 1 cm con textura\n"
                    "• Acabado: Brillante\n"
                    "• Hipoalergénica\n\n"
                    "Perfecta para usar a capas con otros collares."
                ),
            },
        ],
    },
    {
        "category": "Aros",
        "slug": "aros",
        "products": [
            {
                "name": "Aros Dorados Grandes",
                "slug": "aros-dorados-grandes",
                "price": 250.00,
                "stock": 30,
                "description": (
                    "Aros grandes bañados en oro, diseño moderno.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Diámetro: 5 cm\n"
                    "• Ancho: 5 mm\n"
                    "• Cierre: Bisagra\n"
                    "• Peso: 12 g el par\n\n"
                    "Perfectos para darle un toque elegante a tu look."
                ),
            },
            {
                "name": "Aros Dorados con Diamantes",
                "slug": "aros-dorados-con-diamantes",
                "price": 420.00,
                "stock": 18,
                "description": (
                    "Aros colgantes con diamantes sintéticos bañados en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K\n"
                    "• Piedras: Diamantes sintéticos talla brillante\n"
                    "• Largo: 4 cm\n"
                    "• Cierre: Gancho\n"
                    "• Hipoalergénicos\n\n"
                    "Elegancia y brillo para noches especiales."
                ),
            },
            {
                "name": "Aros Dorados Medianos",
                "slug": "aros-dorados-medianos",
                "price": 180.00,
                "stock": 35,
                "description": (
                    "Aros medianos, diseño clásico y elegante.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero inoxidable bañado en oro\n"
                    "• Diámetro: 3 cm\n"
                    "• Acabado: Pulido brillante\n"
                    "• Cierre: Click\n"
                    "• Livianos y cómodos\n\n"
                    "El accesorio ideal para el día a día."
                ),
            },
            {
                "name": "Aros Candonga Dorados",
                "slug": "aros-candonga-dorados",
                "price": 310.00,
                "stock": 14,
                "description": (
                    "Aros tipo candonga con argollas doradas.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Diseño: Argolla doble\n"
                    "• Diámetro: 2.5 cm\n"
                    "• Cierre: Click\n"
                    "• Peso: 8 g el par\n\n"
                    "Tendencia moderna para cualquier ocasión."
                ),
            },
            {
                "name": "Aros Elegantes Dorados",
                "slug": "aros-elegantes-dorados",
                "price": 350.00,
                "stock": 20,
                "description": (
                    "Aros elegantes con diseño moderno bañados en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Diseño: Colgante con detalles brillantes\n"
                    "• Largo: 4.5 cm\n"
                    "• Cierre: Gancho\n"
                    "• Peso: 10 g el par\n\n"
                    "Perfectos para ocasiones especiales."
                ),
            },
            {
                "name": "Aros Dorados con Perlas",
                "slug": "aros-dorados-con-perlas",
                "price": 380.00,
                "stock": 12,
                "description": (
                    "Aros colgantes con perlas cultivadas bañados en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K\n"
                    "• Perlas: Cultivadas 8 mm\n"
                    "• Largo: 5 cm\n"
                    "• Cierre: Gancho\n"
                    "• Elegantes y sofisticados\n\n"
                    "Perfectos para bodas y eventos formales."
                ),
            },
        ],
    },
    {
        "category": "Pulseras",
        "slug": "pulseras",
        "products": [
            {
                "name": "Pulsera Bangle Dorada Clásica",
                "slug": "pulsera-bangle-dorada-clasica",
                "price": 300.00,
                "stock": 22,
                "description": (
                    "Pulsera bangle dorada con diseño clásico y elegante.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Diámetro: 6.5 cm\n"
                    "• Ancho: 8 mm\n"
                    "• Acabado: Brillante\n"
                    "• Peso: 15 g\n\n"
                    "Combínala con otras pulseras para un look apilado."
                ),
            },
            {
                "name": "Pulsera Cadena Delgada Dorada",
                "slug": "pulsera-cadena-delgada-dorada",
                "price": 220.00,
                "stock": 28,
                "description": (
                    "Pulsera de cadena delgada con baño dorado, delicada y femenina.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero quirúrgico bañado en oro\n"
                    "• Largo: 18 cm + 3 cm extensión\n"
                    "• Grosor: 1.5 mm\n"
                    "• Cierre: Lobster\n"
                    "• Hipoalergénica\n\n"
                    "Perfecta para usar sola o con charms."
                ),
            },
            {
                "name": "Pulsera Bangle Texturizada Dorada",
                "slug": "pulsera-bangle-texturizada-dorada",
                "price": 350.00,
                "stock": 15,
                "description": (
                    "Pulsera bangle con textura única y acabado dorado.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Diámetro: 6.5 cm\n"
                    "• Ancho: 12 mm\n"
                    "• Diseño: Texturizado con grabados\n"
                    "• Cierre: Abierto ajustable\n\n"
                    "Una pieza única con diseño artesanal."
                ),
            },
            {
                "name": "Pulsera Esclava Dorada",
                "slug": "pulsera-esclava-dorada",
                "price": 400.00,
                "stock": 10,
                "description": (
                    "Pulsera tipo esclava con diseño rígido bañada en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Ancho: 15 mm\n"
                    "• Circunferencia: 16 cm\n"
                    "• Cierre: Bisagra\n"
                    "• Acabado: Brillante\n\n"
                    "Un diseño atrevido y sofisticado."
                ),
            },
            {
                "name": "Pulsera Charms Dorada",
                "slug": "pulsera-charms-dorada",
                "price": 450.00,
                "stock": 8,
                "description": (
                    "Pulsera de charms con dijes intercambiables bañados en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Largo: 19 cm\n"
                    "• Incluye: 5 charms iniciales\n"
                    "• Cierre: Lobster\n"
                    "• Personalizable\n\n"
                    "Crea tu propio estilo único."
                ),
            },
        ],
    },
    {
        "category": "Anillos",
        "slug": "anillos",
        "products": [
            {
                "name": "Anillo Diamante Grande Dorado",
                "slug": "anillo-diamante-grande-dorado",
                "price": 520.00,
                "stock": 10,
                "description": (
                    "Anillo con diamante grande central bañado en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K sobre plata\n"
                    "• Piedra: Diamante sintético 1.5 ct\n"
                    "• Talla: Brillante redondo\n"
                    "• Tallas disponibles: 6 a 9\n"
                    "• Acabado: Pulido alto\n\n"
                    "Un anillo de compromiso o regalo espectacular."
                ),
            },
            {
                "name": "Anillo Dorado con Gemas Verdes",
                "slug": "anillo-dorado-con-gemas-verdes",
                "price": 460.00,
                "stock": 8,
                "description": (
                    "Anillo dorado con gemas verdes, diseño vintage.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Gemas: Esmeraldas sintéticas talla ovalada\n"
                    "• Talla: 7\n"
                    "• Diseño: Vintage con detalles grabados\n"
                    "• Ancho: 8 mm\n\n"
                    "Una pieza con estilo clásico y sofisticado."
                ),
            },
            {
                "name": "Anillo Dorado con Diamantes Múltiples",
                "slug": "anillo-dorado-con-diamantes-multiples",
                "price": 580.00,
                "stock": 7,
                "description": (
                    "Anillo dorado con múltiples diamantes en engaste pavé.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K\n"
                    "• Diamantes: 7 piedras talla brillante\n"
                    "• Quilates totales: 0.8 ct\n"
                    "• Talla: 7\n"
                    "• Acabado: Pulido espejo\n\n"
                    "Brilla con luz propia en cualquier ocasión."
                ),
            },
            {
                "name": "Anillo Ajustable Dorado",
                "slug": "anillo-ajustable-dorado",
                "price": 150.00,
                "stock": 40,
                "description": (
                    "Anillo ajustable dorado, diseño sencillo y elegante.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Talla: Ajustable (5 a 10)\n"
                    "• Ancho: 3 mm\n"
                    "• Acabado: Pulido\n"
                    "• Hipoalergénico\n\n"
                    "El básico que combina con todo."
                ),
            },
            {
                "name": "Anillo Dorado con Rubí",
                "slug": "anillo-dorado-con-rubi",
                "price": 490.00,
                "stock": 6,
                "description": (
                    "Anillo dorado con rubí sintético central.\n\n"
                    "Detalles del producto:\n"
                    "• Material: Baño de oro 18K\n"
                    "• Piedra: Rubí sintético talla ovalada\n"
                    "• Talla: 7\n"
                    "• Diseño: Engaste tipo garra\n"
                    "• Acabado: Alto brillo\n\n"
                    "Un toque de color y distinción."
                ),
            },
        ],
    },
    {
        "category": "Sets",
        "slug": "sets",
        "products": [
            {
                "name": "Set Joyero 3 Piezas Dorado",
                "slug": "set-joyero-3-piezas-dorado",
                "price": 890.00,
                "stock": 5,
                "description": (
                    "Set completo de joyería: collar, aros y pulsera en dorado.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: 45 cm con colgante decorado\n"
                    "• Aros: Colgantes a juego\n"
                    "• Pulsera: 18 cm con diseño coordinado\n"
                    "• Material: Baño de oro 18K\n"
                    "• Incluye: Estuche de regalo\n\n"
                    "El regalo perfecto para ella."
                ),
            },
            {
                "name": "Set Elegante 4 Piezas Dorado",
                "slug": "set-elegante-4-piezas-dorado",
                "price": 1200.00,
                "stock": 3,
                "description": (
                    "Set de lujo: collar, aros, pulsera y anillo coordinados.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: 45 cm con dije central\n"
                    "• Aros: Tipo push con brillantes\n"
                    "• Pulsera: Rígida bangle\n"
                    "• Anillo: Talla ajustable\n"
                    "• Material: Oro 18K sobre acero quirúrgico\n"
                    "• Incluye: Estuche de lujo y bolsa de tela\n\n"
                    "Nuestra pieza más exclusiva."
                ),
            },
            {
                "name": "Set Primavera Collar y Aros",
                "slug": "set-primavera-collar-y-aros",
                "price": 650.00,
                "stock": 7,
                "description": (
                    "Set de collar y aros con diseño floral dorado.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: 45 cm con dije floral\n"
                    "• Aros: A juego con diseño de pétalos\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Acabado: Brillante\n"
                    "• Incluye: Bolsa de terciopelo\n\n"
                    "Fresco y elegante para la temporada."
                ),
            },
            {
                "name": "Set Nupcial 3 Piezas Dorado",
                "slug": "set-nupcial-3-piezas-dorado",
                "price": 1500.00,
                "stock": 2,
                "description": (
                    "Set de joyería nupcial: collar, aros y pulsera.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: Gargantilla con cristales\n"
                    "• Aros: Colgantes largos con brillantes\n"
                    "• Pulsera: Delgada con detalles\n"
                    "• Material: Oro 18K sobre plata\n"
                    "• Incluye: Estuche de lujo\n\n"
                    "Para el día más especial de tu vida."
                ),
            },
            {
                "name": "Set Collar y Aros Clásico",
                "slug": "set-collar-y-aros-clasico",
                "price": 750.00,
                "stock": 8,
                "description": (
                    "Set clásico de collar y aros bañados en oro.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: Cadena 45 cm con dije decorado\n"
                    "• Aros: A juego con el collar\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Acabado: Brillante\n"
                    "• Incluye: Bolsa de tela\n\n"
                    "Un regalo perfecto para cualquier ocasión."
                ),
            },
            {
                "name": "Set Día a Día Collar y Pulsera",
                "slug": "set-dia-a-dia-collar-y-pulsera",
                "price": 550.00,
                "stock": 10,
                "description": (
                    "Set diario de collar y pulsera combinados.\n\n"
                    "Detalles del producto:\n"
                    "• Collar: Cadena delgada 45 cm\n"
                    "• Pulsera: A juego 18 cm\n"
                    "• Material: Acero bañado en oro 18K\n"
                    "• Acabado: Brillante\n"
                    "• Livianos y cómodos\n\n"
                    "Perfectos para el uso diario con estilo."
                ),
            },
        ],
    },
]

VARIANT_TEMPLATES = [
    {"label": "Dorado / Oro 18K", "material": "oro_18k", "color": "dorado", "price_delta": 0, "size": "Única"},
    {"label": "Plateado / Plata", "material": "plata", "color": "plateado", "price_delta": -30, "size": "Única"},
    {"label": "Rosado / Oro Rosa", "material": "oro_rosa", "color": "rosado", "price_delta": 20, "size": "Única"},
]

# Manual mapping for download files whose names don't exactly match product slugs
DOWNLOAD_MAP = {
    "collar-colgante-diamante-dorado": "Collar Colgante Corazón Hueco Dorado.jpg",
    "collar-cadena-dorada-clasica": "Collar de perlas.webp",
    "collar-colgante-redondo-dorado": "Dije.jpg",
    "collar-capa-dorado-con-flores": "Pulsera.webp",
    "aros-dorados-con-perlas": "PENDIENTES, CHANEL, bisutería, imitación perla, metal amarillo. Moda vintage y accesorios.jpg",
    "pulsera-cadena-delgada-dorada": "Pulsera.jpg",
    "anillo-diamante-grande-dorado": "anillo de compromiso.png",
    "anillo-dorado-con-gemas-verdes": "Anillos.jpg",
    "anillo-dorado-con-diamantes-multiples": "Anillo.avif",
    "anillo-dorado-con-rubi": "brasalete.avif",
    "set-elegante-4-piezas-dorado": "Juego de collar y aros.jpg",
    "set-primavera-collar-y-aros": "Juego De Collar Y Pendientes De Perlas De Imitación - Gargantilla Multivuelta.webp",
    "set-nupcial-3-piezas-dorado": "Aros.jpg",
    "aros-elegantes-dorados": "Aros2.webp",
    "set-collar-y-aros-clasico": "made-in-china.webp",
}


def normalize(s):
    return re.sub(r'[^a-z0-9\s]', '', s.replace('-', ' ').replace('_', ' ')).lower().split()


class Command(BaseCommand):
    help = "Seed (or refresh) the database with categories, products, and variants"

    def handle(self, *args, **options):
        media_path = settings.MEDIA_ROOT / "products"
        media_path.mkdir(parents=True, exist_ok=True)
        downloads_path = Path(settings.BASE_DIR) / "downloads"
        downloads_path.mkdir(parents=True, exist_ok=True)

        random.seed(42)

        for cat_data in PRODUCTS:
            category, created = Category.objects.get_or_create(
                name=cat_data["category"],
                defaults={"slug": cat_data["slug"]},
            )
            if created:
                self.stdout.write(f"Categoría creada: {category.name}")

            for prod_data in cat_data["products"]:
                product, created = Product.objects.update_or_create(
                    slug=prod_data["slug"],
                    defaults={
                        "category": category,
                        "name": prod_data["name"],
                        "price": prod_data["price"],
                        "stock": prod_data["stock"],
                        "description": prod_data["description"],
                        "available": True,
                    },
                )
                if created:
                    self.stdout.write(f"Producto creado: {product.name}")
                else:
                    self.stdout.write(f"Producto actualizado: {product.name}")
                self._assign_image(product, downloads_path)
                self._create_variants(product, prod_data)

        self.stdout.write(self.style.SUCCESS("Base de datos poblada exitosamente"))

    def _create_variants(self, product, prod_data):
        base_price = float(product.price)
        for vt in VARIANT_TEMPLATES:
            price = max(base_price + vt["price_delta"], 50)
            sku = f"{product.slug.upper()}-{vt['material'].upper()}-{vt['color'].upper()}"
            Variant.objects.update_or_create(
                product=product,
                material=vt["material"],
                color=vt["color"],
                size=vt["size"],
                defaults={
                    "price_override": price,
                    "stock": max(product.stock // 3, 2),
                    "sku": sku,
                },
            )
        self.stdout.write(f"  Variantes actualizadas para: {product.name}")

    def _find_exact(self, slug, downloads_path):
        slug_lower = slug.lower()
        for f in sorted(downloads_path.iterdir()):
            if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS:
                if f.stem.lower() == slug_lower:
                    return f
        return None

    def _find_fuzzy(self, slug, category_slug, downloads_path, used_files):
        slug_words = set(normalize(slug))
        cat_word = category_slug.rstrip('s')
        candidates = []

        for f in sorted(downloads_path.iterdir()):
            if not (f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS):
                continue
            if f in used_files:
                continue
            stem = f.stem.lower()
            name_words = set(normalize(stem))
            common = slug_words & name_words
            has_cat = cat_word in name_words
            containment = slug in stem.replace('-', ' ').replace('_', ' ') or stem.replace('-', ' ').replace('_', ' ').replace('  ', ' ') in slug
            score = len(common) + (5 if has_cat else 0) + (10 if containment else 0)
            if score >= 2:
                candidates.append((score, f))

        candidates.sort(key=lambda x: (-x[0], x[1].stem))
        return candidates[0][1] if candidates else None

    def _assign_image(self, product, downloads_path):
        if product.image:
            product.image.delete(save=False)

        used = set()
        for p in Product.objects.exclude(image=''):
            if p.image:
                used.add(Path(p.image.path))

        # 1. Exact slug match
        match = self._find_exact(product.slug, downloads_path)
        if match:
            ext = match.suffix
            with open(match, "rb") as f:
                data = f.read()
            filename = f"{product.slug}{ext}"
            product.image.save(filename, ContentFile(data), save=True)
            self.stdout.write(f"  Imagen: {product.name} ({match.name})")
            return

        # 2. Manual map (DOWNLOAD_MAP)
        mapped = DOWNLOAD_MAP.get(product.slug)
        if mapped:
            src = downloads_path / mapped
            if src.exists():
                ext = src.suffix
                with open(src, "rb") as f:
                    data = f.read()
                filename = f"{product.slug}{ext}"
                product.image.save(filename, ContentFile(data), save=True)
                self.stdout.write(f"  Imagen: {product.name} ({src.name})")
                return

        # 3. Fuzzy match
        fuzzy = self._find_fuzzy(product.slug, product.category.slug, downloads_path, used)
        if fuzzy:
            ext = fuzzy.suffix
            with open(fuzzy, "rb") as f:
                data = f.read()
            filename = f"{product.slug}{ext}"
            product.image.save(filename, ContentFile(data), save=True)
            self.stdout.write(f"  Imagen (fuzzy): {product.name} ({fuzzy.name})")
            return

        self.stdout.write(self.style.WARNING(f"  SIN IMAGEN: {product.name} — no hay archivo en downloads/"))
