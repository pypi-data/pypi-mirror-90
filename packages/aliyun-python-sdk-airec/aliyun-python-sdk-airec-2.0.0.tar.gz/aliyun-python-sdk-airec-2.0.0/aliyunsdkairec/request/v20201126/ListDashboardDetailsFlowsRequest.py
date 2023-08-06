# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest
from aliyunsdkairec.endpoint import endpoint_data

class ListDashboardDetailsFlowsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'Airec', '2020-11-26', 'ListDashboardDetailsFlows','airec')
		self.set_uri_pattern('/v2/openapi/instances/[instanceId]/dashboard/details/flows')
		self.set_method('GET')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_metricType(self):
		return self.get_query_params().get('metricType')

	def set_metricType(self,metricType):
		self.add_query_param('metricType',metricType)

	def get_instanceId(self):
		return self.get_path_params().get('instanceId')

	def set_instanceId(self,instanceId):
		self.add_path_param('instanceId',instanceId)

	def get_experimentIds(self):
		return self.get_query_params().get('experimentIds')

	def set_experimentIds(self,experimentIds):
		self.add_query_param('experimentIds',experimentIds)

	def get_traceIds(self):
		return self.get_query_params().get('traceIds')

	def set_traceIds(self,traceIds):
		self.add_query_param('traceIds',traceIds)

	def get_endTime(self):
		return self.get_query_params().get('endTime')

	def set_endTime(self,endTime):
		self.add_query_param('endTime',endTime)

	def get_startTime(self):
		return self.get_query_params().get('startTime')

	def set_startTime(self,startTime):
		self.add_query_param('startTime',startTime)

	def get_sceneIds(self):
		return self.get_query_params().get('sceneIds')

	def set_sceneIds(self,sceneIds):
		self.add_query_param('sceneIds',sceneIds)