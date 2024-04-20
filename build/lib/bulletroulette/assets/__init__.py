from PIL import Image
from os import chdir,getcwd
print(getcwd())
chdir("Buckshot_Roulette/assets/")
imgaels = ("knife")
image = Image.open("knife.png")
image = image.resize((100,200))
image.save("kifne.png")