from django.db import models

class ClienteManagers(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(visible=True)
    
    def get_model(self,id:int):
        return self.get(id=id)
    
    def filtra_fecha(self,fecha):
        return self.filter(fecha_creacion__exact=fecha)
    
    def filtra_nombre(self,nombre):
        return self.filter(nombre_completo__icontains=nombre)
    
    def filtra_nombre_exact(self,nombre):
        return self.filter(nombre_completo__exact=nombre)
