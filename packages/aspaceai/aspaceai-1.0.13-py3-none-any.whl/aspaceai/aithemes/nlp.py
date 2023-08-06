#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: conversation.py
Description: ai solutions for each Sense.
"""
import aspaceai
import json
import aspaceai
import aspaceai.utility.aspaceconnector as connector

#         Theme Conversation
class nlp:
    def translate(text, from_lang, to_lang):

        """Perform translation for a given text.
                Args:
                    text            : Text to be translated
                    from_lang       : From Language code
                    to_lang         : To Language code
                    Language codes  : Afrikaans=af,Arabic=ar,Assamese=as,Bangla=bn,Bosnian (Latin)=bs,
                    Bulgarian=bg,Cantonese (Traditional)=yue,Catalan=ca,Chinese Simplified=zh-Hans,
                    Chinese Traditional=zh-Hant,Croatian=hr,Czech=cs,Dari=prs,Danish=da,Dutch=nl,English=en,
                    Estonian=et,Fijian=fj,Filipino=fil,Finnish=fi,French=fr,French (Canada)=fr-ca,
                    German=de,Greek=el,Gujarati=gu,Haitian Creole=ht,Hebrew=he,Hindi=hi,
                    Hmong Daw=mww,Hungarian=hu,Icelandic=is,Indonesian=id,Irish=ga,Italian=it,
                    Japanese=ja,Kannada=kn,Kazakh=kk,Klingon=tlh-Latn,Klingon (plqaD)=tlh-Piqd,Korean=ko,
                    Kurdish (Central)=ku,Kurdish (Northern)=kmr,Latvian=lv,Lithuanian=lt,Malagasy=mg,Malay=ms,
                    Malayalam=ml,Maltese=mt,Maori=mi,Marathi=mr,Norwegian=nb,Odia=or,Pashto=ps,Persian=fa,Polish=pl,
                    Portuguese (Brazil)=pt-br,Portuguese (Portugal)=pt-pt,Punjabi=pa,Queretaro Otomi=otq,Romanian=ro,
                    Russian=ru,Samoan=sm,Serbian (Cyrillic)=sr-Cyrl,Serbian (Latin)=sr-Latn,Slovak=sk,Slovenian=sl,
                    Spanish=es,Swahili=sw,Swedish=sv,Tahitian=ty,Tamil=ta,Telugu=te,Thai=th,Tongan=to,Turkish=tr,
                    Ukrainian=uk,Urdu=ur,Vietnamese=vi,Welsh=cy,Yucatec Maya=yua
                Returns:
                    An array of translated text , from_lang language, to_lang language
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['text'] = text
            payload['from_lang'] = from_lang
            payload['to_lang'] = to_lang
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, api_key, json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    def part_of_speech(text):

        """Perform classifying words into their parts of speech and labeling them accordingly is known as part-of-speech tagging, POS-tagging, or simply tagging.
            Args:
                text: Text to be tagged

            Returns:
                status  : Operation status
                text    : Original text provided
                result  : Tagged value as JSON array
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['text'] = text
            json_payload =json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url,api_key,json_payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)


        return result_message

    def named_entity_recognition(text):

        """Perform named entity recognition
            Args:
                text: Text to be tagged

            Returns:
                status  : Operation status
                text    : Original text provided
                result  : NER value as JSON array
        """

        try:
            api_url = aspaceai.ASPACE_API_URL
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['text'] = text
            json_payload =json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url,api_key,json_payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    def dependency_parser(text):

        """Perform Dependency Parsing
            Args:
                text: Text for dependency parsing

            Returns:
                status  : Operation status
                text    : Original text provided
                result  : Dependency Parsing value as JSON array
        """

        try:
            api_url = aspaceai.ASPACE_API_URL
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['text'] = text
            json_payload =json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url,api_key,json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message

    def tags_extraction(text):

        """Perform tag extraction from a given text.
                Args:
                    text: Text for tag extraction

                Returns:
                status  : Operation status
                text    : Original text provided
                result  : Tags Exracted values as JSON array
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            api_key = aspaceai.ASPACE_API_KEY
            payload = {}
            payload['text'] = text
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, api_key, json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message


