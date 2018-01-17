from ..models import permission
from user.models.user import User
from django import forms

class PermissionForm(forms.ModelForm):
    def __init__(self):
        self.fields['AssetEnable'].required = False
        self.fields['PermEnable'].required = False

    username = forms.ModelChoiceField(queryset=User.objects.filter(admin_active=False),required=True)
    class Meta:
        model = permission
        fields = ['AssetEnable','PermEnable']


