from django.db import models
from django.contrib.auth.models import User


class MemberProfile(models.Model):
    """
    RELACIÓN UNO A UNO (OneToOne)

    Cada usuario del sistema tiene exactamente un perfil de miembro.
    Se utiliza cuando una entidad extiende a otra con más información
    sin duplicar la tabla original (User).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="member_profile",
        help_text="Usuario base del sistema (relación uno a uno)"
    )

    membership_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Identificador único de la membresía"
    )

    address = models.CharField(
        max_length=255,
        help_text="Dirección del miembro"
    )

    phone = models.CharField(
        max_length=20,
        help_text="Teléfono de contacto"
    )

    joined_at = models.DateField(
        auto_now_add=True,
        help_text="Fecha de ingreso a la biblioteca"
    )

    class Meta:
        db_table = "member_profile"

    def __str__(self):
        return f"{self.user.username} - {self.membership_id}"


class Author(models.Model):
    """
    ENTIDAD PADRE PARA RELACIÓN UNO A MUCHOS

    Un autor puede escribir muchos libros,
    pero cada libro pertenece a un solo autor.
    """

    name = models.CharField(
        max_length=150,
        help_text="Nombre completo del autor"
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de nacimiento del autor"
    )

    class Meta:
        db_table = "author"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    ENTIDAD PARA RELACIÓN MUCHOS A MUCHOS

    Una categoría puede estar asociada a muchos libros
    y un libro puede tener múltiples categorías.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre de la categoría"
    )

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    ENTIDAD CENTRAL DEL DOMINIO

    Relaciones:
    - Muchos a Uno con Author
    - Muchos a Muchos con Category (con tabla intermedia)
    """

    title = models.CharField(
        max_length=200,
        help_text="Título del libro"
    )

    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="ISBN del libro"
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        help_text="Autor del libro (relación muchos a uno)"
    )

    published_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de publicación"
    )

    categories = models.ManyToManyField(
        Category,
        through="BookCategory",
        related_name="books",
        help_text="Categorías asociadas al libro (muchos a muchos)"
    )

    class Meta:
        db_table = "book"

    def __str__(self):
        return self.title


class BookCategory(models.Model):
    """
    ENTIDAD INTERMEDIA (ManyToMany con campos extra)

    Permite agregar información adicional a la relación
    libro ↔ categoría.
    """

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    assigned_at = models.DateField(
        auto_now_add=True,
        help_text="Fecha en que se asignó la categoría al libro"
    )

    priority = models.PositiveSmallIntegerField(
        default=1,
        help_text="Prioridad de la categoría dentro del libro"
    )

    class Meta:
        db_table = "book_category"
        unique_together = ("book", "category")

    def __str__(self):
        return f"{self.book.title} - {self.category.name}"