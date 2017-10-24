# API View
from django.http import Http404, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from collections import OrderedDict
from django.http import Http404

from repair.apps.asmfa.models import (
    ActivityGroup, Activity, Actor, Flow,
    Activity2Activity, Actor2Actor, Group2Group)
from repair.apps.asmfa.serializers import (
    ActivityGroupSerializer, ActivitySerializer,
    ActorSerializer, FlowSerializer)
from django.shortcuts import get_object_or_404


class ActivityGroupViewSet(ViewSet):
    serializer_class = ActivityGroupSerializer

    def list(self, request, casestudy_pk=None):
        queryset = ActivityGroup.objects.filter(case_study=casestudy_pk)
        serializer = ActivityGroupSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, casestudy_pk=None):
        queryset = ActivityGroup.objects.filter(pk=pk, case_study=casestudy_pk)
        activitygroup = get_object_or_404(queryset, pk=pk)
        serializer = ActivityGroupSerializer(activitygroup)
        return Response(serializer.data)


class ActivityViewSet(ViewSet):
    serializer_class = ActivitySerializer

    def list(self, request, casestudy_pk=None, activitygroup_pk=None):
        queryset = Activity.objects.filter(
            own_activitygroup=activitygroup_pk)
        serializer = ActivitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, casestudy_pk=None,
                 activitygroup_pk=None):
        queryset = Activity.objects.filter(
            pk=pk, own_activitygroup=activitygroup_pk)
        activity = get_object_or_404(queryset, pk=pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)


class ActorViewSet(ViewSet):
    serializer_class = ActorSerializer
    
    def get_nace(self, activity_pk, activitygroup_pk):
        queryset = Activity.objects.filter(
            pk=activity_pk, own_activitygroup=activitygroup_pk)
        activity = get_object_or_404(queryset, pk=activity_pk)
        return activity.nace

    def list(self, request, casestudy_pk=None, activitygroup_pk=None,
             activity_pk=None):
        nace = self.get_nace(activity_pk, activitygroup_pk)
        queryset = Actor.objects.filter(own_activity=nace)
        serializer = ActorSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, casestudy_pk=None,
                 activitygroup_pk=None, activity_pk=None):
        nace = self.get_nace(activity_pk, activitygroup_pk)
        queryset = Actor.objects.filter(pk=pk, own_activity=nace)
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorSerializer(actor)
        return Response(serializer.data)


class MaterialViewSet(ViewSet):
    def list(self, request, casestudy_pk=None):
        materials = Flow.material_choices
        data = [OrderedDict([('id', m[0]), ('name', m[1])]) for m in materials]
        return Response(data)
    
    def retrieve(self, request, pk=None, casestudy_pk=None):
        materials = Flow.material_choices
        for m in materials:
            if m[0] == pk:
                data = OrderedDict([('id', m[0]), ('name', m[1])])
                return Response(data)
        raise Http404('No matches for the given query.')


class FlowViewSet(ViewSet):
    serializer_class = FlowSerializer
    model = None
    
    def list(self, request, casestudy_pk=None, material_pk=None):
        queryset = self.model.objects.filter(
            case_study=casestudy_pk, material=material_pk)
        serializer = FlowSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, casestudy_pk=None, material_pk=None):
        queryset = self.model.objects.filter(
            pk=pk, case_study=casestudy_pk, material=material_pk)
        flow = get_object_or_404(queryset, pk=pk)
        serializer = FlowSerializer(flow)
        return Response(serializer.data)


class Group2GroupViewSet(FlowViewSet):
    model = Group2Group
    
class Activity2ActivityViewSet(FlowViewSet):
    model = Actor2Actor
    
class Actor2ActorViewSet(FlowViewSet):
    model = Activity2Activity