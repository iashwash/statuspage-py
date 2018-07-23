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

import pytest
import sys
sys.path.append('..')
from statuspage.core.page_access_user import PageAccessUser

class Test_PageAccessUser(object):

  def setup_class(self):
    self.pau = PageAccessUser()
    self.pau.email = 'testing+pageaccessuser@issa.io'

  def teardown_class(self):
    pass

  def test_create_user(self):
    self.pau.create()
    
  def test_get_user(self):
    pau = PageAccessUser.fromEmail('testing+pageaccessuser@issa.io')
    assert(pau.email == self.pau.email)
    assert(pau.id == self.pau.id)

  def test_delete_user(self):
    self.pau.delete()
    try:
      pau = PageAccessUser.fromEmail('testing+pageaccessuser@issa.io')
    except ValueError as e:
      assert(e.message == 'PageAccessUser does not exist')
