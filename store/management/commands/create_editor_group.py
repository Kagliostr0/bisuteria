from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el grupo Editor con permisos limitados (solo lectura/edición)"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Editor")
        if not created:
            self.stdout.write(self.style.WARNING("El grupo 'Editor' ya existe."))
            return

        perm_codenames = [
            # Productos: ver, cambiar (editar)
            "view_product",
            "change_product",
            # Categorías: ver, cambiar
            "view_category",
            "change_category",
            # Variantes: ver, cambiar, agregar, eliminar
            "view_variant",
            "change_variant",
            "add_variant",
            "delete_variant",
            # Pedidos: ver, cambiar
            "view_order",
            "change_order",
        ]

        perms = Permission.objects.filter(codename__in=perm_codenames)
        group.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS(f"Grupo 'Editor' creado con {perms.count()} permisos."))
