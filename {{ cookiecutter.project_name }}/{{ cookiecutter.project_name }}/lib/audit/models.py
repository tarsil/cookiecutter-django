# Copyright (c) 2009 James Aylett <http://tartarus.org/james/computers/django/>
# Copyright (c) 2008 Aaron Sokoloski
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.conf import settings
from django.db import models


exclude = ['created_by', 'modified_by']


class AuditedModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)s_set', null=False, blank=True, on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_%(class)s_set', null=False, blank=True, on_delete=models.SET_DEFAULT)

    class Meta:
        abstract = True


class LooselyAuditedModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)s_set', null=True, blank=True, on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_%(class)s_set', null=True, blank=True, on_delete=models.SET_DEFAULT)

    class Meta:
        abstract = True
