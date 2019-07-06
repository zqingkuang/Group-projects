from .models import *
from django import forms


class LoginForm(forms.ModelForm):
    pw = forms.CharField(max_length=16, min_length=6, error_messages={'max_length': '密码最大长度为16',
                                                                      'min_length': '密码最小长度为6'})

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'sex', 'phone']

    def clean_username(self):
        ul = self.cleaned_data.get('username')
        if UserModel.objects.filter(username=ul).exists():
            raise forms.ValidationError('用户已存在')
        else:
            return ul

    def clean(self):
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('pw')
        if pw1 != pw2:
            raise forms.ValidationError('两次密码输入不一致')

    def get_data(self):
        e_dict = self.errors.get_json_data()
        r_dict = {}
        for k, v in e_dict.items():
            r_list = []
            for i in v:
                msg = i["message"]
                r_list.append(msg)
            r_dict[k] = r_list
        return r_dict


class loginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'sex', 'phone']

    def clean(self):
        ul = self.cleaned_data.get('username')
        phone = self.cleaned_data.get('phone')
        if not UserModel.objects.filter(username=ul,phone=phone).exists():
            return forms.ValidationError('用户不存在')






