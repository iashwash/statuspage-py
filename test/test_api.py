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

import pytest
import sys
sys.path.append('..')
from core.incident import RealtimeIncident

class Test_API_Spdb:

  def setup_class(self):
    pass

  def teardown_class(self):
    pass

  def test_spdb_api(self):
    component = Component.fromName('Spatial Database API')

    result = (pytest.main(["../ndstore/test/test_blosc.py"]) 
               + pytest.main(["../ndstore/test/test_image.py"])
               + pytest.main(["../ndstore/test/test_jpeg.py"])
               + pytest.main(["../ndstore/test/test_raw.py"])
               + pytest.main(["../ndstore/test/test_propagate.py"])
               + pytest.main(["../ndstore/test/test_time.py"]))

    if (result >= 6):
      #Major Outage
      component.update('major_outage')

    elif (result >= 1):
      #Partial Outage
      component.update('partial_outage')

    else:
      #Operational
      component.update('operational')

  def test_ramon_api(self):
    component = Component.fromName('Ramon API')

    result = (pytest.main(["../ndstore/test/test_annoid.py"]) 
               + pytest.main(["../ndstore/test/test_ramon.py"])
               + pytest.main(["../ndstore/test/test_jsonann.py"])
               + pytest.main(["../ndstore/test/test_neuron.py"])

    if (result >= 4):
      #Major Outage
      component.update('major_outage')

    elif (result >= 1):
      #Partial Outage
      component.update('partial_outage')

    else:
      #Operational
      component.update('operational')

  def test_io_api(self):
    component = Component.fromName('IO API')

    result = (pytest.main(["../ndstore/test/test_autoingest.py"])
               + pytest.main(["../ndstore/test/test_io.py"])
               + pytest.main(["../ndstore/test/test_query.py"])

    if (result >= 3):
      #Major Outage
      component.update('major_outage')

    elif (result >= 1):
      #Partial Outage
      component.update('partial_outage')

    else:
      #Operational
      component.update('operational')

  def test_stats_api(self):
    component = Component.fromName('Stats/Graph')

    result = (pytest.main(["../ndstore/test/test_graphgen.py"])
               + pytest.main(["../ndstore/test/test_probability.py"])
               + pytest.main(["../ndstore/test/test_stats.py"])

    if (result >= 3):
      #Major Outage
      component.update('major_outage')

    elif (result >= 1):
      #Partial Outage
      component.update('partial_outage')

    else:
      #Operational
      component.update('operational')

  def test_metadata_api(self):
    component = Component.fromName('Metadata')

    result = (pytest.main(["../ndstore/test/test_info.py"])
               + pytest.main(["../ndstore/test/test_resource.py"])

    if (result >= 2):
      #Major Outage
      component.update('major_outage')

    elif (result >= 1):
      #Partial Outage
      component.update('partial_outage')

    else:
      #Operational
      component.update('operational')
