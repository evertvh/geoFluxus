from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from repair.apps.studyarea.models import (StakeholderCategory,
                                          Stakeholder,
                                          AdminLevels,
                                          Area,
                                          )
from repair.apps.login.models import CaseStudy
from repair.apps.login.serializers import (CaseStudySerializer,
                                           InCasestudyField,
                                           InCaseStudyIdentityField,
                                           IdentityFieldMixin,
                                           CreateWithUserInCasestudyMixin)



class StakeholderCategoryField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}


class StakeholderSetField(InCasestudyField):
    lookup_url_kwarg = 'stakeholdercategory_pk'
    parent_lookup_kwargs = {
        'casestudy_pk': 'stakeholder_category__casestudy__id',
        'stakeholdercategory_pk': 'stakeholder_category__id', }


class StakeholderListField(IdentityFieldMixin, StakeholderSetField):
    """"""
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',
                            'stakeholdercategory_pk': 'id', }


class StakeholderSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'stakeholder_category__casestudy__id',
        'stakeholdercategory_pk': 'stakeholder_category__id',
    }
    stakeholder_category = StakeholderCategoryField(
        view_name='stakeholdercategory-detail'
    )

    class Meta:
        model = Stakeholder
        fields = ('url', 'id', 'name', 'stakeholder_category')


class StakeholderSetSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'stakeholder_category__casestudy__id',
        'stakeholdercategory_pk': 'stakeholder_category__id',
    }
    class Meta:
        model = Stakeholder
        fields = ('url', 'id', 'name')


class StakeholderCategorySerializer(CreateWithUserInCasestudyMixin,
                                    NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    stakeholder_list = StakeholderListField(source='stakeholder_set',
                                            view_name='stakeholder-list')
    stakeholder_set = StakeholderSetField(many=True,
                                          view_name='stakeholder-detail',
                                          read_only=True)

    class Meta:
        model = StakeholderCategory
        fields = ('url', 'id', 'name', 'stakeholder_set', 'stakeholder_list',
                  )

    def get_required_fields(self, user, kic=None):
        required_fields = {'casestudy': user.casestudy,}
        return required_fields


class AdminLevelSerializer(CreateWithUserInCasestudyMixin,
                           NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    #level = serializers.IntegerField(source='_level')

    class Meta:
        model = AdminLevels
        fields = ('url', 'id', 'casestudy', 'name', 'level',
                  )


class AreaSerializer(CreateWithUserInCasestudyMixin,
                     NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',
                            'level_pk': 'level',}

    class Meta:
        model = Area
        fields = ('url', 'id', 'casestudy', 'name', 'level',
                  )
