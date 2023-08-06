#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class VariableManager(OpsviewConfigResourceManager):
    resource_uri = '/config/attribute'
    schema_name = 'attribute'
