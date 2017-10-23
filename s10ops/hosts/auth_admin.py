#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:auth_admin.py
@time:2017/3/9 0009 17:34
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from myauth import UserProfile
from django.contrib.auth import forms as auth_form

class UserCreationForm(forms.ModelForm):
    """A form for creating new users.Includes all the required fields,plus a repeated password."""
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)
    class Meta:
        model = UserProfile
        fields = ('email','token')
    def clean_password2(self):
        # check that the two password entries  match
        password1 = self.cleaned_data.get('password1')
        password2 = self.changed_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # save the provieded password in hashed format
        user = super(UserCreationForm,self).save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
"""
label参数让你指定字段"对人类友好"的label。当字段在表单中显示时用到它。
http://python.usyiyi.cn/translate/django_182/ref/forms/fields.html#built-in-fields
widget是Django对HTML输入元素的表示。widget负责渲染HTML和提取GET/POST字典中的数据。
http://python.usyiyi.cn/translate/django_182/ref/forms/widgets.html
"""

class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.Includes all the fields on the user,but replaces the password field with admin's password hash display field.
    """
    password  = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored,so there is no way to see"
                   "this user's password,but you can change the password"
                   "using <a href=\"password/\">this form</a>."))
    class Meta:
        model = UserProfile
        fields = ('email','password','is_active','is_admin')
    def clean_password(self):
        # Regardless of what the user provides,return the initial value
        # This is done here,rather than on the field,because the field does not have access to the initial value
        return self.initial['password']

class UserProfileAdmin(UserAdmin):
    # the forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the user model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.user.
    list_display = ('email','is_admin','name','department','tel')
    list_filter = (
        (None,{'fields':('email','password')}),
        ('Personal info',{'fields':('department','tel','mobile','memo')}),
        ('API TOKEN info',{'fields':('token',)}),
        (u'可管理的主机组',{'fields':('host_groups',)}),
        (u'可管理的主机',{'fields':('bind_hosts',)}),
        ('Permissions',{'fields':('is_active','is_admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2','is_active','is_admin')
        }),
    )

    search_fields = ('email','department')
    ordering = ('email','department')
    filter_horizontal = ('bind_hosts','host_groups')


