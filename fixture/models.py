from django.db import models
from django.utils import timezone

class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'country'

class Prefecture(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    number = models.IntegerField(default=0)
    value = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'prefecture'

class WorkParent(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    number = models.IntegerField(default=0)
    value = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'work_parent'

class WorkChild(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    parent = models.ForeignKey(WorkParent, on_delete=models.CASCADE, related_name="child")
    number = models.IntegerField(default=0)
    value = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'work_child'

