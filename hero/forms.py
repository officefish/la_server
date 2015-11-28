#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'inozemcev'
from django import forms


class HeroForm (forms.Form):
      title = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
      vocation = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'maxlength':70}))
      description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'maxlength':200}))
      uid = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'maxlength':2}))
      health = forms.IntegerField(max_value=90, widget=forms.TextInput(attrs={'maxlength':2}))
