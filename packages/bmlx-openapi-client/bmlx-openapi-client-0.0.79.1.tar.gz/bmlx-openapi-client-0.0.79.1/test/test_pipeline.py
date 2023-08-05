# coding: utf-8

"""
    bmlx api-server.

    Documentation of bmlx api-server apis. To find more info about generating spec from source, please refer to https://goswagger.io/use/spec.html  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import openapi_client
from openapi_client.models.pipeline import Pipeline  # noqa: E501
from openapi_client.rest import ApiException

class TestPipeline(unittest.TestCase):
    """Pipeline unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Pipeline
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.pipeline.Pipeline()  # noqa: E501
        if include_optional :
            return Pipeline(
                id = 56, 
                name = '0', 
                owner = openapi_client.models.user.User(
                    groups = [
                        openapi_client.models.group.Group(
                            users = [
                                openapi_client.models.user.User(
                                    email = '0', 
                                    id = 56, 
                                    name = '0', 
                                    phone = '0', 
                                    role = '0', 
                                    token = '0', )
                                ], 
                            id = 56, 
                            name = '0', )
                        ], 
                    email = '0', 
                    id = 56, 
                    name = '0', 
                    phone = '0', 
                    role = '0', 
                    token = '0', ), 
                owner_id = 56, 
                repo = '0', 
                tags = [
                    openapi_client.models.pipeline_tag.PipelineTag(
                        name = '0', )
                    ]
            )
        else :
            return Pipeline(
        )

    def testPipeline(self):
        """Test Pipeline"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
