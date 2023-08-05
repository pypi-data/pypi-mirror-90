# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore
from typing import Dict

from alibabacloud_tea_rpc.client import Client as RPCClient
from alibabacloud_tea_rpc import models as rpc_models
from alibabacloud_imageenhan20190930 import models as imageenhan_20190930_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_openplatform20191219.client import Client as OpenPlatformClient
from alibabacloud_openplatform20191219 import models as open_platform_models
from alibabacloud_oss_sdk import models as oss_models
from alibabacloud_rpc_util.client import Client as RPCUtilClient
from alibabacloud_oss_sdk.client import Client as OSSClient
from alibabacloud_tea_fileform import models as file_form_models
from alibabacloud_oss_util import models as ossutil_models
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient


class Client(RPCClient):
    def __init__(
        self, 
        config: rpc_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('imageenhan', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_async_job_result(
        self,
        request: imageenhan_20190930_models.GetAsyncJobResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.GetAsyncJobResultResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.GetAsyncJobResultResponse().from_map(
            self.do_request('GetAsyncJobResult', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def get_async_job_result_async(
        self,
        request: imageenhan_20190930_models.GetAsyncJobResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.GetAsyncJobResultResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.GetAsyncJobResultResponse().from_map(
            await self.do_request_async('GetAsyncJobResult', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def imitate_photo_style(
        self,
        request: imageenhan_20190930_models.ImitatePhotoStyleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImitatePhotoStyleResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImitatePhotoStyleResponse().from_map(
            self.do_request('ImitatePhotoStyle', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def imitate_photo_style_async(
        self,
        request: imageenhan_20190930_models.ImitatePhotoStyleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImitatePhotoStyleResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImitatePhotoStyleResponse().from_map(
            await self.do_request_async('ImitatePhotoStyle', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def imitate_photo_style_advance(
        self,
        request: imageenhan_20190930_models.ImitatePhotoStyleAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImitatePhotoStyleResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        imitate_photo_stylereq = imageenhan_20190930_models.ImitatePhotoStyleRequest()
        RPCUtilClient.convert(request, imitate_photo_stylereq)
        imitate_photo_stylereq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        imitate_photo_style_resp = self.imitate_photo_style(imitate_photo_stylereq, runtime)
        return imitate_photo_style_resp

    async def imitate_photo_style_advance_async(
        self,
        request: imageenhan_20190930_models.ImitatePhotoStyleAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImitatePhotoStyleResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        imitate_photo_stylereq = imageenhan_20190930_models.ImitatePhotoStyleRequest()
        RPCUtilClient.convert(request, imitate_photo_stylereq)
        imitate_photo_stylereq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        imitate_photo_style_resp = await self.imitate_photo_style_async(imitate_photo_stylereq, runtime)
        return imitate_photo_style_resp

    def enhance_image_color(
        self,
        request: imageenhan_20190930_models.EnhanceImageColorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.EnhanceImageColorResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.EnhanceImageColorResponse().from_map(
            self.do_request('EnhanceImageColor', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def enhance_image_color_async(
        self,
        request: imageenhan_20190930_models.EnhanceImageColorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.EnhanceImageColorResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.EnhanceImageColorResponse().from_map(
            await self.do_request_async('EnhanceImageColor', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def enhance_image_color_advance(
        self,
        request: imageenhan_20190930_models.EnhanceImageColorAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.EnhanceImageColorResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        enhance_image_colorreq = imageenhan_20190930_models.EnhanceImageColorRequest()
        RPCUtilClient.convert(request, enhance_image_colorreq)
        enhance_image_colorreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        enhance_image_color_resp = self.enhance_image_color(enhance_image_colorreq, runtime)
        return enhance_image_color_resp

    async def enhance_image_color_advance_async(
        self,
        request: imageenhan_20190930_models.EnhanceImageColorAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.EnhanceImageColorResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        enhance_image_colorreq = imageenhan_20190930_models.EnhanceImageColorRequest()
        RPCUtilClient.convert(request, enhance_image_colorreq)
        enhance_image_colorreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        enhance_image_color_resp = await self.enhance_image_color_async(enhance_image_colorreq, runtime)
        return enhance_image_color_resp

    def recolor_hdimage(
        self,
        request: imageenhan_20190930_models.RecolorHDImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorHDImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RecolorHDImageResponse().from_map(
            self.do_request('RecolorHDImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def recolor_hdimage_async(
        self,
        request: imageenhan_20190930_models.RecolorHDImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorHDImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RecolorHDImageResponse().from_map(
            await self.do_request_async('RecolorHDImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def recolor_hdimage_advance(
        self,
        request: imageenhan_20190930_models.RecolorHDImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorHDImageResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        recolor_hdimagereq = imageenhan_20190930_models.RecolorHDImageRequest()
        RPCUtilClient.convert(request, recolor_hdimagereq)
        recolor_hdimagereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recolor_hdimage_resp = self.recolor_hdimage(recolor_hdimagereq, runtime)
        return recolor_hdimage_resp

    async def recolor_hdimage_advance_async(
        self,
        request: imageenhan_20190930_models.RecolorHDImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorHDImageResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        recolor_hdimagereq = imageenhan_20190930_models.RecolorHDImageRequest()
        RPCUtilClient.convert(request, recolor_hdimagereq)
        recolor_hdimagereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recolor_hdimage_resp = await self.recolor_hdimage_async(recolor_hdimagereq, runtime)
        return recolor_hdimage_resp

    def assess_composition(
        self,
        request: imageenhan_20190930_models.AssessCompositionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessCompositionResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessCompositionResponse().from_map(
            self.do_request('AssessComposition', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def assess_composition_async(
        self,
        request: imageenhan_20190930_models.AssessCompositionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessCompositionResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessCompositionResponse().from_map(
            await self.do_request_async('AssessComposition', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def assess_composition_advance(
        self,
        request: imageenhan_20190930_models.AssessCompositionAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessCompositionResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        assess_compositionreq = imageenhan_20190930_models.AssessCompositionRequest()
        RPCUtilClient.convert(request, assess_compositionreq)
        assess_compositionreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_composition_resp = self.assess_composition(assess_compositionreq, runtime)
        return assess_composition_resp

    async def assess_composition_advance_async(
        self,
        request: imageenhan_20190930_models.AssessCompositionAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessCompositionResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        assess_compositionreq = imageenhan_20190930_models.AssessCompositionRequest()
        RPCUtilClient.convert(request, assess_compositionreq)
        assess_compositionreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_composition_resp = await self.assess_composition_async(assess_compositionreq, runtime)
        return assess_composition_resp

    def assess_sharpness(
        self,
        request: imageenhan_20190930_models.AssessSharpnessRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessSharpnessResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessSharpnessResponse().from_map(
            self.do_request('AssessSharpness', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def assess_sharpness_async(
        self,
        request: imageenhan_20190930_models.AssessSharpnessRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessSharpnessResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessSharpnessResponse().from_map(
            await self.do_request_async('AssessSharpness', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def assess_sharpness_advance(
        self,
        request: imageenhan_20190930_models.AssessSharpnessAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessSharpnessResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        assess_sharpnessreq = imageenhan_20190930_models.AssessSharpnessRequest()
        RPCUtilClient.convert(request, assess_sharpnessreq)
        assess_sharpnessreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_sharpness_resp = self.assess_sharpness(assess_sharpnessreq, runtime)
        return assess_sharpness_resp

    async def assess_sharpness_advance_async(
        self,
        request: imageenhan_20190930_models.AssessSharpnessAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessSharpnessResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        assess_sharpnessreq = imageenhan_20190930_models.AssessSharpnessRequest()
        RPCUtilClient.convert(request, assess_sharpnessreq)
        assess_sharpnessreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_sharpness_resp = await self.assess_sharpness_async(assess_sharpnessreq, runtime)
        return assess_sharpness_resp

    def assess_exposure(
        self,
        request: imageenhan_20190930_models.AssessExposureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessExposureResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessExposureResponse().from_map(
            self.do_request('AssessExposure', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def assess_exposure_async(
        self,
        request: imageenhan_20190930_models.AssessExposureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessExposureResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.AssessExposureResponse().from_map(
            await self.do_request_async('AssessExposure', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def assess_exposure_advance(
        self,
        request: imageenhan_20190930_models.AssessExposureAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessExposureResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        assess_exposurereq = imageenhan_20190930_models.AssessExposureRequest()
        RPCUtilClient.convert(request, assess_exposurereq)
        assess_exposurereq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_exposure_resp = self.assess_exposure(assess_exposurereq, runtime)
        return assess_exposure_resp

    async def assess_exposure_advance_async(
        self,
        request: imageenhan_20190930_models.AssessExposureAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.AssessExposureResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        assess_exposurereq = imageenhan_20190930_models.AssessExposureRequest()
        RPCUtilClient.convert(request, assess_exposurereq)
        assess_exposurereq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        assess_exposure_resp = await self.assess_exposure_async(assess_exposurereq, runtime)
        return assess_exposure_resp

    def image_blind_character_watermark(
        self,
        request: imageenhan_20190930_models.ImageBlindCharacterWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse().from_map(
            self.do_request('ImageBlindCharacterWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def image_blind_character_watermark_async(
        self,
        request: imageenhan_20190930_models.ImageBlindCharacterWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse().from_map(
            await self.do_request_async('ImageBlindCharacterWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def image_blind_character_watermark_advance(
        self,
        request: imageenhan_20190930_models.ImageBlindCharacterWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.origin_image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        image_blind_character_watermarkreq = imageenhan_20190930_models.ImageBlindCharacterWatermarkRequest()
        RPCUtilClient.convert(request, image_blind_character_watermarkreq)
        image_blind_character_watermarkreq.origin_image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        image_blind_character_watermark_resp = self.image_blind_character_watermark(image_blind_character_watermarkreq, runtime)
        return image_blind_character_watermark_resp

    async def image_blind_character_watermark_advance_async(
        self,
        request: imageenhan_20190930_models.ImageBlindCharacterWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindCharacterWatermarkResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.origin_image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        image_blind_character_watermarkreq = imageenhan_20190930_models.ImageBlindCharacterWatermarkRequest()
        RPCUtilClient.convert(request, image_blind_character_watermarkreq)
        image_blind_character_watermarkreq.origin_image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        image_blind_character_watermark_resp = await self.image_blind_character_watermark_async(image_blind_character_watermarkreq, runtime)
        return image_blind_character_watermark_resp

    def remove_image_subtitles(
        self,
        request: imageenhan_20190930_models.RemoveImageSubtitlesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageSubtitlesResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RemoveImageSubtitlesResponse().from_map(
            self.do_request('RemoveImageSubtitles', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def remove_image_subtitles_async(
        self,
        request: imageenhan_20190930_models.RemoveImageSubtitlesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageSubtitlesResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RemoveImageSubtitlesResponse().from_map(
            await self.do_request_async('RemoveImageSubtitles', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def remove_image_subtitles_advance(
        self,
        request: imageenhan_20190930_models.RemoveImageSubtitlesAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageSubtitlesResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        remove_image_subtitlesreq = imageenhan_20190930_models.RemoveImageSubtitlesRequest()
        RPCUtilClient.convert(request, remove_image_subtitlesreq)
        remove_image_subtitlesreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        remove_image_subtitles_resp = self.remove_image_subtitles(remove_image_subtitlesreq, runtime)
        return remove_image_subtitles_resp

    async def remove_image_subtitles_advance_async(
        self,
        request: imageenhan_20190930_models.RemoveImageSubtitlesAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageSubtitlesResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        remove_image_subtitlesreq = imageenhan_20190930_models.RemoveImageSubtitlesRequest()
        RPCUtilClient.convert(request, remove_image_subtitlesreq)
        remove_image_subtitlesreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        remove_image_subtitles_resp = await self.remove_image_subtitles_async(remove_image_subtitlesreq, runtime)
        return remove_image_subtitles_resp

    def remove_image_watermark(
        self,
        request: imageenhan_20190930_models.RemoveImageWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RemoveImageWatermarkResponse().from_map(
            self.do_request('RemoveImageWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def remove_image_watermark_async(
        self,
        request: imageenhan_20190930_models.RemoveImageWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RemoveImageWatermarkResponse().from_map(
            await self.do_request_async('RemoveImageWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def remove_image_watermark_advance(
        self,
        request: imageenhan_20190930_models.RemoveImageWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageWatermarkResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        remove_image_watermarkreq = imageenhan_20190930_models.RemoveImageWatermarkRequest()
        RPCUtilClient.convert(request, remove_image_watermarkreq)
        remove_image_watermarkreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        remove_image_watermark_resp = self.remove_image_watermark(remove_image_watermarkreq, runtime)
        return remove_image_watermark_resp

    async def remove_image_watermark_advance_async(
        self,
        request: imageenhan_20190930_models.RemoveImageWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RemoveImageWatermarkResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        remove_image_watermarkreq = imageenhan_20190930_models.RemoveImageWatermarkRequest()
        RPCUtilClient.convert(request, remove_image_watermarkreq)
        remove_image_watermarkreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        remove_image_watermark_resp = await self.remove_image_watermark_async(remove_image_watermarkreq, runtime)
        return remove_image_watermark_resp

    def image_blind_pic_watermark(
        self,
        request: imageenhan_20190930_models.ImageBlindPicWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindPicWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImageBlindPicWatermarkResponse().from_map(
            self.do_request('ImageBlindPicWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def image_blind_pic_watermark_async(
        self,
        request: imageenhan_20190930_models.ImageBlindPicWatermarkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindPicWatermarkResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ImageBlindPicWatermarkResponse().from_map(
            await self.do_request_async('ImageBlindPicWatermark', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def image_blind_pic_watermark_advance(
        self,
        request: imageenhan_20190930_models.ImageBlindPicWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindPicWatermarkResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.origin_image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        image_blind_pic_watermarkreq = imageenhan_20190930_models.ImageBlindPicWatermarkRequest()
        RPCUtilClient.convert(request, image_blind_pic_watermarkreq)
        image_blind_pic_watermarkreq.origin_image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        image_blind_pic_watermark_resp = self.image_blind_pic_watermark(image_blind_pic_watermarkreq, runtime)
        return image_blind_pic_watermark_resp

    async def image_blind_pic_watermark_advance_async(
        self,
        request: imageenhan_20190930_models.ImageBlindPicWatermarkAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ImageBlindPicWatermarkResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.origin_image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        image_blind_pic_watermarkreq = imageenhan_20190930_models.ImageBlindPicWatermarkRequest()
        RPCUtilClient.convert(request, image_blind_pic_watermarkreq)
        image_blind_pic_watermarkreq.origin_image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        image_blind_pic_watermark_resp = await self.image_blind_pic_watermark_async(image_blind_pic_watermarkreq, runtime)
        return image_blind_pic_watermark_resp

    def intelligent_composition(
        self,
        request: imageenhan_20190930_models.IntelligentCompositionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.IntelligentCompositionResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.IntelligentCompositionResponse().from_map(
            self.do_request('IntelligentComposition', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def intelligent_composition_async(
        self,
        request: imageenhan_20190930_models.IntelligentCompositionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.IntelligentCompositionResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.IntelligentCompositionResponse().from_map(
            await self.do_request_async('IntelligentComposition', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def intelligent_composition_advance(
        self,
        request: imageenhan_20190930_models.IntelligentCompositionAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.IntelligentCompositionResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        intelligent_compositionreq = imageenhan_20190930_models.IntelligentCompositionRequest()
        RPCUtilClient.convert(request, intelligent_compositionreq)
        intelligent_compositionreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        intelligent_composition_resp = self.intelligent_composition(intelligent_compositionreq, runtime)
        return intelligent_composition_resp

    async def intelligent_composition_advance_async(
        self,
        request: imageenhan_20190930_models.IntelligentCompositionAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.IntelligentCompositionResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        intelligent_compositionreq = imageenhan_20190930_models.IntelligentCompositionRequest()
        RPCUtilClient.convert(request, intelligent_compositionreq)
        intelligent_compositionreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        intelligent_composition_resp = await self.intelligent_composition_async(intelligent_compositionreq, runtime)
        return intelligent_composition_resp

    def change_image_size(
        self,
        request: imageenhan_20190930_models.ChangeImageSizeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ChangeImageSizeResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ChangeImageSizeResponse().from_map(
            self.do_request('ChangeImageSize', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def change_image_size_async(
        self,
        request: imageenhan_20190930_models.ChangeImageSizeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ChangeImageSizeResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ChangeImageSizeResponse().from_map(
            await self.do_request_async('ChangeImageSize', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def change_image_size_advance(
        self,
        request: imageenhan_20190930_models.ChangeImageSizeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ChangeImageSizeResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        change_image_sizereq = imageenhan_20190930_models.ChangeImageSizeRequest()
        RPCUtilClient.convert(request, change_image_sizereq)
        change_image_sizereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        change_image_size_resp = self.change_image_size(change_image_sizereq, runtime)
        return change_image_size_resp

    async def change_image_size_advance_async(
        self,
        request: imageenhan_20190930_models.ChangeImageSizeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ChangeImageSizeResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        change_image_sizereq = imageenhan_20190930_models.ChangeImageSizeRequest()
        RPCUtilClient.convert(request, change_image_sizereq)
        change_image_sizereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        change_image_size_resp = await self.change_image_size_async(change_image_sizereq, runtime)
        return change_image_size_resp

    def extend_image_style(
        self,
        request: imageenhan_20190930_models.ExtendImageStyleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ExtendImageStyleResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ExtendImageStyleResponse().from_map(
            self.do_request('ExtendImageStyle', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def extend_image_style_async(
        self,
        request: imageenhan_20190930_models.ExtendImageStyleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.ExtendImageStyleResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.ExtendImageStyleResponse().from_map(
            await self.do_request_async('ExtendImageStyle', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def make_super_resolution_image(
        self,
        request: imageenhan_20190930_models.MakeSuperResolutionImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.MakeSuperResolutionImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.MakeSuperResolutionImageResponse().from_map(
            self.do_request('MakeSuperResolutionImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def make_super_resolution_image_async(
        self,
        request: imageenhan_20190930_models.MakeSuperResolutionImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.MakeSuperResolutionImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.MakeSuperResolutionImageResponse().from_map(
            await self.do_request_async('MakeSuperResolutionImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def make_super_resolution_image_advance(
        self,
        request: imageenhan_20190930_models.MakeSuperResolutionImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.MakeSuperResolutionImageResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        oss_client.post_object(upload_request, oss_runtime)
        # Step 2: request final api
        make_super_resolution_imagereq = imageenhan_20190930_models.MakeSuperResolutionImageRequest()
        RPCUtilClient.convert(request, make_super_resolution_imagereq)
        make_super_resolution_imagereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        make_super_resolution_image_resp = self.make_super_resolution_image(make_super_resolution_imagereq, runtime)
        return make_super_resolution_image_resp

    async def make_super_resolution_image_advance_async(
        self,
        request: imageenhan_20190930_models.MakeSuperResolutionImageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.MakeSuperResolutionImageResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='imageenhan',
            region_id=self._region_id
        )
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        # Step 1: request OSS api to upload file
        oss_config = oss_models.Config(
            access_key_id=auth_response.access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint=RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type),
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.url_object,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        await oss_client.post_object_async(upload_request, oss_runtime)
        # Step 2: request final api
        make_super_resolution_imagereq = imageenhan_20190930_models.MakeSuperResolutionImageRequest()
        RPCUtilClient.convert(request, make_super_resolution_imagereq)
        make_super_resolution_imagereq.url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        make_super_resolution_image_resp = await self.make_super_resolution_image_async(make_super_resolution_imagereq, runtime)
        return make_super_resolution_image_resp

    def recolor_image(
        self,
        request: imageenhan_20190930_models.RecolorImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RecolorImageResponse().from_map(
            self.do_request('RecolorImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def recolor_image_async(
        self,
        request: imageenhan_20190930_models.RecolorImageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> imageenhan_20190930_models.RecolorImageResponse:
        UtilClient.validate_model(request)
        return imageenhan_20190930_models.RecolorImageResponse().from_map(
            await self.do_request_async('RecolorImage', 'HTTPS', 'POST', '2019-09-30', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)
