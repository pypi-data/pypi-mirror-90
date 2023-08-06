#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: sense.py
Description: ai solutions for each Sense.
"""
#         Theme Sense

import aspaceai
import aspaceai.utility.aspaceconnector as connector
import json
class sense:
    def sentiment_analysis(text):
        """Perform Sentiment analysis for a given text.
        Args:
            text: Text on which to perform sentiment analysis.

        Returns:
            An array of sentiment analysis and corresponding confidence factor.
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {}
            payload['text'] = text
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey, json_payload)
            result_message = response_from_aspace.text


        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message