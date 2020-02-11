import classes
from PIL import Image
import glob
import os
import shutil


K = 4   # кол-во нейронов = кол-ву кластеров
a = 30
b = 30
M = a*b    # кол-во связей в 1 нейроне = кол-ву входных значений (пикселей)
Neurons = []
for j in range(K):
    Neurons.append(classes.Neuron(M))       # массив из нейронов (заполнение)

image_list = []
image_name = []
for filename in glob.glob('image/*.jpg'):
    image_name.append(filename)
    image = Image.open(filename)    # считать изображение
    image_list.append(image)        # сохранить массив изображений
print(len(image_name))
print(image_name)

data_image_list = []
for im in image_list:
    blackImage = im.convert('L')                             # конвертировать изображение в серые тона
    bw = blackImage.point(lambda x: 0 if x < 128 else 1, '1')   # преобразование в черно-белое изображение
    data = list(bw.getdata())                                   # преобразование изображения в список значений: 1-белый, 0-черный
    data_image_list.append(data)

for i in range(50,1,-2):
    u=i*0.01
    print('Epoha - ', u)
    eps = 0
    list_sort = []      # список выигравших нейронов для каждой картинки
    for data in data_image_list:
        Distance = []
        for j in range(K):
            Distance.append(Neurons[j].getR(data))                 # заполнение массива расстояний для каждого нейрона
        list_sort.append(Distance.index(min(Distance)))                             # определение выигр. нейрона
        eps = eps + Neurons[Distance.index(min(Distance))].correction(u, data)      # накопление суммарной ошибки эпохи
    # print(list_sort)
    print(eps)
    if eps < 0.001:
        break

if os.path.exists('sort'):          # проверка на существование папки
    shutil.rmtree('sort')           # удаление папки
os.mkdir('sort')                    # создание папки
for i in range(K):
    os.mkdir('sort/' + str(i))      # создание папок для каждого нейрона
for i in range(len(list_sort)):
    shutil.copy(image_name[i],'sort/'+str(list_sort[i]))    # сортировка изображений копированием


for n in range(K):
    im = Image.new('L', (a, b))     # создание изображения для каждого нейрона
    for i in range(a):
        for j in range(b):
            pix = round(250 * Neurons[n].Links[i*b+j].weight)   # преобразование data в число от 0 до 255 (250, чтобы видеть границы)
            im.putpixel((j, i), (pix))
    im.save('sort/' + str(n) + '/' + str(n)+'.jpg', "JPEG")     # сохранение изображения в папке с нейроном
