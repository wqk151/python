#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:myauth.py
@time:2017/3/9 0009 17:36
"""
from django.db import models
from  django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        """
                create and save a User with the given email,date of birth and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,email,name,password):
        """
        create and save a superuser with the given email,date of birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        user = self.create_user(email,password=password,name=name,)
        user.is_admin = True
        user.save(using = self._db)
        return user
class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=64,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    name = models.CharField(u'名字',max_length=32)
    token = models.CharField(u'token',max_length=128,default=None,blank=True,null=True)
    department = models.CharField(u'部门',max_length=32,default=None,blank=True,null=True)
    tel = models.CharField(u'座机',max_length=32,default=None,blank=True,null=True)
    mobile = models.CharField(u'手机',max_length=32,default=None,blank=True,null=True)
    memo = models.TextField(u'备注',blank=True,null=True,default=None)
    date_joined = models.DateTimeField(blank=True,auto_now_add=True)
    host_groups = models.ManyToManyField("HostGroup",blank=True)
    bind_hosts = models.ManyToManyField("BindHostToUser",blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def get_full_name(self):
        # the user is identified by their email address
        return self.email
    def get_short_name(self):
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission?"
        return  True
    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    @property
    def is_straff(self):
        "is the user a member of staff?"
        return self.is_admin
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'
    def __unicode__(self):
        return self.name
    objects = UserManager()