import io
from PIL import Image

from faceapp.faceapp import FaceApp

Fa = FaceApp()
filters = ['smile', 'smile_2', 'hot', 'old', 'young', 'female', 'male']

code = Fa.get_code('./img/paveldurov.jpg')

n = 0
for f in range(len(filters)):
    b = Fa.make_img(code, filters[n])
    image = Image.open(io.BytesIO(b))
    image.save('./img/'+str(filters[n])+'.png')
    n = n + 1
