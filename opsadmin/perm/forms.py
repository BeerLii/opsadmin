from django import forms
from asset.models import asset_group
from .models import perm


class perm_form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(perm_form, self).__init__(*args, **kwargs)
        self.fields['descriptions'].required = False
        self.user_obj = kwargs.get('instance')
        self.fields['system_user_choices'].queryset = self.user_obj.SystemUser_ID.all()



    system_user_choices = forms.ModelChoiceField(queryset=None,required=True)
    asset_group_choices = forms.ModelChoiceField(queryset=asset_group.AssetGroup.objects.all(),required=True)

    class Meta:
        model = perm
        fields = ['name','perm','descriptions']

    def clean(self):
        if(len(perm.objects.filter(SystemUser=self.cleaned_data['system_user_choices'],asset_group=self.cleaned_data['asset_group_choices'])) != 0):
            raise forms.ValidationError('该用户和资产组已经创建过权限了')
        return super(perm_form,self).clean()




