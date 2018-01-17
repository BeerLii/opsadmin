from django import forms
from ..models.user import SystemUser
from django.utils import timezone
from ..util import prpcrypt
from common import util
from opsadmin import settings
import base64

class SystemUserCreateForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput, max_length=100,required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=100,required=False)


    class Meta:
        model = SystemUser
        fields = ['description','name','UserName','private_key']

    def clean_password2(self):
        # Check that the two password entries match

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password1

    def clean_private_key(self):
        private_key = self.cleaned_data.get('private_key')


        return private_key


    def clean(self):
        private_key = self.cleaned_data.get('private_key')
        if not self.cleaned_data.get('password1') and not self.cleaned_data.get('password2') and not private_key:
            raise forms.ValidationError('plz input password or key file')

        return super(SystemUserCreateForm,self).clean()

    def save(self, commit=True):
        user = super(SystemUserCreateForm, self).save(commit=False)
        t = timezone.now()
        if self.cleaned_data['password1']:

            pc = prpcrypt(settings.SECRET_KEY[0:16])
            user.get_password = base64.b64encode(pc.encrypt(self.cleaned_data['password1'])).decode('utf-8')
        user.CreateTime = t
        if self.cleaned_data.get('private_key'):
            public_key = util.ssh_pubkey_gen(private_key=self.cleaned_data['private_key'],username=self.cleaned_data['UserName'])
            user.public_key = public_key
        obj = self.cleaned_data['request'].user
        if commit:
            user.save()
        obj.SystemUser_ID.add(user)
        obj.save()
        return user

