# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import BinaryIO, List


class GetAsyncJobResultRequest(TeaModel):
    def __init__(
        self,
        job_id: str = None,
    ):
        self.job_id = job_id

    def validate(self):
        self.validate_required(self.job_id, 'job_id')

    def to_map(self):
        result = dict()
        if self.job_id is not None:
            result['JobId'] = self.job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        return self


class GetAsyncJobResultResponseData(TeaModel):
    def __init__(
        self,
        job_id: str = None,
        status: str = None,
        result: str = None,
        error_code: str = None,
        error_message: str = None,
    ):
        self.job_id = job_id
        self.status = status
        self.result = result
        self.error_code = error_code
        self.error_message = error_message

    def validate(self):
        self.validate_required(self.job_id, 'job_id')
        self.validate_required(self.status, 'status')
        self.validate_required(self.result, 'result')
        self.validate_required(self.error_code, 'error_code')
        self.validate_required(self.error_message, 'error_message')

    def to_map(self):
        result = dict()
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.status is not None:
            result['Status'] = self.status
        if self.result is not None:
            result['Result'] = self.result
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        return self


class GetAsyncJobResultResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: GetAsyncJobResultResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = GetAsyncJobResultResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ImitatePhotoStyleRequest(TeaModel):
    def __init__(
        self,
        style_url: str = None,
        image_url: str = None,
    ):
        self.style_url = style_url
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.style_url, 'style_url')
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.style_url is not None:
            result['StyleUrl'] = self.style_url
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StyleUrl') is not None:
            self.style_url = m.get('StyleUrl')
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class ImitatePhotoStyleResponseData(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class ImitatePhotoStyleResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ImitatePhotoStyleResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ImitatePhotoStyleResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ImitatePhotoStyleAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
        style_url: str = None,
    ):
        self.image_urlobject = image_urlobject
        self.style_url = style_url

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')
        self.validate_required(self.style_url, 'style_url')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        if self.style_url is not None:
            result['StyleUrl'] = self.style_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        if m.get('StyleUrl') is not None:
            self.style_url = m.get('StyleUrl')
        return self


class EnhanceImageColorRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        output_format: str = None,
        mode: str = None,
    ):
        self.image_url = image_url
        self.output_format = output_format
        self.mode = mode

    def validate(self):
        self.validate_required(self.image_url, 'image_url')
        self.validate_required(self.output_format, 'output_format')
        self.validate_required(self.mode, 'mode')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        if self.output_format is not None:
            result['OutputFormat'] = self.output_format
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        if m.get('OutputFormat') is not None:
            self.output_format = m.get('OutputFormat')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class EnhanceImageColorResponseData(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class EnhanceImageColorResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: EnhanceImageColorResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = EnhanceImageColorResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class EnhanceImageColorAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
        output_format: str = None,
        mode: str = None,
    ):
        self.image_urlobject = image_urlobject
        self.output_format = output_format
        self.mode = mode

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')
        self.validate_required(self.output_format, 'output_format')
        self.validate_required(self.mode, 'mode')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        if self.output_format is not None:
            result['OutputFormat'] = self.output_format
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        if m.get('OutputFormat') is not None:
            self.output_format = m.get('OutputFormat')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class RecolorHDImageRequestColorTemplate(TeaModel):
    def __init__(
        self,
        color: str = None,
    ):
        self.color = color

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.color is not None:
            result['Color'] = self.color
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Color') is not None:
            self.color = m.get('Color')
        return self


