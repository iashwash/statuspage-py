# Copyright 2018 Issa Ashwash (github.com/iashwash)
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

class PageAccessUser(object):

  def __init__(self):
    self._id = None
    self._external_login = None
    self._email = None
    self._subscribe_to_components = None
    self._component_ids = None
    self._metric_ids = None
    self._page_access_group_ids = None
    
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
  def external_login(self):
    return self._external_login
  
  @external_login.setter
  def external_login(self, value):
    self._external_login = value
    
  @property
  def email(self):
    return self._email

  @email.setter
  def email(self, value):
    self._email = value
 
  @property
  def subscribe_to_components(self):
    return self._subscribe_to_components
  
  @subscribe_to_components.setter
  def subscribe_to_components(self, value):
    self._subscribe_to_components = value
  
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
  def page_access_group_ids(self):
    return self._page_access_group_ids
  
  @page_access_group_ids.setter
  def page_access_group_ids(self, value):
    self._page_access_group_ids = value
  
  @staticmethod
  def fromEmail(page_access_user_email):
    pau_list = PageAccessUser.list()
    for pau in pau_list:
      if pau.email == page_access_user_email:
        return pau
    raise ValueError('Page Access User does not exist')

  @staticmethod
  def fromDict(page_access_user_dict):
    pau = PageAccessUser()
    pau.id = page_access_user_dict['id']
    pau.page_id = page_access_user_dict['page_id']
    pau.email = page_access_user_dict['email']
    if 'external_login' in page_access_user_dict:
        pau.external_login = page_access_user_dict['external_login']
    if 'subscribe_to_components' in page_access_user_dict:
        pau.subscribe_to_components = page_access_user_dict['subscribe_to_components']
    if 'component_ids' in page_access_user_dict:
        pau.component_ids = page_access_user_dict['component_ids']
    if 'metric_ids' in page_access_user_dict:
        pau.metric_ids = page_access_user_dict['metric_ids']
    if 'page_access_group_ids' in page_access_user_dict:
        pau.page_access_group_ids = page_access_user_dict['page_access_group_ids']
    return pau

  @staticmethod
  def list():
    # url format : GET /pages/[page_id]/page_access_users.json
    url = 'https://{}/pages/{}/page_access_users.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    try:
      response = getUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not fetch PageAccessUser list. Returned status code {}. Content: {}".format(response.status_code, response.content))
    
    for pau in response.json():
      yield(PageAccessUser.fromDict(pau))

  def create(self):
    # url format : POST /pages/[page_id]/page_access_users.json
    url = 'https://{}/pages/{}/page_access_users.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'page_access_user' : {
                'email': self.email,
                'page_access_group_ids' : self.page_access_group_ids
                }
           }
    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      j = response.json()
      self.id = j['id']
      if 'component_ids' in j:
          self.component_ids = j['component_ids']
      if 'metric_ids' in j:
          self.metric_ids = j['metric_ids']
      if 'page_access_group_ids' in j:
          self.page_access_group_ids = j['page_access_group_ids']
      if 'external_identifier' in j:
          self.external_identifier = j['external_identifier']
    except AssertionError as e:
      raise ValueError("Could not create PageAccessUser. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def update(self, **kwargs):
    # url format : PATCH /pages/[page_id]/page_access_users/[page_access_user_id].json
    url = 'https://{}/pages/{}/page_access_users/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_user' : {
                }
           }

    # TODO: limit kwargs to attributes specified in documentation? https://doers.statuspage.io/api/v1/page_access_group/
    # For now depend on the SP API to valida
    for k,v in kwargs.iteritems():
        data['page_access_user'][k] = v

    try:
      response = patchUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not update PageAccessUser. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def delete(self,):
    # url = DELETE /pages/[page_id]/page_access_groups/[page_access_group_id].json
    url = 'https://{}/pages/{}/page_access_users/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'page_access_users' : {
                # TODO: this data placeholder can probably be removed
                }
           }
    try:
      response = deleteUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not delete PageAccessUser. Returned status code {}. Content: {}".format(response.status_code, response.content))

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
    # url = DELETE /pages/[page_id]/page_access_users/[page_access_user_id]/components.json
    url = 'https://{}/pages/{}/page_access_users/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove all PageAccessUser components. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def remove_component(self, component_id):
    # url =  DELETE /pages/[page_id]/page_access_users/[page_access_user_id]/components/[component_id].json
    url = 'https://{}/pages/{}/page_access_users/{}/components/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id, component_id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove PageAccessUser Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  @staticmethod
  def remove_component_from_all_users(component_id):
    # url =  DELETE /pages/[page_id]/components/[component_id]/page_access_users.json
    url = 'https://{}/pages/{}/components/{}/page_access_users.json'.format(settings.SITE_HOST, settings.PAGE_ID, component_id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not remove Component from all users. Returned status code {}. Content: {}".format(response.status_code, response.content))
