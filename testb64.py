"""import base64
base64_output=''
with open('./contents/user/666/169.cdz', 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_output = base64_encoded_data.decode('utf-8')

    print(base64_output)"""
from codebara.cards.cardgen import setCardName
import asyncio

asyncio.run(setCardName(uid=666,cid=170,name='toto'))
    

