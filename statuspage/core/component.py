# Copyright 2016 Kunal Lillaney (http://kunallillaney.github.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from __future__ import absolute_import
from statuspage.util.rest import *
from .settings import Settings
settings = Settings()

class Component(object):

  def __init__(self):
    self._id = None
    self._name = None
    self._position = None
    self._status = None
    self._group_id = None
    self._updated_at = None
    self._description = None
    
  @property
  def id(self):
    return self._id
  
  @id.setter
  def id(self, value):
    self._id = value
    
  @property
  def position(self):
    return self._position
  
  @position.setter
  def position(self, value):
    self._position = value
  
  @property
  def group_id(self):
    return self._group_id
  
  @group_id.setter
  def group_id(self, value):
    self._group_id = value

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value
 
  @property
  def status(self):
    return self._status
  
  @status.setter
  def status(self, value):
    self._status = value
  
  @property
  def description(self):
    return self._description
  
  @description.setter
  def description(self, value):
    self._description = value
  
  @staticmethod
  def fromName(component_name):
    component_list = Component.list()
    for component in component_list:
      if component.name == component_name:
        return component
    raise ValueError('Component does not exist')

  @staticmethod
  def fromDict(component_dict):
    component = Component()
    component.id = component_dict['id']
    component.name = component_dict['name']
    component.description = component_dict['description']
    component.status = component_dict['status']
    component.group_id = component_dict['group_id']
    # component.created_at = component_dict['created_at']
    # component.updated-at = component_dict['updated_at']
    return component

  @staticmethod
  def list():
    # url format : GET /pages/[page_id]/components.json
    url = 'https://{}/pages/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    try:
      response = getUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not fetch Component list. Returned status code {}. Content: {}".format(response.status_code, response.content))
    
    for component in response.json():
      yield(Component.fromDict(component))

  def create(self):
    # url format : POST /pages/[page_id]/components.json
    url = 'https://{}/pages/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'component' : {
                'name': self.name,
                'description': self.description
                }
           }
    if self.group_id:
        data['group_id'] = self.group_id
    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      self.status = response.json()['status']
      self.position = response.json()['position']
      self.id = response.json()['id']
    except AssertionError as e:
      raise ValueError("Could not create Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def update(self, status='major_outage'):
    # url format : PATCH /pages/[page_id]/components/[component_id].json
    url = 'https://{}/pages/{}/components/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'component' : {
                'status': status,
                }
           }
    try:
      response = patchUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not update Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def delete(self):
    # url = DELETE /pages/[page_id]/components/[component_id].json
    url = 'https://{}/pages/{}/components/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 204)
    except AssertionError as e:
      raise ValueError("Could not delete Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def assign_page_access_groups(self, page_access_group_ids):
    # url format : POST /pages/[page_id]/components/[component_id]/page_access_groups.json
    url = 'https://{}/pages/{}/components/{}/page_access_groups.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_group_ids' : page_access_group_ids
           }
    try:
      response = postUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not assign Page Access Groups to Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def remove_all_page_access_groups(self):
    # url = DELETE /pages/[page_id]/components/[component_id]/page_access_groups.json
    url = 'https://{}/pages/{}/components/{}/page_access_groups.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove all Page Access Groups from Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