class RecolorHDImageRequest(TeaModel):
    def __init__(
        self,
        url: str = None,
        mode: str = None,
        ref_url: str = None,
        color_count: int = None,
        color_template: List[RecolorHDImageRequestColorTemplate] = None,
        degree: str = None,
    ):
        self.url = url
        self.mode = mode
        self.ref_url = ref_url
        self.color_count = color_count
        self.color_template = color_template
        self.degree = degree

    def validate(self):
        self.validate_required(self.url, 'url')
        if self.color_template:
            for k in self.color_template:
                if k:
                    k.validate()
        self.validate_required(self.degree, 'degree')

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.ref_url is not None:
            result['RefUrl'] = self.ref_url
        if self.color_count is not None:
            result['ColorCount'] = self.color_count
        result['ColorTemplate'] = []
        if self.color_template is not None:
            for k in self.color_template:
                result['ColorTemplate'].append(k.to_map() if k else None)
        if self.degree is not None:
            result['Degree'] = self.degree
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('RefUrl') is not None:
            self.ref_url = m.get('RefUrl')
        if m.get('ColorCount') is not None:
            self.color_count = m.get('ColorCount')
        self.color_template = []
        if m.get('ColorTemplate') is not None:
            for k in m.get('ColorTemplate'):
                temp_model = RecolorHDImageRequestColorTemplate()
                self.color_template.append(temp_model.from_map(k))
        if m.get('Degree') is not None:
            self.degree = m.get('Degree')
        return self


class RecolorHDImageResponseData(TeaModel):
    def __init__(
        self,
        image_list: List[str] = None,
    ):
        self.image_list = image_list

    def validate(self):
        self.validate_required(self.image_list, 'image_list')

    def to_map(self):
        result = dict()
        if self.image_list is not None:
            result['ImageList'] = self.image_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageList') is not None:
            self.image_list = m.get('ImageList')
        return self


class RecolorHDImageResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RecolorHDImageResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RecolorHDImageResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RecolorHDImageAdvanceRequestColorTemplate(TeaModel):
    def __init__(
        self,
        color: str = None,
    ):
        self.color = color

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.color is not None:
            result['Color'] = self.color
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Color') is not None:
            self.color = m.get('Color')
        return self


class RecolorHDImageAdvanceRequest(TeaModel):
    def __init__(
        self,
        url_object: BinaryIO = None,
        mode: str = None,
        ref_url: str = None,
        color_count: int = None,
        color_template: List[RecolorHDImageAdvanceRequestColorTemplate] = None,
        degree: str = None,
    ):
        self.url_object = url_object
        self.mode = mode
        self.ref_url = ref_url
        self.color_count = color_count
        self.color_template = color_template
        self.degree = degree

    def validate(self):
        self.validate_required(self.url_object, 'url_object')
        if self.color_template:
            for k in self.color_template:
                if k:
                    k.validate()
        self.validate_required(self.degree, 'degree')

    def to_map(self):
        result = dict()
        if self.url_object is not None:
            result['UrlObject'] = self.url_object
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.ref_url is not None:
            result['RefUrl'] = self.ref_url
        if self.color_count is not None:
            result['ColorCount'] = self.color_count
        result['ColorTemplate'] = []
        if self.color_template is not None:
            for k in self.color_template:
                result['ColorTemplate'].append(k.to_map() if k else None)
        if self.degree is not None:
            result['Degree'] = self.degree
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UrlObject') is not None:
            self.url_object = m.get('UrlObject')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('RefUrl') is not None:
            self.ref_url = m.get('RefUrl')
        if m.get('ColorCount') is not None:
            self.color_count = m.get('ColorCount')
        self.color_template = []
        if m.get('ColorTemplate') is not None:
            for k in m.get('ColorTemplate'):
                temp_model = RecolorHDImageAdvanceRequestColorTemplate()
                self.color_template.append(temp_model.from_map(k))
        if m.get('Degree') is not None:
            self.degree = m.get('Degree')
        return self


class AssessCompositionRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class AssessCompositionResponseData(TeaModel):
    def __init__(
        self,
        score: float = None,
    ):
        self.score = score

    def validate(self):
        self.validate_required(self.score, 'score')

    def to_map(self):
        result = dict()
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class AssessCompositionResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: AssessCompositionResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = AssessCompositionResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class AssessCompositionAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class AssessSharpnessRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class AssessSharpnessResponseData(TeaModel):
    def __init__(
        self,
        sharpness: float = None,
    ):
        self.sharpness = sharpness

    def validate(self):
        self.validate_required(self.sharpness, 'sharpness')

    def to_map(self):
        result = dict()
        if self.sharpness is not None:
            result['Sharpness'] = self.sharpness
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Sharpness') is not None:
            self.sharpness = m.get('Sharpness')
        return self


class AssessSharpnessResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: AssessSharpnessResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = AssessSharpnessResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class AssessSharpnessAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class AssessExposureRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class AssessExposureResponseData(TeaModel):
    def __init__(
        self,
        exposure: float = None,
    ):
        self.exposure = exposure

    def validate(self):
        self.validate_required(self.exposure, 'exposure')

    def to_map(self):
        result = dict()
        if self.exposure is not None:
            result['Exposure'] = self.exposure
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Exposure') is not None:
            self.exposure = m.get('Exposure')
        return self


class AssessExposureResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: AssessExposureResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = AssessExposureResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class AssessExposureAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class ImageBlindCharacterWatermarkRequest(TeaModel):
    def __init__(
        self,
        function_type: str = None,
        text: str = None,
        watermark_image_url: str = None,
        output_file_type: str = None,
        quality_factor: int = None,
        origin_image_url: str = None,
    ):
        self.function_type = function_type
        self.text = text
        self.watermark_image_url = watermark_image_url
        self.output_file_type = output_file_type
        self.quality_factor = quality_factor
        self.origin_image_url = origin_image_url

    def validate(self):
        self.validate_required(self.function_type, 'function_type')
        self.validate_required(self.quality_factor, 'quality_factor')
        self.validate_required(self.origin_image_url, 'origin_image_url')

    def to_map(self):
        result = dict()
        if self.function_type is not None:
            result['FunctionType'] = self.function_type
        if self.text is not None:
            result['Text'] = self.text
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.output_file_type is not None:
            result['OutputFileType'] = self.output_file_type
        if self.quality_factor is not None:
            result['QualityFactor'] = self.quality_factor
        if self.origin_image_url is not None:
            result['OriginImageURL'] = self.origin_image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionType') is not None:
            self.function_type = m.get('FunctionType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('OutputFileType') is not None:
            self.output_file_type = m.get('OutputFileType')
        if m.get('QualityFactor') is not None:
            self.quality_factor = m.get('QualityFactor')
        if m.get('OriginImageURL') is not None:
            self.origin_image_url = m.get('OriginImageURL')
        return self


class ImageBlindCharacterWatermarkResponseData(TeaModel):
    def __init__(
        self,
        watermark_image_url: str = None,
        text_image_url: str = None,
    ):
        self.watermark_image_url = watermark_image_url
        self.text_image_url = text_image_url

    def validate(self):
        self.validate_required(self.watermark_image_url, 'watermark_image_url')
        self.validate_required(self.text_image_url, 'text_image_url')

    def to_map(self):
        result = dict()
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.text_image_url is not None:
            result['TextImageURL'] = self.text_image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('TextImageURL') is not None:
            self.text_image_url = m.get('TextImageURL')
        return self


class ImageBlindCharacterWatermarkResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ImageBlindCharacterWatermarkResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ImageBlindCharacterWatermarkResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ImageBlindCharacterWatermarkAdvanceRequest(TeaModel):
    def __init__(
        self,
        origin_image_urlobject: BinaryIO = None,
        function_type: str = None,
        text: str = None,
        watermark_image_url: str = None,
        output_file_type: str = None,
        quality_factor: int = None,
    ):
        self.origin_image_urlobject = origin_image_urlobject
        self.function_type = function_type
        self.text = text
        self.watermark_image_url = watermark_image_url
        self.output_file_type = output_file_type
        self.quality_factor = quality_factor

    def validate(self):
        self.validate_required(self.origin_image_urlobject, 'origin_image_urlobject')
        self.validate_required(self.function_type, 'function_type')
        self.validate_required(self.quality_factor, 'quality_factor')

    def to_map(self):
        result = dict()
        if self.origin_image_urlobject is not None:
            result['OriginImageURLObject'] = self.origin_image_urlobject
        if self.function_type is not None:
            result['FunctionType'] = self.function_type
        if self.text is not None:
            result['Text'] = self.text
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.output_file_type is not None:
            result['OutputFileType'] = self.output_file_type
        if self.quality_factor is not None:
            result['QualityFactor'] = self.quality_factor
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OriginImageURLObject') is not None:
            self.origin_image_urlobject = m.get('OriginImageURLObject')
        if m.get('FunctionType') is not None:
            self.function_type = m.get('FunctionType')
        if m.get('Text') is not None:
            self.text = m.get('Text')
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('OutputFileType') is not None:
            self.output_file_type = m.get('OutputFileType')
        if m.get('QualityFactor') is not None:
            self.quality_factor = m.get('QualityFactor')
        return self


class RemoveImageSubtitlesRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        bx: float = None,
        by: float = None,
        bw: float = None,
        bh: float = None,
    ):
        self.image_url = image_url
        self.bx = bx
        self.by = by
        self.bw = bw
        self.bh = bh

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        if self.bx is not None:
            result['BX'] = self.bx
        if self.by is not None:
            result['BY'] = self.by
        if self.bw is not None:
            result['BW'] = self.bw
        if self.bh is not None:
            result['BH'] = self.bh
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        if m.get('BX') is not None:
            self.bx = m.get('BX')
        if m.get('BY') is not None:
            self.by = m.get('BY')
        if m.get('BW') is not None:
            self.bw = m.get('BW')
        if m.get('BH') is not None:
            self.bh = m.get('BH')
        return self


