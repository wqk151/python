# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Host(models.Model):
    hostname = models.CharField(max_length=64)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey('IDC')
    system_type_choice=(
        ('linux','Linux'),
        ('windows','Windows')
    )
    system_type = models.CharField(choices=system_type_choice,max_length=32,default='linux')
    enabled = models.BooleanField(default=True)
    memo = models.TextField(blank=True,null=True)   #备忘录
    date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s(%s)" % (self.hostname,self.ip_addr)
    class Meta:
        verbose_name = u'主机列表'
        verbose_name_plural = u'主机列表'
class IDC(models.Model):
    name = models.CharField(unique=True,max_length=64)
    memo = models.TextField(blank=True,null=True)
    def __unicode__(self):
        return self.name
class HostUser(models.Model):
    auth_type_choices = (
        ('ssh-password','SSH/PASSWORD'),
        ('ssh-key','SSH/KEY')
    )
    auth_type = models.CharField(choices=auth_type_choices,max_length=32,default='ssh-password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128,blank=True,null=True)

    def __unicode__(self):
        return "(%s)%s" %(self.auth_type,self.username)
    class Meta:
        unique_together = ('auth_type','username','password')
        verbose_name = u'远程主机用户'
        verbose_name_plural = u'远程主机用户'
class HostGroup(models.Model):
    name = models.CharField(unique=True,max_length=64)
    memo = models.TextField(blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u'主机组'
class BindHostToUser(models.Model):
    host = models.ForeignKey('Host')
    host_user = models.ForeignKey('HostUser')
    host_groups = models.ManyToManyField('HostGroup')

    class Meta:
        unique_together = ('host','host_user')
        verbose_name = u'主机与用户绑定关系'
        verbose_name_plural = u'主机与用户绑定关系'
    def __unicode__(self):
        return "%s:%s" %(self.host.hosname,self.host_user.username)
    def get_groups(self):
        return ''.join([g.name for g in self.host_groups.select_related()])
