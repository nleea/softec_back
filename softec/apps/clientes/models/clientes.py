from django.db import models
from .managers.client_managers import ClienteManagers
from django.core.validators import EmailValidator, MinValueValidator, MinLengthValidator
from datetime import date


class Cliente(models.Model):
    nombre_completo = models.CharField(
        max_length=256,
        db_index=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        validators=[EmailValidator()],
        help_text="Por favor, introduce una dirección de correo electrónico válida.",
    )
    fecha_nacimiento = models.DateField(
        validators=[MinValueValidator(limit_value=date(1950, 1, 1))],
        blank=False,
        null=False,
        help_text="La fecha no puede ser inferios a 1950-1-1",
    )
    numero_documento = models.CharField(
        validators=[MinLengthValidator(8)],
        blank=False,
        null=False,
        unique=True,
        help_text="El campo debe ser mayor a 8 digitos",
        max_length=12
    )
    fecha_creacion = models.DateField(auto_now_add=True,db_index=True)
    visible = models.BooleanField(default=True)

    objects = models.Manager()
    objects_ = ClienteManagers()
    
    def soft_delete(self):
        self.visible = False
        self.save()

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["-id"]
