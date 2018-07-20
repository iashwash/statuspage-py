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

class ComponentGroup(object):

  def __init__(self):
    self._id = None
    self._name = None
    self._components = None
    
  @property
  def id(self):
    return self._id
  
  @id.setter
  def id(self, value):
    self._id = value
    
  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value
 
  @property
  def components(self):
    return self._components
  
  @status.setter
  def components(self, value):
    self._components = value
  
  @staticmethod
  def fromName(component_group):
    cg_list = ComponentGroup.list()
    for cg in cg_list:
      if cg.name == component_group:
        return cd
    raise ValueError('Componenti Group does not exist')

  @staticmethod
  def fromDict(cg_dict):
    cg = ComponentGroup()
    cg.id = cg_dict['id']
    cg.name = cg_dict['name']
    cg.components = cg_dict['components']
    return cg

  @staticmethod
  def list():
    # url format : GET /pages/[page_id]/component-groups.json
    url = 'https://{}/pages/{}/components-groups.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    try:
      response = getUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not fetch Component Group list. Returned status code {}. Content: {}".format(response.status_code, response.content))
    
    for cg in response.json():
      yield(ComponentGroup.fromDict(cg))

  def create(self):
    # url format : POST /pages/[page_id]/component-groups.json
    url = 'https://{}/pages/{}/components.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'component_group' : {
                'name': self.name,
                'components': self.components
                }
           }
    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      self.status = response.json()['status']
      self.position = response.json()['position']
      self.id = response.json()['id']
    except AssertionError as e:
      raise ValueError("Could not create Component Group. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def update(self, name=None, description=None):
    # url format : PUT /pages/[page_id]/component-groups/[component_group_id].json
    url = 'https://{}/pages/{}/component-groups/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    data = {
            'component_group' : {
                }
           }
    if name:
        data['component_group']['name'] = name
    if description:
        data['component_group']['description'] = description
    try:
      response = patchUrl(url, data)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not update Component. Returned status code {}. Content: {}".format(response.status_code, response.content))

  def delete(self):
    # url = DELETE /pages/[page_id]/component-groups/[component_group_id].json
    url = 'https://{}/pages/{}/component-groups/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 204)
    except AssertionError as e:
      raise ValueError("Could not delete Component Group. Returned status code {}. Content: {}".format(response.status_code, response.content))

