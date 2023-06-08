from django.urls import path,re_path
from .clients import ClienteEliminar, ClienteListaView, ClienteCrear, ClienteActualizar

urlpatterns = [
    re_path(r"(?P<fecha>)(?P<nombre>)$", ClienteListaView.as_view()),
    path("crear/", ClienteCrear.as_view()),
    path("actualizar/<int:pk>/", ClienteActualizar.as_view()),
    path("eliminar/<int:pk>/", ClienteEliminar.as_view()),
]
