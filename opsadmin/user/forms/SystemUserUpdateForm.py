from django import forms
from ..models.user import SystemUser
from django.utils.translation import ugettext as _

class SystemUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        obj = super(SystemUserUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})
            field.label = _(field_name)

    class Meta:
        model = SystemUser
        fields = ['name','description']

