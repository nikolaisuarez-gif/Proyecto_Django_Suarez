from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Category, Product


PRODUCTS = [
    ('Tecnología', 'Dispositivos y accesorios para trabajo y entretenimiento.', 'Audífonos inalámbricos', 'Sonido envolvente y batería para todo el día.', '189.90', 14, '#3157a4'),
    ('Tecnología', 'Dispositivos y accesorios para trabajo y entretenimiento.', 'Teclado mecánico', 'Teclado compacto con switches táctiles.', '249.00', 8, '#3d7e8a'),
    ('Tecnología', 'Dispositivos y accesorios para trabajo y entretenimiento.', 'Mouse ergonómico', 'Control preciso para largas jornadas.', '119.50', 21, '#7950a1'),
    ('Tecnología', 'Dispositivos y accesorios para trabajo y entretenimiento.', 'Monitor 27 pulgadas', 'Panel IPS Full HD de 75 Hz.', '899.00', 5, '#39705d'),
    ('Hogar', 'Objetos funcionales para espacios cotidianos.', 'Lámpara de escritorio', 'Luz LED regulable con brazo articulado.', '95.00', 17, '#b07838'),
    ('Hogar', 'Objetos funcionales para espacios cotidianos.', 'Botella térmica', 'Acero inoxidable, capacidad de 750 ml.', '69.90', 32, '#9e5363'),
    ('Accesorios', 'Complementos útiles para llevar a todas partes.', 'Mochila urbana', 'Compartimento acolchado para laptop de 15 pulgadas.', '159.00', 11, '#47618c'),
    ('Accesorios', 'Complementos útiles para llevar a todas partes.', 'Soporte para laptop', 'Base plegable con altura ajustable.', '79.00', 19, '#65804a'),
]


class Command(BaseCommand):
    help = 'Crea tres categorías y ocho productos de demostración con imágenes locales.'

    def handle(self, *args, **options):
        image_directory = Path(settings.MEDIA_ROOT) / 'products'
        image_directory.mkdir(parents=True, exist_ok=True)
        for category_name, description, name, product_description, price, stock, color in PRODUCTS:
            category, _ = Category.objects.get_or_create(name=category_name, defaults={'description': description})
            filename = f'{slugify(name)}.svg'
            image_path = image_directory / filename
            image_path.write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">'
                f'<rect width="800" height="600" rx="40" fill="{color}"/><circle cx="400" cy="270" r="145" fill="#ffffff" fill-opacity=".13"/>'
                f'<text x="400" y="285" text-anchor="middle" fill="white" font-family="Arial" font-size="38">{name}</text>'
                '<text x="400" y="355" text-anchor="middle" fill="white" fill-opacity=".8" font-family="Arial" font-size="21">Catálogo de productos</text></svg>',
                encoding='utf-8',
            )
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category, 'description': product_description,
                    'price': price, 'stock': stock,
                },
            )
            image_name = f'products/{filename}'
            if created or product.image.name != image_name:
                product.image.name = image_name
                product.save(update_fields=['image'])
        self.stdout.write(self.style.SUCCESS('Catálogo listo: 3 categorías y 8 productos con imagen.'))
