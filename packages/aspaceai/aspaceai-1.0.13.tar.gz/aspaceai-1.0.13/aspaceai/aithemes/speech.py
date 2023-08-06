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
class speech:

    def speech_to_text(wav_audio_file_path, audio_language):
        """Perform speech to text for a given audio files ( .wav )
        Args:
            wav_audio_file: Audio file to extract text
            audio_language: default = en-IN
            Supported Languages : Arabic (Bahrain), modern standard=ar-BH,Arabic (Egypt)=ar-EG,Arabic (Iraq)=ar-IQ,
            Arabic (Israel)=ar-IL,Arabic (Jordan)=ar-JO,Arabic (Kuwait)=ar-KW,Arabic (Lebanon)=ar-LB,Arabic (Oman)=ar-OM,
            Arabic (Qatar)=ar-QA,Arabic (Saudi Arabia)=ar-SA,Arabic (State of Palestine)=ar-PS,Arabic (Syria)=ar-SY,
            Arabic (United Arab Emirates)=ar-AE,Bulgarian (Bulgaria)=bg-BG,Catalan (Spain)=ca-ES,
            Chinese (Cantonese, Traditional)=zh-HK,Chinese (Mandarin, Simplified)=zh-CN,
            Chinese (Taiwanese Mandarin)=zh-TW,Croatian (Croatia)=hr-HR,Czech (Czech Republic)=cs-CZ,
            Danish (Denmark)=da-DK,Dutch (Netherlands)=nl-NL,English (Australia)=en-AU,=,English (Canada)=en-CA,
            English (Hong Kong)=en-HK,English (India)=en-IN,=,English (Ireland)=en-IE,English (New Zealand)=en-NZ,
            English (Nigeria)=en-NG,English (Philippines)=en-PH,English (Singapore)=en-SG,English (South Africa)=en-ZA,
            English (United Kingdom)=en-GB,English (United States)=en-US,Estonian(Estonia)=et-EE,
            Finnish (Finland)=fi-FI,French (Canada)=fr-CA,=,French (France)=fr-FR,German (Germany)=de-DE,
            Greek (Greece)=el-GR,Gujarati (Indian)=gu-IN,Hindi (India)=hi-IN,=,Hungarian (Hungary)=hu-HU,
            Irish(Ireland)=ga-IE,Italian (Italy)=it-IT,Japanese (Japan)=ja-JP,Korean (Korea)=ko-KR,
            Latvian (Latvia)=lv-LV,Lithuanian (Lithuania)=lt-LT,Maltese(Malta)=mt-MT,
            Marathi (India)=mr-IN,Norwegian (Bokmål, Norway)=nb-NO,Polish (Poland)=pl-PL,Portuguese (Brazil)=pt-BR,
            Portuguese (Portugal)=pt-PT,Romanian (Romania)=ro-RO,Russian (Russia)=ru-RU,=,Slovak (Slovakia)=sk-SK,
            Slovenian (Slovenia)=sl-SI,Spanish (Argentina)=es-AR,Spanish (Bolivia)=es-BO,Spanish (Chile)=es-CL,
            Spanish (Colombia)=es-CO,Spanish (Costa Rica)=es-CR,Spanish (Cuba)=es-CU,Spanish (Dominican Republic)=es-DO,
            Spanish (Ecuador)=es-EC,Spanish (El Salvador)=es-SV,Spanish (Equatorial Guinea)=es-GQ,
            Spanish (Guatemala)=es-GT,Spanish (Honduras)=es-HN,Spanish (Mexico)=es-MX,=,Spanish (Nicaragua)=es-NI,
            Spanish (Panama)=es-PA,Spanish (Paraguay)=es-PY,Spanish (Peru)=es-PE,Spanish (Puerto Rico) = es-PR,
            Spanish (Spain) = es-ES,  = , Spanish (Uruguay) = es-UY, Spanish (USA) = es-US, Spanish (Venezuela) = es-VE,
            Swedish (Sweden) = sv-SE, Tamil (India) = ta-IN, Telugu (India) = te-IN, Thai (Thailand) = th-TH,
            Turkish (Turkey) = tr-TR

        Returns:
            An extracted speech text in JSON result
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {'To': audio_language}
            files = {'file': open(wav_audio_file_path, 'rb')}

            response_from_aspace = connector.createMultipartPostRequest(api_url, apikey,files ,payload)
            result_message = response_from_aspace.text

        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)
            result_message = json.dumps(result_message)

        return result_message




    def text_to_speech(text, text_lang):
        """Perform text to speech for a given text supports SSML
        Args:
            text: Text to be converted to speech
            text_lang: default = en-US-AriaNeural

            Supported Languages : Arabic (Egypt) = ar-EG-SalmaNeural , Arabic (Egypt) = ar-EG-ShakirNeural 
            Arabic (Saudi Arabia) = ar-SA-ZariyahNeural Arabic (Saudi Arabia) = ar-SA-HamedNeural 
            Bulgarian (Bulgaria) = bg-BG-KalinaNeural Bulgarian (Bulgaria) = bg-BG-BorislavNeural 
            Catalan (Spain) = ca-ES-AlbaNeural Catalan (Spain) = ca-ES-JoanaNeural  Catalan (Spain) = ca-ES-EnricNeural 
            Chinese (Cantonese, Traditional) = zh-HK-HiuGaaiNeural Chinese (Cantonese, Traditional) = zh-HK-HiuMaanNeural 
            Chinese (Cantonese, Traditional) = zh-HK-WanLungNeural  Chinese (Mandarin, Simplified) = zh-CN-XiaoxiaoNeural 
            Chinese (Mandarin, Simplified) = zh-CN-XiaoyouNeural Chinese (Mandarin, Simplified) = zh-CN-YunyangNeural 
            Chinese (Mandarin, Simplified) = zh-CN-YunyeNeural Chinese (Taiwanese Mandarin) = zh-TW-HsiaoChenNeural 
            Chinese (Taiwanese Mandarin) = zh-TW-HsiaoYuNeural Chinese (Taiwanese Mandarin) = zh-TW-YunJheNeural 
            Croatian (Croatia) = hr-HR-GabrijelaNeural Croatian (Croatia) = hr-HR-SreckoNeural  Czech (Czech) = cs-CZ-VlastaNeural 
            Czech (Czech) = cs-CZ-AntoninNeural  Danish (Denmark) = da-DK-ChristelNeural Danish (Denmark) = da-DK-JeppeNeural  
            Dutch (Netherlands) = nl-NL-ColetteNeural Dutch (Netherlands) = nl-NL-FennaNeural  Dutch (Netherlands) = nl-NL-MaartenNeural  
            English (Australia) = en-AU-NatashaNeural English (Australia) = en-AU-WilliamNeural English (Canada) = en-CA-ClaraNeural 
            English (Canada) = en-CA-LiamNeural  English (India) = en-IN-NeerjaNeural English (India) = en-IN-PrabhatNeural  
            English (Ireland) = en-IE-EmilyNeural English (Ireland) = en-IE-ConnorNeural  English (United Kingdom) = en-GB-LibbyNeural 
            English (United Kingdom) = en-GB-MiaNeural English (United Kingdom) = en-GB-RyanNeural 
            English (United States) = en-US-AriaNeural English (United States) = en-US-JennyNeural  
            English (United States) = en-US-GuyNeural Finnish (Finland) = fi-FI-NooraNeural Finnish (Finland) = fi-FI-SelmaNeural 
             Finnish (Finland) = fi-FI-HarriNeural  French (Canada) = fr-CA-SylvieNeural French (Canada) = fr-CA-JeanNeural French (France) = fr-FR-DeniseNeural 
             French (France) = fr-FR-HenriNeural French (Switzerland) = fr-CH-ArianeNeural French (Switzerland) = fr-CH-FabriceNeural  German (Austria) = de-AT-IngridNeural 
             German (Austria) = de-AT-JonasNeural  German (Germany) = de-DE-KatjaNeural German (Germany) = de-DE-ConradNeural German (Switzerland) = de-CH-LeniNeural 
             German (Switzerland) = de-CH-JanNeural  Greek (Greece) = el-GR-AthinaNeural Greek (Greece) = el-GR-NestorasNeural  Hebrew (Israel) = he-IL-HilaNeural 
             Hebrew (Israel) = he-IL-AvriNeural  Hindi (India) = hi-IN-SwaraNeural Hindi (India) = hi-IN-MadhurNeural  Hungarian (Hungary) = hu-HU-NoemiNeural 
             Hungarian (Hungary) = hu-HU-TamasNeural  Indonesian (Indonesia) = id-ID-GadisNeural  Indonesian (Indonesia) = id-ID-ArdiNeural Italian (Italy) = it-IT-ElsaNeural 
             Italian (Italy) = it-IT-IsabellaNeural Italian (Italy) = it-IT-DiegoNeural Japanese (Japan) = ja-JP-NanamiNeural Japanese (Japan) = ja-JP-KeitaNeural 
             Korean (Korea) = ko-KR-SunHiNeural Korean (Korea) = ko-KR-InJoonNeural Malay (Malaysia) = ms-MY-YasminNeural Malay (Malaysia) = ms-MY-OsmanNeural  
             Norwegian (Bokmål, Norway) = nb-NO-IselinNeural Norwegian (Bokmål, Norway) = nb-NO-PernilleNeural  Norwegian (Bokmål, Norway) = nb-NO-FinnNeural  
             Polish (Poland) = pl-PL-AgnieszkaNeural  Polish (Poland) = pl-PL-ZofiaNeural Polish (Poland) = pl-PL-MarekNeural  Portuguese (Brazil) = pt-BR-FranciscaNeural 
             Portuguese (Brazil) = pt-BR-AntonioNeural Portuguese (Portugal) = pt-PT-FernandaNeural Portuguese (Portugal) = pt-PT-RaquelNeural 
              Portuguese (Portugal) = pt-PT-DuarteNeural  Romanian (Romania) = ro-RO-AlinaNeural Romanian (Romania) = ro-RO-EmilNeural  Russian (Russia) = ru-RU-DariyaNeural 
              Russian (Russia) = ru-RU-SvetlanaNeural  Russian (Russia) = ru-RU-DmitryNeural  Slovak (Slovakia) = sk-SK-ViktoriaNeural Slovak (Slovakia) = sk-SK-LukasNeural  
              Slovenian (Slovenia) = sl-SI-PetraNeural Slovenian (Slovenia) = sl-SI-RokNeural  Spanish (Mexico) = es-MX-DaliaNeural Spanish (Mexico) = es-MX-JorgeNeural 
              Spanish (Spain) = es-ES-ElviraNeural Spanish (Spain) = es-ES-AlvaroNeural Swedish (Sweden) = sv-SE-HilleviNeural Swedish (Sweden) = sv-SE-SofieNeural  
              Swedish (Sweden) = sv-SE-MattiasNeural  Tamil (India) = ta-IN-PallaviNeural Tamil (India) = ta-IN-ValluvarNeural  Telugu (India) = te-IN-ShrutiNeural 
              Telugu (India) = te-IN-MohanNeural  Thai (Thailand) = th-TH-AcharaNeural Thai (Thailand) = th-TH-PremwadeeNeural Thai (Thailand) = th-TH-NiwatNeural  
              Turkish (Turkey) = tr-TR-EmelNeural Turkish (Turkey) = tr-TR-AhmetNeural  Vietnamese (Vietnam) = vi-VN-HoaiMyNeural Vietnamese (Vietnam) = vi-VN-NamMinhNeural 

        Returns:
            An .wav file with speech
        """
        try:
            api_url = aspaceai.ASPACE_API_URL
            apikey = aspaceai.ASPACE_API_KEY

            payload = {'text': text , 'text_lang':text_lang}
            json_payload = json.dumps(payload)
            response_from_aspace = connector.createJSONPostRequest(api_url, apikey,json_payload)
            if response_from_aspace.status_code == 200:
                return ("success",response_from_aspace)
            else:
                return ("failed", "Error in conversion : Please check the parameters provided.")


        except  Exception as e:
            return ("failed" , str(e))
