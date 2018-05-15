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

class Incident(object):

  def __init__(self):
    self._name = None
    self._status = None
    self._message = None
    self._impact_override = None
    self._component_ids = None
    self._wants_twitter_update = None
    self._incident_id = None

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
  def message(self):
    return self._message

  @message.setter
  def message(self, value):
    self._message = value

  @property
  def wants_twitter_update(self):
    return self._wants_twitter_update

  @wants_twitter_update.setter
  def wants_twitter_update(self, value):
    self._wants_twitter_update = value
  
  @property
  def impact_override(self):
    return self._impact_override

  @impact_override.setter
  def impact_override(self, value):
    self._impact_override = value
  
  @property
  def component_ids(self):
    return self._component_ids

  @component_ids.setter
  def component_ids(self, value):
    self._component_ids = value
  
  @property
  def component_ids_list(self):
    component_ids_list = []
    if self.component_ids:
      for component in self.component_ids:
        component_ids_list.append(component)
    return component_ids_list
  
  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, value):
    self._id = value

  @staticmethod
  def list():
    # url format : GET /pages/[page_id]/incidents.json
    url = 'https://{}/pages/{}/incidents.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    try:
      response = getUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not fetch incident list. Returned status code {}. Content {}".format(response.status_code, response.content))
    for incident in response.json():
      yield(Incident.fromDict(incident))
  
  @staticmethod
  def fromName(incident_name):
    incident_list = Incident.list()
    for incident in incident_list:
      if incident.name == incident_name:
        return incident
    raise ValueError('Incident does not exist')
  
  @staticmethod
  def fromDict(incident_dict):
    incident = Incident()
    incident.id = incident_dict['id']
    incident.name = incident_dict['name']
    incident.message = incident_dict['incident_updates'][0]['body']
    return incident

  def delete(self):
    # url format : DELETE /pages/[page_id]/incidents/[incident_id].json
    url = 'https://{}/pages/{}/incidents/{}.json'.format(settings.SITE_HOST, settings.PAGE_ID, self.id)
    try:
      response = deleteUrl(url)
      assert(response.status_code == 200)
    except AssertionError as e:
      raise ValueError("Could not delete incident. Returned status code {}. Content: {}".format(response.status_code, response.content))


class ScheduledIncident(Incident):

  def __init__(self):
    super(ScheduledIncident, self).__init__()
    self._scheduled_for = None
    self._scheduled_until = None
    self._scheduled_remind_prior = None
    self._scheduled_auto_in_progress = None
    self._scheduled_auto_completed = None

  def create(self):
    # url format : POST /pages/[page_id]/incidents.json
    url = 'https://{}/pages/{}/incidents.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'incident': {
                'name': self.name,
                'status': self.status,
                'message': self.message,
                'wants_twitter_update': self.wants_twitter_update,
                'component_ids': self.component_ids_list
                }
           }

    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      self.id = response.json()['id']
      # self.impact_override = response.json()['impact_override']
    except AssertionError as e:
      raise ValueError("Could not create incident. Returned status code {}. Content {}".format(response.status_code, response.content))


class RealtimeIncident(Incident):

  def __init__(self):
    super(RealtimeIncident, self).__init__()

  def create(self):
    # url format : POST /pages/[page_id]/incidents.json
    url = 'https://{}/pages/{}/incidents.json'.format(settings.SITE_HOST, settings.PAGE_ID)
    data = {
            'incident': {
                'name': self.name,
                'body': self.message, # message is deprecated
                }
           }

    for attr in ('status', 'wants_twitter_update', 'impact_override', 'component_ids'):
        val = getattr(self, attr)
        if val is not None:
            data['incident'][attr] = val
    
    try:
      response = postUrl(url, data)
      assert(response.status_code == 201)
      self.id = response.json()['id']
    except AssertionError as e:
      raise ValueError("Could not create incident. Returned status code {}. Content {}".format(response.status_code, response.content))

class HistoricalIncident(Incident):

  def __init__(self):
    super(HistoricalIncident, self).__init__()
