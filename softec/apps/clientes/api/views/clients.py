from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from ...models import Cliente
from ..serializers.client_serializers import clientSerializersView, clientSerializers


class ClienteListaView(APIView):
    def get(self, request, *args, **kwargs):
        fecha = request.GET.get("fecha", None)
        nombre = request.GET.get("nombre", None)
        
        if fecha:
            cliente_querySet_filter = Cliente.objects_.filtra_fecha(fecha)
            resulst_serializers = clientSerializersView(cliente_querySet_filter, many=True)
            return Response(
                resulst_serializers.data,
                content_type="application/json",
                status=HTTP_200_OK,
        )
            
        if nombre:
            cliente_querySet_filter = Cliente.objects_.filtra_nombre(nombre)
            resulst_serializers = clientSerializersView(cliente_querySet_filter, many=True)
            return Response(
                resulst_serializers.data,
                content_type="application/json",
                status=HTTP_200_OK,
        )

        cliente_querySet = Cliente.objects_.get_queryset()
        resulst_serializers = clientSerializersView(cliente_querySet, many=True)

        return Response(
            resulst_serializers.data,
            content_type="application/json",
            status=HTTP_200_OK,
        )


class ClienteCrear(APIView):
    http_method_names = ["post"]

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def post(self, request, *args, **kwargs):
        resulst_serializers = clientSerializers(data=request.data)

        if resulst_serializers.is_valid():
            resulst_serializers.save()
            return Response(
                {"message": "Cliente guardado exitisamente", "ok": True},
                content_type="application/json",
                status=HTTP_200_OK,
            )

        return Response(
            {"message": resulst_serializers.errors, "ok": False},
            content_type="application/json",
            status=HTTP_400_BAD_REQUEST,
        )


class ClienteActualizar(APIView):
    http_method_names = ["put"]

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def get_object(self):
        try:
            pk = self.kwargs.get("pk", None)
            return Cliente.objects_.get_model(pk)
        except Cliente.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {"message": "Este registro no existe", "ok": False},
                content_type="application/json",
                status=HTTP_404_NOT_FOUND,
            )

        resulst_serializers = clientSerializers(
            data=request.data, instance=instance, partial=True
        )

        if resulst_serializers.is_valid():
            resulst_serializers.save()
            return Response(
                {"message": "Cliente actualizado exitisamente", "ok": True},
                content_type="application/json",
                status=HTTP_200_OK,
            )

        return Response(
            {"message": resulst_serializers.errors, "ok": False},
            content_type="application/json",
            status=HTTP_400_BAD_REQUEST,
        )


class ClienteEliminar(APIView):
    http_method_names = ["delete"]

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def get_object(self):
        try:
            pk = self.kwargs.get("pk", None)
            return Cliente.objects_.get_model(pk)
        except Cliente.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {"message": "Este registro no existe", "ok": False},
                content_type="application/json",
                status=HTTP_404_NOT_FOUND,
            )

        instance.soft_delete()

        return Response(
            {"message": "Registro eliminado exitosamente", "ok": True},
            content_type="application/json",
            status=HTTP_200_OK,
        )
