# -*- coding: utf-8 -*-
from solutions.tt_solution.types import ResourceType


class Resource:
    @property
    def uid(self):
        return self._uid

    @property
    def entity_type(self):
        return self._entity_type
    
    @property
    def properties(self):
        return self._properties
    
    def __init__(self, uid, entity_type: ResourceType, properties):
        self._uid = uid
        self._entity_type = entity_type
        self._properties = properties
