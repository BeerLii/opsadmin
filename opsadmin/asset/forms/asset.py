from django.forms import ModelForm
from ..models.asset import Asset

class AssetCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetCreateForm, self).__init__(*args, **kwargs)

        print(self.instance)
        self.fields['descriptions'].required = False

    class Meta:
        model = Asset
        fields = ['descriptions','asset_type','manage_ip','external_ip','name','asset_env']


