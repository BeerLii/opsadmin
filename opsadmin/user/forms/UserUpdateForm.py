from django import forms
from ..models.user import User

class UserUpdateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        obj = super(UserUpdateForm,self).__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['name','email','user_role','department','wechat','CellPhoneNumber','description']
