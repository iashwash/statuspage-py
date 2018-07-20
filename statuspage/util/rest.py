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
import requests
from statuspage.core.settings import Settings
settings = Settings()

def getUrl(url):
  try:
    response = requests.get(url, headers={'Authorization': 'OAuth {}'.format(settings.API_TOKEN, verify=True)})
    return response
  except Exception as e:
    raise e

def postUrl(url, data):
  try:
    response = requests.post(url, json=data, headers={'Authorization': 'OAuth {}'.format(settings.API_TOKEN, verify=True)})
    return response
  except Exception as e:
    raise e

def patchUrl(url, data):
  try:
    response = requests.patch(url, json=data, headers={'Authorization': 'OAuth {}'.format(settings.API_TOKEN, verify=True)})
    return response
  except Exception as e:
    raise e

def deleteUrl(url, data=None):
  try:
    if data is None:
        response = requests.delete(url, headers={'Authorization': 'OAuth {}'.format(settings.API_TOKEN, verify=True)})
    else:
        response = requests.delete(url, json=data, headers={'Authorization': 'OAuth {}'.format(settings.API_TOKEN, verify=True)})
    return response
  except Exception as e:
    raise e
