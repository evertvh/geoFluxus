from django.utils.translation import ugettext_lazy as _
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from repair.apps.changes.models import (Implementation,
                                        SolutionInImplementation,
                                        SolutionInImplementationNote,
                                        SolutionInImplementationQuantity,
                                        SolutionInImplementationGeometry,
                                        )

from repair.apps.login.serializers import (InCasestudyField,
                                           UserInCasestudyField,
                                           InSolutionField,
                                           InCaseStudyIdentityField,
                                           IdentityFieldMixin,
                                           CreateWithUserInCasestudyMixin)


from .solutions import SolutionField


class SolutionInImplementationSetField(InCasestudyField):
    """Returns a list of links to the solutions"""
    lookup_url_kwarg = 'implementation_pk'
    parent_lookup_kwargs = {
        'casestudy_pk': 'implementation__user__casestudy__id',
        'implementation_pk': 'implementation__id', }


class SolutionIISetField(InCasestudyField):
    """Returns a list of links to the solutions"""
    lookup_url_kwarg = 'solutioncategory_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id',
                            'solutioncategory_pk': 'id', }


class SolutionInImplementationsListField(IdentityFieldMixin,
                                         SolutionInImplementationSetField):
    """Returns a Link to the solutions--list view"""
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id',
                            'implementation_pk': 'id', }


class StakeholderOfImplementationField(InCaseStudyIdentityField):
    lookup_url_kwarg = 'pk'
    parent_lookup_kwargs = {
        'casestudy_pk': 'user__casestudy__id',
        'pk': 'coordinating_stakeholder__id',
        'stakeholdercategory_pk':
        'coordinating_stakeholder__stakeholder_category__id', }


class ImplementationSerializer(CreateWithUserInCasestudyMixin,
                               NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id'}
    solution_list = SolutionInImplementationsListField(
        source='solutioninimplementation_set',
        view_name='solutioninimplementation-list')
    sii_set = SolutionInImplementationSetField(
        source='solutioninimplementation_set',
        view_name='solutioninimplementation-detail',
        many=True,
        read_only=True)
    solution_set = SolutionIISetField(
        source='solutions',
        view_name='solution-detail',
        many=True)
    coordinating_stakeholder = StakeholderOfImplementationField(
        view_name='stakeholder-detail')
    user = UserInCasestudyField(
        view_name='userincasestudy-detail')

    class Meta:
        model = Implementation
        fields = ('url', 'id', 'name', 'user',
                  'coordinating_stakeholder',
                  'solution_set',
                  'solution_list',
                  'sii_set',
                  )

    def update(self, instance, validated_data):
        """
        update the implementation-attributes,
        including selected solutions
        """
        implementation = instance

        # handle solutions
        new_solutions = validated_data.pop('solutions', None)
        if new_solutions is not None:
            SolutionInImplementationModel = Implementation.solutions.through
            solution_qs = SolutionInImplementationModel.objects.filter(
                implementation=implementation)
            # delete existing solutions
            solution_qs.exclude(solution_id__in=(
                sol.id for sol in new_solutions)).delete()
            # add or update new solutions
            for sol in new_solutions:
                SolutionInImplementationModel.objects.update_or_create(
                    implementation=implementation,
                    solution=sol)

        # update other attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ImplementationOfUserSerializer(ImplementationSerializer):
    """"""
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id',
                            'user_pk': 'user__id', }


class ImplementationField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id'}
    extra_lookup_kwargs = {'casestudy_pk':
                           'implementation__user__casestudy__id'}


class SolutionInImplementationDetailListField(InCaseStudyIdentityField):
    lookup_url_kwarg = 'solution_pk'
    parent_lookup_kwargs = {'casestudy_pk':
                            'implementation__user__casestudy__id',
                            'implementation_pk': 'implementation__id',
                            'solution_pk': 'id',
                            }


class SolutionInImplementationSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk':
                            'implementation__user__casestudy__id',
                            'implementation_pk': 'implementation__id',
                            }
    implementation = ImplementationField(
        view_name='implementation-detail')
    solution = SolutionField(view_name='solution-detail')
    solutioninimplementationnote_set = SolutionInImplementationDetailListField(
        view_name='solutioninimplementationnote-list')
    solutioninimplementationquantity_set = SolutionInImplementationDetailListField(
        view_name='solutioninimplementationquantity-list')
    solutioninimplementationgeometry_set = SolutionInImplementationDetailListField(
        view_name='solutioninimplementationgeometry-list')

    class Meta:
        model = SolutionInImplementation
        fields = ('url', 'id',
                  'implementation',
                  'solution',
                  'solutioninimplementationnote_set',
                  'solutioninimplementationquantity_set',
                  'solutioninimplementationgeometry_set',
                  )


class SolutionInImplementationField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk': 'implementation__user__casestudy__id',
        'implementation_pk': 'implementation__id', }


class SolutionInImplementationDetailCreateMixin:
    def create(self, validated_data):
        """Create a new solution quantity"""
        url_pks = self.context['request'].session['url_pks']
        solution_pks = url_pks['solution_pk']
        sii = SolutionInImplementation.objects.get(id=solution_pks)

        obj = self.Meta.model.objects.create(
            sii=sii,
            **validated_data)
        return obj


class SolutionInImplementationNoteSerializer(SolutionInImplementationDetailCreateMixin,
                                             NestedHyperlinkedModelSerializer):
    sii = SolutionInImplementationField(
        view_name='solutioninimplementation-detail',
        read_only=True)
    parent_lookup_kwargs = {
        'casestudy_pk': 'sii__implementation__user__casestudy__id',
        'implementation_pk': 'sii__implementation__id',
        'solution_pk': 'sii__id', }

    class Meta:
        model = SolutionInImplementationNote
        fields = ('url', 'id', 'note', 'sii')


class SolutionQuantityField(InSolutionField):
    parent_lookup_kwargs = {'casestudy_pk':
                            'solution__solution_category__user__casestudy__id',
                            'solutioncategory_pk': 'solution__solution_category__id',
                            'solution_pk': 'solution__id', }


class SolutionInImplementationQuantitySerializer(SolutionInImplementationNoteSerializer):
    quantity = SolutionQuantityField(view_name='solutionquantity-detail',
                                     help_text=_('the quantity to define'),
                                     label=_('Solution Quantity'),
                                     read_only=True)

    class Meta:
        model = SolutionInImplementationQuantity
        fields = ('url', 'id', 'quantity', 'value', 'sii')
        read_only_fields = ('quantity', 'sii')


class SolutionInImplementationGeometrySerializer(SolutionInImplementationNoteSerializer):
    class Meta:
        model = SolutionInImplementationGeometry
        fields = ('url', 'id', 'name', 'geom', 'sii')
