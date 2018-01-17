from django import forms
from ..models.asset_group import AssetGroup
from ..models.asset import Asset



class AssetGroupForm(forms.ModelForm):
    asset_choices = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,queryset=Asset.objects.all(),required=True)

    def __init__(self,*args,**kwargs):
        super(AssetGroupForm, self).__init__(*args, **kwargs)

        self.fields['descriptions'].required = False


    class Meta:
        model=AssetGroup
        fields = ['name','descriptions']

    def clean_asset_choices(self):
        asset_choices = self.cleaned_data['asset_choices']
        return asset_choices

    def save(self, commit=True):
        AssetGroupObj = super(AssetGroupForm, self).save(commit=False)
        if commit:
            AssetGroupObj.save()

        for asset_obj in self.cleaned_data['asset_choices']:

            asset_obj.asset_group.add(AssetGroupObj)
        return AssetGroupObj
