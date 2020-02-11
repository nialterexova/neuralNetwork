import random
import math

class Link:
    Input = 0
    weight = 1      # весовой коэффициент связи

    def __init__(self, weight):     # создание связи с заданым весовым коэффициентом
        self.weight = weight

    def set_input(self, inp):       # переопределение входного значения связи
        self.Input = inp


class Neuron:
    input_count = 1     # кол-во связей нейрона
    Links = [Link]      # массив связей
    Output = 1          # выходное значение нейрона

    def __init__(self, M):      # создание нейрона с заданым кол-вом связей
        self.input_count = M            # задание кол-ва связей нейрона
        self.Links = []                 # обнуление массива связей
        a = 0.5 - 1 / math.sqrt(M)      # нижний предел весового коэффициента (для нормализации в пределах [0;1]
        b = 0.5 + 1 / math.sqrt(M)      # верхний предел весового коэффициента (для нормализации в пределах [0;1]
        for i in range(M):              # для каждой связи от 1 до М
            w = round(random.uniform(a, b), 1)      # округление рандомного весового коэффициента до 1 знака после запятой
            self.Links.append(Link(w))              # добавление связи с весом w в массив связей нейрона

    def print_info(self):                   # вывод информации о нейроне
        print('Neuron.')
        print('Inputs: ', self.input_count)
        for i in range(self.input_count):
            print(i+1, ') ', self.Links[i].Input, '   ', self.Links[i].weight)
        print('Outputs: ', self.Output)

    def getR(self, InputList):              # получение информации о расстояние нейрона до входных параметров
        summ = 0
        for i in range(self.input_count):
            summ = summ + (InputList[i] - self.Links[i].weight)**2
        self.Output = math.sqrt(summ)
        return self.Output

    def correction(self, u, InputList):     # корректировка весовых коэффициентов
        err = 0
        for i in range(self.input_count):
            w = self.Links[i].weight
            self.Links[i].weight = self.Links[i].weight + u*(InputList[i]-self.Links[i].weight)
            err = err + (w - self.Links[i].weight)
        return math.fabs(err)