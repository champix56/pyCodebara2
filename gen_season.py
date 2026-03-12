from codebara.seasons.generator import generer_combinaisons
from codebara.seasons.season import seasonsFilter
import http.client
import os
import base64
import json
from io import BytesIO
from pathlib import Path
from PIL import Image
from codebara.config.config import IMAGE_IA_GEN_BODY_BASE, IMAGE_IA_GEN_ENDPOINT_GEN, IMAGE_IA_GEN_ENDPOINT_METHOD,IMAGE_IA_GEN_REST_URL
__DEBUG=False
seasons=seasonsFilter()

for season in seasons:
    combinaisons = generer_combinaisons(season)
    #seedBase=prompt['seed']
    for c in combinaisons:
        for i in range(1,7):
            print(i)
            cs=c.split('/')
            prompt=dict(IMAGE_IA_GEN_BODY_BASE)
            #seedBase=prompt['seed']
            if __DEBUG is True:
                prompt['image_height'] =64
                prompt['image_width'] =64
                prompt['inference_steps' ]=1
            prompt['prompt']=cs[1]
            prompt['seed']+=i
            my_file = Path('.'+season['ressourcesFolder']+'/'+cs[0]+'_'+str(prompt['seed'])+".png")
            if not my_file.is_file():
                try:
                    host = IMAGE_IA_GEN_REST_URL
                    conn = http.client.HTTPConnection(host)
                    conn.request(
                        method=IMAGE_IA_GEN_ENDPOINT_METHOD,
                        url=IMAGE_IA_GEN_ENDPOINT_GEN,
                        body=json.dumps(prompt),
                        headers={"Host": host, "Content-Type": "application/json"},
                    )
                    response = conn.getresponse()
                    print(response.status, response.reason)
                    data1 = response.read()
                    string = data1.decode("utf-8")
                    jsonObj = json.loads(string)
                    #print(jsonObj["images"][0])
                    conn.close()
                    if os.path.isdir('.'+season['ressourcesFolder']) is not True:
                        os.makedirs('.'+season['ressourcesFolder'])
                    """with open('.'+season['ressourcesFolder']+'/'+cs[0]+".json", "w") as fout:
                        json.dump(jsonObj, fout)"""
                    file_content = jsonObj["images"][0]
                    image_bytes = base64.b64decode(file_content)
                    image = Image.open(BytesIO(image_bytes))
                    image.save(my_file,optimize=True, format="PNG")
                except Exception as e:
                    print("error http")
                    print(e)
                print("request IA")
                
        print(c)

print("Total:", len(combinaisons))
#genImagesOfSeason(season=seasonsFilter()[0])