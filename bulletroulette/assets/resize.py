from PIL import Image
from os import chdir
chdir("/home/gqx/codelab/BulletRoulette/bulletroulette/assets/")
for i in ["knife.png","magnifier.png","smoke.png","handcuff.png","beer.png"]:
    image = Image.open(i)
    image = image.resize((100,200))
    image.save(i)