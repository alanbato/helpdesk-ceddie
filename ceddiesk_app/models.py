from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Adviser(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=128, blank=True, null=True)
    nomina = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format("Asesor", self.nomina, self.name)

    def __repr__(self):
        return str(self)


class Teacher(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=128, blank=True, null=True)
    nomina = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format("Maestro", self.nomina, self.name)

    def __repr__(self):
        return str(self)


class Request(models.Model):
    REQUEST_TYPE = (
        ("TECNO", "Asesoría Tecnológica"),
        ("PLAT", "Asesoría de Plataforma"),
        ("PEDAG", "Asesoría Pedagógica"),
        ("CAPA", "Asesoría de Capacitación"),
        ("CADIS", "Solicitudes de CADIS"),
        ("COPIA", "Copia de Plataforma"),
        ("ESPA", "Espacio de Plataforma"),
        ("CUEN", "Cuenta de Plataforma"),
        ("ENRL", "Enrolamiento de Plataforma"),
    )
    ADVICE_TYPE = (
        ("EMA", "Solicitud por Email"),
        ("TEL", "Solicitud por Teléfono"),
        ("PRES", "Solicitud Presencial"),
        ("ONL", "En Línea"),
    )
    PLATFORM_TYPE = (("BLACK", "Blackboard"), ("CANV", "Canvas"), ("OTHER", "Otra"))
    REQUEST_STATUS = (
        ("PEND", "Pendiente"),
        ("PROG", "En Profreso"),
        ("RESG", "Reasignado"),
        ("TERM", "Terminado"),
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name="requests",
        related_query_name="request",
        null=True,
    )
    adviser = models.ForeignKey(
        Adviser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="requests",
        related_query_name="request",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=5, choices=REQUEST_STATUS, default="PEND")
    request_type = models.CharField(max_length=5, choices=REQUEST_TYPE, default="PLAT")
    advice_type = models.CharField(max_length=5, choices=ADVICE_TYPE, default="PRES")
    platform_type = models.CharField(
        max_length=5, choices=PLATFORM_TYPE, default="BLACK"
    )
    description = models.TextField()
    course_name = models.CharField(max_length=100, blank=True, null=True)
    course_id = models.CharField(max_length=10, blank=True, null=True)
    reassigned_ticket = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "{} {}".format("Solicitud", self.id)

    def __repr__(self):
        return str(self)


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="comments",
        related_query_name="comment",
        null=True,
    )
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return "{} {} {} {}".format(
            "Comentario", self.id, "de la solicitud", self.solicitud.id
        )

    def __repr__(self):
        return str(self)
