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

class CreateWorkspaceRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'AIWorkSpace', '2020-08-14', 'CreateWorkspace')
		self.set_uri_pattern('/api/core/v1.0/workspaces')
		self.set_method('POST')

	def get_WorkspaceName(self):
		return self.get_body_params().get('WorkspaceName')

	def set_WorkspaceName(self,WorkspaceName):
		self.add_body_params('WorkspaceName', WorkspaceName)

	def get_Description(self):
		return self.get_body_params().get('Description')

	def set_Description(self,Description):
		self.add_body_params('Description', Description)

	def get_WorkspaceAlias(self):
		return self.get_body_params().get('WorkspaceAlias')

	def set_WorkspaceAlias(self,WorkspaceAlias):
		self.add_body_params('WorkspaceAlias', WorkspaceAlias)