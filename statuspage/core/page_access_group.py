# Copyright 2018 Issa Ashwash github.com/iashwash
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

class PageAccessGroup(object):

  def __init__(self):
    self._id = None
    self._page_id = None
    self._name = None
    self._external_identifier = None
    self._component_ids = None
    self._metric_ids = None
    self._page_access_user_ids = None
    
  @property
  def id(self):
    return self._id
  
  @id.setter
  def id(self, value):
    self._id = value
    
  @property
  def page_id(self):
    return self._page_id
  
  @page_id.setter
  def page_id(self, value):
    self._page_id = value
    
  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value
 
  @property
  def external_identifier(self):
    return self._external_identifier
  
  @external_identifier.setter
  def external_identifier(self, value):
    self._external_identifier = value
  
  @property
  def component_ids(self):
    return self._component_ids
  
  @component_ids.setter
  def component_ids(self, value):
    self._component_ids = value

  @property
  def metric_ids(self):
    return self._metric_ids
  
  @metric_ids.setter
  def metric_ids(self, value):
    self._metric_ids = value
  
  @property
  def page_access_user_ids(self):
    return self._page_access_user_ids
  
  @page_access_user_ids.setter
  def page_access_user_ids(self, value):
    self._page_access_user_ids = value
  
  @staticmethod
  def fromName(page_access_group_name):
    pag_list = PageAccessGroup.list()
    for pag in pag_list:
      if pag.name == page_access_group_name:
        return pag
    raise ValueError('PageAccessGroup does not exist')

  @staticmethod
  def fromDict(page_access_group_dict):
    pag = PageAccessGroup()
    pag.id = page_access_group_dict['id']
    pag.page_id = page_access_group_dict['page_id']
    pag.name = page_access_group_dict['name']
    pag.component_ids = page_access_group_dict['component_ids']
    pag.metric_ids = page_access_group_dict['metric_ids']
    pag.page_access_user_ids = page_access_group_dict['page_access_user_ids']
    if 'external_identifier' in page_access_group_dict:
        pag.external_identifier = page_access_group_dict['external_identifier']
    return pag

  @staticmethod
  def list():
    # url format : GET /pages/[page_id]/page_access_groups.json
    url = 'https://{}/pages/{}/page_access_groups.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    try:
      response = getUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not fetch PageAccessGroup list. Returned status code {}. Content: {}".format(response.status_code, response.content))
    
    for pag in response.json():
      yield(PageAccessGroup.fromDict(pag))

  def create(self):
    # url format : POST /pages/[page_id]/page_access_groups.json
    url = 'https://{}/pages/{}/page_access_groups.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'page_access_group' : {
                'name': self.name,
                'external_identifier': self.external_identifier,
                'component_ids': self.component_ids,
                'metric_ids': self.metric_ids,
                'page_access_user_ids' : self.page_access_user_ids
                }
           }
    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      j = response.json()
      self.id = j['id']
      self.component_ids = j['component_ids']
      self.metric_ids = j['metric_ids']
      self.page_access_user_ids = j['page_access_user_ids']
      if 'external_identifier' in j:
          self.external_identifier = j['external_identifier']
    except AssertionError as e:
      raise ValueError("Could not create PageAccessGroup. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def update(self, **kwargs):
    # url format : PATCH /pages/[page_id]/page_access_groups/[page_access_group_id].json
    url = 'https://{}/pages/{}/page_access_groups/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_group' : {
                'status': status,
                }
           }

    # TODO: limit kwargs to attributes specified in documentation? https://doers.statuspage.io/api/v1/page_access_group/
    # For now depend on the SP API to valida
    for k,v in kwargs.iteritems():
        data['page_access_group'][k] = v

    try:
      response = patchUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not update PageAccessGroup. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def delete(self, orphan_mode='empty'):
    # url = DELETE /pages/[page_id]/page_access_groups/[page_access_group_id].json
    url = 'https://{}/pages/{}/page_access_groups/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_group' : {
                'orphan_mode': orphan_mode,
                }
           }
    try:
      response = deleteUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not delete PageAccessGroup. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def overwrite_components(self, component_ids):
    # url = POST /pages/[page_id]/page_access_groups/[page_access_group_id]/components.json
    url = 'https://{}/pages/{}/page_access_groups/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_group' : {
                'component_ids': component_ids,
                }
           }
    try:
      response = postUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not overwrite PageAccessGroup components. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def add_components(self, component_ids):
    # url = PATCH /pages/[page_id]/page_access_groups/[page_access_group_id]/components.json
    url = 'https://{}/pages/{}/page_access_groups/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_group' : {
                'component_ids': component_ids,
                }
           }
    try:
      response = patchUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not add components PageAccessGroup. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def remove_all_components(self):
    # url = DELETE /pages/[page_id]/page_access_groups/[page_access_group_id]/components.json
    url = 'https://{}/pages/{}/page_access_groups/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove all PageAccessGroup components. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def remove_component(self, component_id):
    # url =  DELETE /pages/[page_id]/page_access_groups/[page_access_group_id]/components/[component_id].json
    url = 'https://{}/pages/{}/page_access_groups/{}/components/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id, component_id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove component from PageAccessGroup. Returned status code {}. Content: {}".format(response.status_code, response.content))
