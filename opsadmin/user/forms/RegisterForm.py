from django import forms
from ..models.user import User
from ..models.permission import Permission

class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(widget = forms.PasswordInput,max_length=100)
    password2 = forms.CharField(widget = forms.PasswordInput,max_length=100)
    department = forms.CharField(max_length=30,widget=forms.Select(choices=User.DEPARTMENT_CHOICES))

    class Meta:
        model = User

        fields = ['username','email','wechat','CellPhoneNumber','name','user_role','description']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username has exists")
        return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("name has exists")
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email has exists")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2:
            raise forms.ValidationError('Passwords is empty')
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1


    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.get_department = self.cleaned_data['department']
        if commit:
            user.save()

        permission_obj = Permission(user=user)
        permission_obj.save()
        return user