class RemoveImageSubtitlesResponseData(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RemoveImageSubtitlesResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RemoveImageSubtitlesResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RemoveImageSubtitlesResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RemoveImageSubtitlesAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
        bx: float = None,
        by: float = None,
        bw: float = None,
        bh: float = None,
    ):
        self.image_urlobject = image_urlobject
        self.bx = bx
        self.by = by
        self.bw = bw
        self.bh = bh

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        if self.bx is not None:
            result['BX'] = self.bx
        if self.by is not None:
            result['BY'] = self.by
        if self.bw is not None:
            result['BW'] = self.bw
        if self.bh is not None:
            result['BH'] = self.bh
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        if m.get('BX') is not None:
            self.bx = m.get('BX')
        if m.get('BY') is not None:
            self.by = m.get('BY')
        if m.get('BW') is not None:
            self.bw = m.get('BW')
        if m.get('BH') is not None:
            self.bh = m.get('BH')
        return self


class RemoveImageWatermarkRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RemoveImageWatermarkResponseData(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RemoveImageWatermarkResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RemoveImageWatermarkResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RemoveImageWatermarkResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RemoveImageWatermarkAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class ImageBlindPicWatermarkRequest(TeaModel):
    def __init__(
        self,
        function_type: str = None,
        logo_url: str = None,
        watermark_image_url: str = None,
        output_file_type: str = None,
        quality_factor: int = None,
        origin_image_url: str = None,
    ):
        self.function_type = function_type
        self.logo_url = logo_url
        self.watermark_image_url = watermark_image_url
        self.output_file_type = output_file_type
        self.quality_factor = quality_factor
        self.origin_image_url = origin_image_url

    def validate(self):
        self.validate_required(self.function_type, 'function_type')
        self.validate_required(self.quality_factor, 'quality_factor')
        self.validate_required(self.origin_image_url, 'origin_image_url')

    def to_map(self):
        result = dict()
        if self.function_type is not None:
            result['FunctionType'] = self.function_type
        if self.logo_url is not None:
            result['LogoURL'] = self.logo_url
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.output_file_type is not None:
            result['OutputFileType'] = self.output_file_type
        if self.quality_factor is not None:
            result['QualityFactor'] = self.quality_factor
        if self.origin_image_url is not None:
            result['OriginImageURL'] = self.origin_image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FunctionType') is not None:
            self.function_type = m.get('FunctionType')
        if m.get('LogoURL') is not None:
            self.logo_url = m.get('LogoURL')
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('OutputFileType') is not None:
            self.output_file_type = m.get('OutputFileType')
        if m.get('QualityFactor') is not None:
            self.quality_factor = m.get('QualityFactor')
        if m.get('OriginImageURL') is not None:
            self.origin_image_url = m.get('OriginImageURL')
        return self


class ImageBlindPicWatermarkResponseData(TeaModel):
    def __init__(
        self,
        watermark_image_url: str = None,
        logo_url: str = None,
    ):
        self.watermark_image_url = watermark_image_url
        self.logo_url = logo_url

    def validate(self):
        self.validate_required(self.watermark_image_url, 'watermark_image_url')
        self.validate_required(self.logo_url, 'logo_url')

    def to_map(self):
        result = dict()
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.logo_url is not None:
            result['LogoURL'] = self.logo_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('LogoURL') is not None:
            self.logo_url = m.get('LogoURL')
        return self


class ImageBlindPicWatermarkResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ImageBlindPicWatermarkResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ImageBlindPicWatermarkResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ImageBlindPicWatermarkAdvanceRequest(TeaModel):
    def __init__(
        self,
        origin_image_urlobject: BinaryIO = None,
        function_type: str = None,
        logo_url: str = None,
        watermark_image_url: str = None,
        output_file_type: str = None,
        quality_factor: int = None,
    ):
        self.origin_image_urlobject = origin_image_urlobject
        self.function_type = function_type
        self.logo_url = logo_url
        self.watermark_image_url = watermark_image_url
        self.output_file_type = output_file_type
        self.quality_factor = quality_factor

    def validate(self):
        self.validate_required(self.origin_image_urlobject, 'origin_image_urlobject')
        self.validate_required(self.function_type, 'function_type')
        self.validate_required(self.quality_factor, 'quality_factor')

    def to_map(self):
        result = dict()
        if self.origin_image_urlobject is not None:
            result['OriginImageURLObject'] = self.origin_image_urlobject
        if self.function_type is not None:
            result['FunctionType'] = self.function_type
        if self.logo_url is not None:
            result['LogoURL'] = self.logo_url
        if self.watermark_image_url is not None:
            result['WatermarkImageURL'] = self.watermark_image_url
        if self.output_file_type is not None:
            result['OutputFileType'] = self.output_file_type
        if self.quality_factor is not None:
            result['QualityFactor'] = self.quality_factor
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OriginImageURLObject') is not None:
            self.origin_image_urlobject = m.get('OriginImageURLObject')
        if m.get('FunctionType') is not None:
            self.function_type = m.get('FunctionType')
        if m.get('LogoURL') is not None:
            self.logo_url = m.get('LogoURL')
        if m.get('WatermarkImageURL') is not None:
            self.watermark_image_url = m.get('WatermarkImageURL')
        if m.get('OutputFileType') is not None:
            self.output_file_type = m.get('OutputFileType')
        if m.get('QualityFactor') is not None:
            self.quality_factor = m.get('QualityFactor')
        return self


class IntelligentCompositionRequest(TeaModel):
    def __init__(
        self,
        num_boxes: int = None,
        image_url: str = None,
    ):
        self.num_boxes = num_boxes
        self.image_url = image_url

    def validate(self):
        self.validate_required(self.image_url, 'image_url')

    def to_map(self):
        result = dict()
        if self.num_boxes is not None:
            result['NumBoxes'] = self.num_boxes
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NumBoxes') is not None:
            self.num_boxes = m.get('NumBoxes')
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class IntelligentCompositionResponseDataElements(TeaModel):
    def __init__(
        self,
        min_x: int = None,
        min_y: int = None,
        max_x: int = None,
        max_y: int = None,
        score: float = None,
    ):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.score = score

    def validate(self):
        self.validate_required(self.min_x, 'min_x')
        self.validate_required(self.min_y, 'min_y')
        self.validate_required(self.max_x, 'max_x')
        self.validate_required(self.max_y, 'max_y')
        self.validate_required(self.score, 'score')

    def to_map(self):
        result = dict()
        if self.min_x is not None:
            result['MinX'] = self.min_x
        if self.min_y is not None:
            result['MinY'] = self.min_y
        if self.max_x is not None:
            result['MaxX'] = self.max_x
        if self.max_y is not None:
            result['MaxY'] = self.max_y
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MinX') is not None:
            self.min_x = m.get('MinX')
        if m.get('MinY') is not None:
            self.min_y = m.get('MinY')
        if m.get('MaxX') is not None:
            self.max_x = m.get('MaxX')
        if m.get('MaxY') is not None:
            self.max_y = m.get('MaxY')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class IntelligentCompositionResponseData(TeaModel):
    def __init__(
        self,
        elements: List[IntelligentCompositionResponseDataElements] = None,
    ):
        self.elements = elements

    def validate(self):
        self.validate_required(self.elements, 'elements')
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = IntelligentCompositionResponseDataElements()
                self.elements.append(temp_model.from_map(k))
        return self


class IntelligentCompositionResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: IntelligentCompositionResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = IntelligentCompositionResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class IntelligentCompositionAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
        num_boxes: int = None,
    ):
        self.image_urlobject = image_urlobject
        self.num_boxes = num_boxes

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        if self.num_boxes is not None:
            result['NumBoxes'] = self.num_boxes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        if m.get('NumBoxes') is not None:
            self.num_boxes = m.get('NumBoxes')
        return self


