# ASpace AI API: Python SDK & Sample


This repo contains the Python SDK for the ASpace AI cognitive services, an offering within [ASpace AI Cognitive Services](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)

* [Learn about EY ASpace AI Platform](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)


## Getting started

Install the module using [pip](https://pypi.python.org/pypi/pip/):

```bash
pip install aspaceai
```

Use it:

```python
'''-------------------------------------------------- OCR ------------------------------------------------------'''

import aspaceai
import json


aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image_url = 'https://i.ibb.co/3RHzMqB/eurotext.png'

result = aspaceai.vision.ocr(image=image_url,image_format='url',language='eng')
operation_status = json.loads(result)['status']

if operation_status.lower() == 'success':
    print (json.loads(result)['result'])

else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- PART OF SPEECH ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text = "The quick brown fox jumps over the lazy dog"
result = aspaceai.nlp.part_of_speech(text)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    print (json.loads(result)['result'])
else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- NAMED ENTITY RECOGNITION ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text = "European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"
result = aspaceai.nlp.named_entity_recognition(text)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    print (json.loads(result)['result'])
else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- DEPENDENCY PARSER------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text = "European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"
result = aspaceai.nlp.dependency_parser(text)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    print (json.loads(result)['result'])
else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- TAGS EXTRACTION------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text = "European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"
result = aspaceai.nlp.tags_extraction(text)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    print (json.loads(result)['result'])
else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- FACE DETECTION ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image = "https://www.thestatesman.com/wp-content/uploads/2017/08/1493458748-beauty-face-517.jpg"
image_format = "url"
result = aspaceai.vision.face_detection_image(image,image_format)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    base64_image_string = json.loads(result)['result']['image']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print (json.loads(result)['message'])


'''-------------------------------------------------- EYE DETECTION ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image = "https://www.thestatesman.com/wp-content/uploads/2017/08/1493458748-beauty-face-517.jpg"
image_format = "url"
result = aspaceai.vision.eye_detection(image,image_format)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    base64_image_string = json.loads(result)['result']['image']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print (json.loads(result)['message'])



'''-------------------------------------------------- SMILE DETECTION ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image = "https://st.depositphotos.com/1008939/3024/i/950/depositphotos_30248143-stock-photo-beautiful-woman-smiling.jpg"
image_format = "url"
result = aspaceai.vision.smile_detection(image,image_format)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    base64_image_string = json.loads(result)['result']['image']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print (json.loads(result)['message'])



'''-------------------------------------------------- OBJECT DETECTION ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image = "https://i.pinimg.com/564x/0d/b6/10/0db610089c3e8bfef6c33c3059f70903.jpg"
image_format = "url"
result = aspaceai.vision.object_detection(image, image_format)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':

    objects = json.loads(result)['result']['objects']
    print(objects)

    base64_image_string = json.loads(result)['result']['image']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print(json.loads(result)['message'])



'''-------------------------------------------------- IMAGE CLASSIFICATION ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

image = "https://i.pinimg.com/564x/0d/b6/10/0db610089c3e8bfef6c33c3059f70903.jpg"
image_format = "url"
result = aspaceai.vision.image_classification(image,image_format)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    objects_identified = json.loads(result)['result']
    print(objects_identified)

else:
    print (json.loads(result)['message'])




'''-------------------------------------------------- SENTIMENT ANALYSIS ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text="Hello ASpace World, its a great day !!!"
result = aspaceai.sense.sentiment_analysis(text)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    objects_identified = json.loads(result)['result']
    print(objects_identified)

else:
    print (json.loads(result)['message'])




'''-------------------------------------------------- TRANSLATE ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text="Hello ASpace World, its a great day !!!"
result = aspaceai.nlp.translate(text,"en","hi")

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    objects_identified = json.loads(result)['result']
    print(objects_identified)

else:
    print (json.loads(result)['message'])



'''-------------------------------------------------- QR CREATOR ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text_to_encode = "Hello ASpace World !!!"
result = aspaceai.vision.qr_creator(text_to_encode)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':

    base64_image_string = json.loads(result)['result']['QRCodeImage']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print(json.loads(result)['message'])



'''-------------------------------------------------- BARCODE CREATOR ------------------------------------------------------'''

import aspaceai
import json
import cv2
import numpy as np
import base64

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text_to_encode = "Hello ASpace World !!!"
result = aspaceai.vision.barcode_creator(text_to_encode)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':

    base64_image_string = json.loads(result)['result']['BarCodeImage(base64)']
    jpg_original = base64.b64decode(base64_image_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imshow("Output From ASpaceAI", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows();

else:
    print(json.loads(result)['message'])



'''-------------------------------------------------- QR CODE READER ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

qr_code_image_path = r"C:\Users\<>\Downloads\qr.jpg"

result = aspaceai.vision.qr_reader(qr_code_image_path)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    data = json.loads(result)['result']['data']
    print(data)

else:
    print(json.loads(result)['message'])



'''-------------------------------------------------- BARCODE READER ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

barcode_image_path = r"C:\Users\<>\Downloads\bar.jpg"

result = aspaceai.vision.barcode_reader(barcode_image_path)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    data = json.loads(result)['result']['data']
    print(data)

else:
    print(json.loads(result)['message'])





'''-------------------------------------------------- SPEECH TO TEXT ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

wav_audio_file_path = r"C:\Users\<>\Downloads\audio_sample.wav"
audio_language = "en-IN"

result = aspaceai.speech.speech_to_text(wav_audio_file_path,audio_language)

operation_status = json.loads(result)['status']
if operation_status.lower() == 'success':
    data = json.loads(result)['result']['text']
    print(data)

else:
    print(json.loads(result)['message'])




'''-------------------------------------------------- TEXT TO SPEECH  ------------------------------------------------------'''

import aspaceai
import json

aspaceai.ASPACE_API_URL = '< ASpace AI API endpoint URL >'  # Replace with your aspace endpoint URL
aspaceai.ASPACE_API_KEY = '< ASpace AI API KEY >'  # Replace with a valid Subscription Key here.

text = "Hello ASpace World !!!"
text_lang = "en-US-AriaNeural"

operation_status , result = aspaceai.speech.text_to_speech(text,text_lang)

if operation_status.lower() == 'success':
    with open('text_to_speech.wav', 'wb') as f:
        f.write(result.content)

    # Retrieve HTTP meta-data
    print(result.status_code)
    print(result.headers['content-type'])
    print(result.encoding)



else:
    print(result)


```

### Installing from the source code

```bash
python setup.py install
```
![ASpace AI Themes](https://assets.ey.com/content/dam/ey-sites/ey-com/en_in/topics/consulting/2020/07/aspace/vison-sense.png.rendition.3840.2560.png)
## Contributing

We welcome contributions. Feel free to file issues and pull requests on the repo and we'll address them as we can. Learn more about how you can help on our [Contribution Rules & Guidelines](/CONTRIBUTING.md).

You can reach out to us anytime with questions and suggestions using our communities below:
 - **Support questions:** [StackOverflow](https://stackoverflow.com/questions/tagged/aspaceai)
 
## Updates
* [ASpace.ai Platform Release Notes](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)

## License
All ASpace Cognitive Services SDKs and samples are licensed with the MIT License. For more details, see
[LICENSE](/LICENSE.txt).



## Developer Code of Conduct
Developers using Cognitive Services, including this sample, are expected to follow the “Developer Code of Conduct for ASpace AI”, found at [https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai).