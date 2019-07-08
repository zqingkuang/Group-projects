from .models import *
from django import forms


class Register(forms.ModelForm):
    pw = forms.CharField(max_length=20, min_length=8, error_messages={'max_length': '密码最大长度为20',
                                                                      'min_length': '密码最小长度为8'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # def clean_username(self):
    #     user= self.cleaned_data.get("username")
    #     if User.objects.filter(username=user).exists():
    #         raise forms.ValidationError('用户已存在')

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        cpwd = self.cleaned_data.get('cpwd')
        if pwd!=cpwd:
            raise forms.ValidationError('两次输入密码不一致')




