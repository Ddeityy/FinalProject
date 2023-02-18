from rest_framework import viewsets, permissions
from .serializers import *
from app.models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseForbidden


# all methods
class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request, pk=None):
        q = Car.objects.get(id=pk)
        s = None
        if (
            self.request.user.id == (q.buyer.id or q.service_company.id)
        ) or self.request.user.groups.filter(name="manager").exists():
            s = CarSerializer(q)
        else:
            s = LimitedCarSerializer(q)
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        q = Car.objects.all()
        s = None
        if self.request.user.groups.filter(name="manager").exists():
            s = CarSerializer(q, many=True)
        else:
            s = LimitedCarSerializer(q, many=True)
        return Response(s.data)


class MaitenanceViewSet(viewsets.ModelViewSet):
    queryset = Maitenance.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]
    serializer_class = MaitenanceSerializer

    def retrieve(self, request, pk=None):
        q = Maitenance.objects.get(id=pk)
        s = None
        if (
            self.request.user.id == (q.car.buyer.id or q.service_company.id)
        ) or self.request.user.groups.filter(name="manager").exists():
            s = CarSerializer(q)
        else:
            Response(status=HttpResponseForbidden)
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        q = None
        if self.request.user.groups.filter(name="client").exists():
            q = Maitenance.objects.filter(car__buyer=request.user.id)
        elif self.request.user.groups.filter(name="service company").exists():
            q = Maitenance.objects.filter(service_company=request.user.id)
        elif self.request.user.groups.filter(name="manager").exists():
            q = Maitenance.objects.all()
        else:
            return Response(status=HttpResponseForbidden)
        s = MaitenanceSerializer(q, many=True)
        return Response(s.data)


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def retrieve(self, request, pk=None):
        q = Repair.objects.get(id=pk)
        s = None
        if (
            self.request.user.id == (q.car.buyer.id or q.service_company.id)
        ) or self.request.user.groups.filter(name="manager").exists():
            s = CarSerializer(q)
        else:
            Response(status=HttpResponseForbidden)
        return Response(s.data)

    def list(self, request, *args, **kwargs):
        q = Repair.objects.all()
        if self.request.user.groups.filter(name="client").exists():
            q = Repair.objects.filter(car__buyer=request.user.id)
        elif self.request.user.groups.filter(name="service company").exists():
            q = Repair.objects.filter(service_company=request.user.id)
        s = RepairSerializer(q, many=True)
        return Response(s.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    @action(detail=False)
    def cars(self, request):
        q = Car.objects.all()
        if self.request.user.groups.filter(name="client").exists():
            q = Car.objects.filter(buyer=request.user.id)
        elif self.request.user.groups.filter(name="service company").exists():
            q = Car.objects.filter(service_company=request.user.id)
        s = CarSerializer(q, many=True)
        return Response(s.data)

    @action(detail=False)
    def maitenance(self, request):
        q = Maitenance.objects.all()
        if self.request.user.groups.filter(name="client").exists():
            q = Maitenance.objects.filter(car__buyer=request.user.id)
        elif self.request.user.groups.filter(name="service company").exists():
            q = Maitenance.objects.filter(service_company=request.user.id)
        s = MaitenanceSerializer(q, many=True)
        return Response(s.data)

    @action(detail=False)
    def repair(self, request):
        q = Repair.objects.all()
        if self.request.user.groups.filter(name="client").exists():
            q = Repair.objects.filter(car__buyer=request.user.id)
        elif self.request.user.groups.filter(name="service company").exists():
            q = Repair.objects.filter(service_company=request.user.id)
        s = RepairSerializer(q, many=True)
        return Response(s.data)