class ChangeImageSizeRequest(TeaModel):
    def __init__(
        self,
        width: int = None,
        height: int = None,
        url: str = None,
    ):
        self.width = width
        self.height = height
        self.url = url

    def validate(self):
        self.validate_required(self.width, 'width')
        self.validate_required(self.height, 'height')
        self.validate_required(self.url, 'url')

    def to_map(self):
        result = dict()
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class ChangeImageSizeResponseDataRetainLocation(TeaModel):
    def __init__(
        self,
        x: int = None,
        y: int = None,
        width: int = None,
        height: int = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def validate(self):
        self.validate_required(self.x, 'x')
        self.validate_required(self.y, 'y')
        self.validate_required(self.width, 'width')
        self.validate_required(self.height, 'height')

    def to_map(self):
        result = dict()
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        return self


class ChangeImageSizeResponseData(TeaModel):
    def __init__(
        self,
        url: str = None,
        retain_location: ChangeImageSizeResponseDataRetainLocation = None,
    ):
        self.url = url
        self.retain_location = retain_location

    def validate(self):
        self.validate_required(self.url, 'url')
        self.validate_required(self.retain_location, 'retain_location')
        if self.retain_location:
            self.retain_location.validate()

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        if self.retain_location is not None:
            result['RetainLocation'] = self.retain_location.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('RetainLocation') is not None:
            temp_model = ChangeImageSizeResponseDataRetainLocation()
            self.retain_location = temp_model.from_map(m['RetainLocation'])
        return self


class ChangeImageSizeResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ChangeImageSizeResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ChangeImageSizeResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ChangeImageSizeAdvanceRequest(TeaModel):
    def __init__(
        self,
        url_object: BinaryIO = None,
        width: int = None,
        height: int = None,
    ):
        self.url_object = url_object
        self.width = width
        self.height = height

    def validate(self):
        self.validate_required(self.url_object, 'url_object')
        self.validate_required(self.width, 'width')
        self.validate_required(self.height, 'height')

    def to_map(self):
        result = dict()
        if self.url_object is not None:
            result['UrlObject'] = self.url_object
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UrlObject') is not None:
            self.url_object = m.get('UrlObject')
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        return self


class ExtendImageStyleRequest(TeaModel):
    def __init__(
        self,
        style_url: str = None,
        major_url: str = None,
    ):
        self.style_url = style_url
        self.major_url = major_url

    def validate(self):
        self.validate_required(self.style_url, 'style_url')
        self.validate_required(self.major_url, 'major_url')

    def to_map(self):
        result = dict()
        if self.style_url is not None:
            result['StyleUrl'] = self.style_url
        if self.major_url is not None:
            result['MajorUrl'] = self.major_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('StyleUrl') is not None:
            self.style_url = m.get('StyleUrl')
        if m.get('MajorUrl') is not None:
            self.major_url = m.get('MajorUrl')
        return self


class ExtendImageStyleResponseData(TeaModel):
    def __init__(
        self,
        url: str = None,
        major_url: str = None,
    ):
        self.url = url
        self.major_url = major_url

    def validate(self):
        self.validate_required(self.url, 'url')
        self.validate_required(self.major_url, 'major_url')

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        if self.major_url is not None:
            result['MajorUrl'] = self.major_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('MajorUrl') is not None:
            self.major_url = m.get('MajorUrl')
        return self


class ExtendImageStyleResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ExtendImageStyleResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ExtendImageStyleResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class MakeSuperResolutionImageRequest(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        self.url = url

    def validate(self):
        self.validate_required(self.url, 'url')

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class MakeSuperResolutionImageResponseData(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        self.url = url

    def validate(self):
        self.validate_required(self.url, 'url')

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class MakeSuperResolutionImageResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: MakeSuperResolutionImageResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = MakeSuperResolutionImageResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


class MakeSuperResolutionImageAdvanceRequest(TeaModel):
    def __init__(
        self,
        url_object: BinaryIO = None,
    ):
        self.url_object = url_object

    def validate(self):
        self.validate_required(self.url_object, 'url_object')

    def to_map(self):
        result = dict()
        if self.url_object is not None:
            result['UrlObject'] = self.url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('UrlObject') is not None:
            self.url_object = m.get('UrlObject')
        return self


class RecolorImageRequestColorTemplate(TeaModel):
    def __init__(
        self,
        color: str = None,
    ):
        self.color = color

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.color is not None:
            result['Color'] = self.color
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Color') is not None:
            self.color = m.get('Color')
        return self


class RecolorImageRequest(TeaModel):
    def __init__(
        self,
        url: str = None,
        mode: str = None,
        ref_url: str = None,
        color_count: int = None,
        color_template: List[RecolorImageRequestColorTemplate] = None,
    ):
        self.url = url
        self.mode = mode
        self.ref_url = ref_url
        self.color_count = color_count
        self.color_template = color_template

    def validate(self):
        self.validate_required(self.url, 'url')
        if self.color_template:
            for k in self.color_template:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.url is not None:
            result['Url'] = self.url
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.ref_url is not None:
            result['RefUrl'] = self.ref_url
        if self.color_count is not None:
            result['ColorCount'] = self.color_count
        result['ColorTemplate'] = []
        if self.color_template is not None:
            for k in self.color_template:
                result['ColorTemplate'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Url') is not None:
            self.url = m.get('Url')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('RefUrl') is not None:
            self.ref_url = m.get('RefUrl')
        if m.get('ColorCount') is not None:
            self.color_count = m.get('ColorCount')
        self.color_template = []
        if m.get('ColorTemplate') is not None:
            for k in m.get('ColorTemplate'):
                temp_model = RecolorImageRequestColorTemplate()
                self.color_template.append(temp_model.from_map(k))
        return self


class RecolorImageResponseData(TeaModel):
    def __init__(
        self,
        image_list: List[str] = None,
    ):
        self.image_list = image_list

    def validate(self):
        self.validate_required(self.image_list, 'image_list')

    def to_map(self):
        result = dict()
        if self.image_list is not None:
            result['ImageList'] = self.image_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageList') is not None:
            self.image_list = m.get('ImageList')
        return self


class RecolorImageResponse(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RecolorImageResponseData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.data, 'data')
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RecolorImageResponseData()
            self.data = temp_model.from_map(m['Data'])
        return self


