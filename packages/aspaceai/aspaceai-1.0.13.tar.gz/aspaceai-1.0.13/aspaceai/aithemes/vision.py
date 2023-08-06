#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: sense.py
Description: ai solutions for each vision.
"""
#         Theme vision

import aspaceai
import aspaceai.utility.aspaceconnector as connector
import json
class vision:

    '''-------------------------------------------------- OCR ------------------------------------------------------'''

    def ocr(image,image_format,language='eng'):
        """Perform OCR on a given image.
        Args:
            image: Image information on which to perform OCR.
            image_format: url, file ,base64string
            language: default = eng
            Supported Languages : ["afr","amh","ara","asm","aze","aze-cyrl","bel","ben","bod","bos","bul","cat","ceb","ces","chi-sim","chi-tra","chr","cym","dan",
                "dan-frak","deu","deu-frak","dev","dzo","ell","eng","enm","epo","est","eus","fas","fin","fra","frk","frm","gle","gle-uncial","glg","grc",
                 "guj","hat","heb","hin","hrv","hun","iku","ind","isl","ita","ita-old","jav","jpn","kan","kat","kat-old","kaz","khm","kir","kor","kur",
                 "lao","lat","lav","lit","mal","mar","mkd","mlt","msa","mya","nep","nld","nor","ori","pan","pol","por","pus","ron","rus","san","sin",
                 "slk","slk-frak","slv","spa","spa-old","sqi"]

        Returns:
            An OCR JSON result
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?language=" + language + "&image_format=" + image_format
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['image'] = image
            json_payload =json.dumps(payload)

            response_from_aspace = connector.createJSONPostRequest(api_url,api_key,json_payload)

            result_message = {}
            result_message['status'] = 'success'
            result_message['result'] = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)


        return json.dumps(result_message)

    '''-------------------------------------------------- FACE DETECTION ------------------------------------------------------'''
    def face_detection_image(image,image_format):
        """Perform Face Detection on a given image.
        Args:
            image: Image information on which to perform Face detection.
            image_format: url, file ,base64string

        Returns:
            An JSON result , Image in Base64 format
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?image_format=" + image_format
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['image'] = image
            json_payload =json.dumps(payload)

            response_from_aspace = connector.createJSONPostRequest(api_url,apikey,json_payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- EYE DETECTION ------------------------------------------------------'''
    def eye_detection(image,image_format):
        """Perform Eye Detection on a given image.
        Args:
            image: Image information on which to perform eye detection.
            image_format: url, file ,base64string

        Returns:
            An JSON result , Image in Base64 format
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?image_format=" + image_format
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['image'] = image
            json_payload =json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url,apikey,json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- SMILE DETECTION ------------------------------------------------------'''
    def smile_detection(image,image_format):
        """Perform Smile Detection on a given image.
        Args:
            image: Image information on which to perform Smile detection.
            image_format: url, file ,base64string

        Returns:
            An JSON result , Image in Base64 format
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?image_format=" + image_format
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['image'] = image
            json_payload =json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url,apikey,json_payload)
            result_message = response_from_aspace.text



        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- OBJECT DETECTION ------------------------------------------------------'''
    def object_detection(image, image_format):
        """Perform Object Detection on a given image.
        Args:
            image: Image information on which to perform Object detection.
            image_format: url, file ,base64string

        Returns:
            An JSON result , Image in Base64 format
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?image_format=" + image_format
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['image'] = image
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey, json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message


    '''-------------------------------------------------- IMAGE CLASSIFICATION ------------------------------------------------------'''
    def image_classification(image, image_format):
        """Perform Object Detection on a given image.
        Args:
            image: Image information on which to perform Object detection.
            image_format: url, file ,base64string

        Returns:
            An JSON result , Image in Base64 format
        """
        try:
            api_url = aspaceai.ASPACE_API_URL + "?image_format=" + image_format
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['image'] = image
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey, json_payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- QR Code Creator ------------------------------------------------------'''

    def qr_creator (text_to_encode):
        """Perform QR Code generation.
        Args:
            text: text to create QR code

        Returns:
            image:  An JSON result BASE64 image
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['data'] = text_to_encode
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey, json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- BARCODE Creator ------------------------------------------------------'''

    def barcode_creator(text_to_encode):
        """Perform QR Code generation.
        Args:
            text: text to create QR code

        Returns:
            image:  An JSON result BASE64 image
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['data'] = text_to_encode
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey, json_payload)
            result_message = response_from_aspace.text



        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- QR Code Reader ------------------------------------------------------'''

    def qr_reader (qr_code_image_path):
        """Perform QR Code generation.
        Args:
            image: QR code image path ( .png / .jpg / .pdf )

        Returns:
            text:  Extracted text from QR code

        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            files = {'file': open(qr_code_image_path, 'rb')}

            response_from_aspace = connector.createMultipartPostRequest(api_url, apikey, files, payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    '''-------------------------------------------------- BARCODE Reader ------------------------------------------------------'''

    def barcode_reader (barcode_code_image_path):
        """Perform barcode reading.
        Args:
            image: BARCODE image path ( .png / .jpg / .pdf )

        Returns:
            text:  Extracted text from BARCODE

        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            files = {'file': open(barcode_code_image_path, 'rb')}

            response_from_aspace = connector.createMultipartPostRequest(api_url,apikey,files,payload)

            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message