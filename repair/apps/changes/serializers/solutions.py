from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from repair.apps.changes.models import (Unit,
                                        SolutionCategory,
                                        Solution,
                                        SolutionQuantity,
                                        SolutionRatioOneUnit,
                                        )

from repair.apps.login.serializers import (InCasestudyField,
                                           UserInCasestudyField,
                                           InCaseStudyIdentityField,
                                           IdentityFieldMixin,
                                           CreateWithUserInCasestudyMixin)


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ('url', 'id', 'name')


class SolutionCategoryField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id'}


class SolutionField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk':
                            'solution_category__user__casestudy__id',
                            'solutioncategory_pk': 'solution_category__id', }
    extra_lookup_kwargs = {'casestudy_pk':
                           'implementation__user__casestudy__id'}


class SolutionSetField(InCasestudyField):
    """Returns a List of links to the solutions"""
    lookup_url_kwarg = 'solutioncategory_pk'
    parent_lookup_kwargs = {'casestudy_pk':
                            'solution_category__user__casestudy__id',
                            'solutioncategory_pk': 'solution_category__id', }


class SolutionListField(IdentityFieldMixin, SolutionSetField):
    """Returns a Link to the solutions--list view"""
    lookup_url_kwarg = 'solutioncategory_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id',
                            'solutioncategory_pk': 'id', }


class SolutionSetSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'solutioncategory_pk': 'solution_category__id',
                            'casestudy_pk':
                            'solution_category__user__casestudy__id', }

    class Meta:
        model = Solution
        fields = ('url', 'id', 'name')


class UnitField(serializers.HyperlinkedRelatedField):
    """A Unit Field"""
    queryset = Unit.objects


class SolutionCategorySerializer(CreateWithUserInCasestudyMixin,
                                 NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id'}
    solution_set = SolutionListField(
        view_name='solution-list')
    solution_list = SolutionSetField(
        source='solution_set',
        view_name='solution-detail',
        many=True,
        read_only=True,
    )
    user = UserInCasestudyField(
        view_name='userincasestudy-detail',
    )

    class Meta:
        model = SolutionCategory
        fields = ('url', 'id', 'name', 'user', 'solution_set', 'solution_list')
        read_only_fields = ('url', 'id')


class SolutionCategoryPostSerializer(SolutionCategorySerializer):
    class Meta:
        model = SolutionCategory
        fields = ('url', 'id', 'name', 'user', 'solution_set', 'solution_list')
        read_only_fields = ('url', 'id')


class SolutionDetailCreateMixin:
    def create(self, validated_data):
        """Create a new solution quantity"""
        url_pks = self.context['request'].session['url_pks']
        solution_pk = url_pks['solution_pk']
        solution = Solution.objects.get(id=solution_pk)

        obj = self.Meta.model.objects.create(
            solution=solution,
            **validated_data)
        return obj


class SolutionQuantitySerializer(SolutionDetailCreateMixin,
                                 NestedHyperlinkedModelSerializer):
    unit = UnitField(view_name='unit-detail')
    solution = SolutionField(view_name='solution-detail', read_only=True)
    parent_lookup_kwargs = {
        'casestudy_pk': 'solution__user__casestudy__id',
        'solutioncategory_pk': 'solution__solution_category__id',
        'solution_pk': 'solution__id',
    }

    class Meta:
        model = SolutionQuantity
        fields = ('url', 'id', 'name', 'unit', 'solution')


class SolutionDetailListField(InCaseStudyIdentityField):
    lookup_url_kwarg = 'solution_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'user__casestudy__id',
                            'solutioncategory_pk': 'solution_category__id',
                            'solution_pk': 'id',
                            }


class SolutionRatioOneUnitSerializer(SolutionDetailCreateMixin,
                                     NestedHyperlinkedModelSerializer):
    unit = UnitField(view_name='unit-detail')
    solution = SolutionField(view_name='solution-detail', read_only=True)
    value = serializers.DecimalField(max_digits=10, decimal_places=3)
    parent_lookup_kwargs = {
        'casestudy_pk': 'solution__user__casestudy__id',
        'solutioncategory_pk': 'solution__solution_category__id',
        'solution_pk': 'solution__id',
    }

    class Meta:
        model = SolutionRatioOneUnit
        fields = ('url', 'id', 'name', 'value', 'unit', 'solution')


class SolutionSerializer(CreateWithUserInCasestudyMixin,
                         NestedHyperlinkedModelSerializer):

    parent_lookup_kwargs = {
        'casestudy_pk': 'user__casestudy__id',
        'solutioncategory_pk': 'solution_category__id',
    }
    user = UserInCasestudyField(view_name='userincasestudy-detail')
    solution_category = SolutionCategoryField(
        view_name='solutioncategory-detail')
    solutionquantity_set = SolutionDetailListField(
        view_name='solutionquantity-list')
    solutionratiooneunit_set = SolutionDetailListField(
        view_name='solutionratiooneunit-list')

    class Meta:
        model = Solution
        fields = ('url', 'id', 'name', 'user', 'description',
                  'one_unit_equals', 'solution_category',
                  'solutionquantity_set',
                  'solutionratiooneunit_set',
                  )
        read_only_fields = ('url', 'id', )