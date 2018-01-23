
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from repair.apps.login.models import CaseStudy
from repair.apps.asmfa.models import (Keyflow,
                                      KeyflowInCasestudy,
                                      Product,
                                      ProductFraction,
                                      Material,
                                      )

from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           InCasestudySerializerMixin,
                                           InCasestudyField,
                                           InCasestudyListField,
                                           IdentityFieldMixin,
                                           NestedHyperlinkedRelatedField,
                                           IDRelatedField)


class InCasestudyKeyflowListField(InCasestudyListField):
    """
    Field that returns a list of all items in the keyflow in the casestudy
    """
    lookup_url_kwarg = 'keyflow_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',
                            'keyflow_pk': 'id'}


class KeyflowSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {}
    casestudies = serializers.HyperlinkedRelatedField(
        queryset=CaseStudy.objects,
        many=True,
        view_name='casestudy-detail',
        help_text=_('Select the Casestudies the Keyflow is used in')
    )

    class Meta:
        model = Keyflow
        fields = ('url', 'id', 'code', 'name', 'casestudies',
                  )

    def update(self, instance, validated_data):
        """update the user-attributes, including profile information"""
        keyflow = instance

        # handle groups
        new_casestudies = validated_data.pop('casestudies', None)
        if new_casestudies is not None:
            ThroughModel = Keyflow.casestudies.through
            casestudy_qs = ThroughModel.objects.filter(
                keyflow=keyflow.id)
            # delete existing groups
            casestudy_qs.exclude(
                casestudy__id__in=(cs.id for cs in new_casestudies)).delete()
            # add or update new groups
            for cs in new_casestudies:
                ThroughModel.objects.update_or_create(keyflow=keyflow,
                                                      casestudy=cs)

        # update other attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        """Create a new Keyflow"""
        code = validated_data.pop('code')

        keyflow = Keyflow.objects.create(code=code)
        self.update(instance=keyflow, validated_data=validated_data)
        return keyflow


class InKeyflowField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk':
        'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id', }
    extra_lookup_kwargs = {}
    filter_field = 'keyflow_pk'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_pks_lookup['keyflow_pk'] = \
            self.parent_lookup_kwargs['keyflow_pk']


class InKeyflowSetField(IdentityFieldMixin, InKeyflowField, ):
    """Field that returns a list of all items in the casestudy"""
    lookup_url_kwarg = 'keyflow_pk'
    parent_lookup_kwargs = {
        'casestudy_pk': 'casestudy__id',
        'keyflow_pk': 'id', }


class KeyflowField(NestedHyperlinkedRelatedField):
    parent_lookup_kwargs = {'pk': 'id'}
    queryset = Keyflow.objects
    """This is fixed in rest_framework_nested, but not yet available on pypi"""
    def use_pk_only_optimization(self):
        return False


class KeyflowInCasestudySerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    note = serializers.CharField(required=False, allow_blank=True)
    casestudy = IDRelatedField()
    keyflow = KeyflowField(view_name='keyflow-detail')
    groupstock_set = InKeyflowSetField(view_name='groupstock-list')
    group2group_set = InKeyflowSetField(view_name='group2group-list')
    activitystock_set = InKeyflowSetField(view_name='activitystock-list')
    activity2activity_set = InKeyflowSetField(view_name='activity2activity-list')
    actorstock_set = InKeyflowSetField(view_name='actorstock-list')
    actor2actor_set = InKeyflowSetField(view_name='actor2actor-list')

    activitygroups = InCasestudyKeyflowListField(view_name='activitygroup-list')
    activities = InCasestudyKeyflowListField(view_name='activity-list')
    actors = InCasestudyKeyflowListField(view_name='actor-list')
    administrative_locations = InCasestudyKeyflowListField(
        view_name='administrativelocation-list')
    operational_locations = InCasestudyKeyflowListField(
        view_name='operationallocation-list')

    code = serializers.CharField(source='keyflow.code',
                                 allow_blank=True, required=False)
    name = serializers.CharField(source='keyflow.name',
                                 allow_blank=True, required=False)

    class Meta:
        model = KeyflowInCasestudy
        fields = ('url',
                  'id',
                  'keyflow',
                  'casestudy',
                  'note',
                  'groupstock_set',
                  'group2group_set',
                  'activitystock_set',
                  'activity2activity_set',
                  'actorstock_set',
                  'actor2actor_set',
                  'code',
                  'note',
                  'name',
                  'activitygroups',
                  'activities',
                  'actors',
                  'administrative_locations',
                  'operational_locations',
                  )


class KeyflowInCasestudyPostSerializer(InCasestudySerializerMixin,
                                       NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    note = serializers.CharField(required=False, allow_blank=True)
    keyflow = KeyflowField(view_name='keyflow-detail')

    class Meta:
        model = KeyflowInCasestudy
        fields = ('keyflow',
                  'note',
                  )


class KeyflowInCasestudyDetailCreateMixin:
    def create(self, validated_data):
        """Create a new solution quantity"""
        url_pks = self.context['request'].session['url_pks']
        keyflow_pk = url_pks['keyflow_pk']
        # ToDo: raise some kind of exception or prevent creating object with
        # wrong keyflow/casestudy combination somewhere else (view.update?)
        # atm the server will just hang up here
        mic = KeyflowInCasestudy.objects.get(id=keyflow_pk)
        validated_data['keyflow'] = mic

        obj = self.Meta.model.objects.create(
            **validated_data)
        return obj


class KeyflowInCasestudyField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',
                            }


class ProductInKeyflowInCasestudyField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }


class ProductFractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFraction
        fields = ('id',
                  'product',
                  'material',
                  'fraction')
        read_only_fields = ['id', 'product']


class ProductSerializer(KeyflowInCasestudyDetailCreateMixin,
                        NestedHyperlinkedModelSerializer):
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    fractions = ProductFractionSerializer(many=True)

    class Meta:
        model = Product
        fields = ('url', 'id', 'name', 'default',
                  'keyflow',
                  'fractions',
                  )

    def create(self, validated_data):
        fractions = validated_data.pop('fractions')
        instance = super().create(validated_data)
        validated_data['fractions'] = fractions
        self.update(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        """update the user-attributes, including fraction information"""
        product = instance

        # handle product fractions
        new_fractions = validated_data.pop('fractions', None)

        if new_fractions is not None:
            product_fractions = ProductFraction.objects.filter(product=product)
            # delete existing rows not needed any more
            fraction_materials = (
                getattr(fraction.get('material'), 'id')
                for fraction in new_fractions
                if getattr(fraction.get('material'), 'id') is not None)
            to_delete = product_fractions.exclude(
                material__id__in=fraction_materials)
            to_delete.delete()
            # add or update new fractions
            for new_fraction in new_fractions:
                material_id = getattr(new_fraction.get('material'), 'id')
                material = Material.objects.get(id=material_id)
                fraction = ProductFraction.objects.update_or_create(
                    product=product,
                    material=material)[0]

                for attr, value in new_fraction.items():
                    if attr in ('product', 'material'):
                        continue
                    setattr(fraction, attr, value)
                fraction.save()

        # update other attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MaterialSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {}

    class Meta:
        model = Material
        fields = ('url', 'id', 'name', 'code', 'flowType')