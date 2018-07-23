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
from statuspage.core.component_group import ComponentGroup

class Test_ComponentGroup(object):

  def setup_class(self):
    self.cg = ComponentGroup()
    self.cg.name = 'Test_Component_Group_1'

  def teardown_class(self):
    pass

  def test_create_group(self):
    self.cg.create()
    
  def test_get_group(self):
    pag = ComponentGroup.fromName('Test_Component_Group_1')
    assert(cg.name == self.cg.name)
    assert(cg.id == self.cg.id)

  def test_delete_group(self):
    self.cg.delete()
    try:
      cg = ComponentGroup.fromName('Test_Component_Group_1')
    except ValueError as e:
      assert(e.message == 'Component Group does not exist')
