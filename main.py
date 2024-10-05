from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
import PyQt5.Qt
from PIL import Image
import os

app = QApplication([]) 
wind = QWidget()
wind.setStyleSheet("background-color: rgb(75,155,0)")
wind.resize(700,500)
wind.setWindowTitle("Easy Editor")

# --- Віджети --- #

btn_file = QPushButton("Папка") # Кнопка папка
btn_left = QPushButton("Ліворуч") # Кнопка ліворуч
btn_right = QPushButton("Праворуч") # Кнопка праворуч
btn_mirror = QPushButton("Дзеркало") # Кнопка дзеркало
btn_sharp = QPushButton("Різкість") # Кнопка різкість
btn_blur = QPushButton("Розмиття") # Кнопка розмиття
btn_black_white = QPushButton("Ч/Б") # Кнопка Ч/Б

list_file = QListWidget() # Список файлів
lbl_picture = QLabel("Картинка") # Надпис
list_file.setStyleSheet('background-color: rgb(155,155,65)')
btn_file.setStyleSheet('background-color: rgb(0,55,255)')

# --- Макет --- #

v1 = QVBoxLayout() # Два вертикальних макета
v2 = QVBoxLayout()
h1 = QHBoxLayout() # Два горизонтальних макета
h2 = QHBoxLayout()

main_layout = QHBoxLayout() # Основний макет

v1.addWidget(btn_file)     # Додавання віджетів на перший вертикальний макет
v1.addWidget(list_file)

h1.addWidget(btn_left) # Додавання віджетів на перший горизонтальний макет
h1.addWidget(btn_right)
h1.addWidget(btn_mirror)
h1.addWidget(btn_sharp)
h1.addWidget(btn_black_white)

h2.addWidget(btn_blur) # Додавання віджета на другий горизонтальний макет

v2.addWidget(lbl_picture) # Додавання віджета на другий вертикальний макет
v2.addLayout(h1) # Встановлення першого горизонтального макета на другий вертикальний макет
v2.addLayout(h2) # Встановлення другого горизонтального макета на другий вертикальний макет 

main_layout.addLayout(v1) # Встановлення першого горизонтального макета на основний макет
main_layout.addLayout(v2) # Встановлення другого горизонтального макета на основний макет

wind.setLayout(main_layout) # Встановлення основного макета на основне вікно

# --- Функціонал (Завдання 2) --- #

workdir = "" # Зберігаємо шлях до вказаної папки

# Зберігаємо робочу папку
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory() # Запитуємо у діалоговому вікні шлях до папки

# Відфільтрувати файли
def filter(filenames, extensions):
    result = []    # Список для зберігання назв файлів
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

# Відбір файлів із відображенням їх у віджеті
def showFilenamesList():
    chooseWorkdir()
    extensions = [".jpg",".png",".jpeg",".gif",".bmp"]
    filenames = filter(os.listdir(workdir),extensions)
    list_file.clear()
    for file in filenames:
        list_file.addItem(file)



class ImageProcessor():
    def __init__(self): # Конструктор
        self.Image = None          # Зберігає поточне зображення
        self.filename = None       # Зберігає ім'я поточної картинки
        self.dir = None            # Шлях до зображення
        self.savedir = 'Modified/' # Шлях до модифікованих зображень
    # Знайти зображення за шляхом
    def loadImage(self,filename,dir):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir,filename) # Об'єднання шляхів
        self.Image = Image.open(image_path)
    
    # Функція відображення зображення у вікні програми
    def showImage(self):
        # Шлях до тимчасового зображення
        temp_image_path = os.path.join(workdir,self.savedir,self.filename)
        pixmapImage = QPixmap(temp_image_path)
        w = lbl_picture.width()              # Дізнаємось розміри поля
        h = lbl_picture.height()
        pixmapImage.scaled(w, h, Qt.KeepAspectRatio) # Встановлюємо розмір зображення
        lbl_picture.setPixmap(pixmapImage)   # Встановлюємо зображення у віджеті
    # Зробити зображення Ч/Б
    def b_w(self):
        self.Image = self.Image.convert("L")
        self.saveImage()
        self.showImage()

# Функція збереження зображення
    def saveImage(self):
       path = os.path.join(workdir,self.savedir) # Формуємо шлях до папки збереження модифікованих фото

       if not os.path.exists(path): # Якщо немає папки то створити нову
           os.mkdir(path)

       image_path = os.path.join(path,self.filename) # Повний шлях до модифікованого зображення
       self.Image.save(image_path)  # Зберігаємо зображення за повним шляхом


workImage = ImageProcessor() # Створення екземпляру класу

# Отримати з віджету файл та відобразити у вікні
def showSelectImage():
    if list_file.selectedItems():
       filename = list_file.selectedItems()[0].text()
       workImage.loadImage(filename,workdir)
       workImage.saveImage()        # Збереження у папку модіфікованих зображень
       workImage.showImage()        # Відображаємо



btn_file.clicked.connect(showFilenamesList)

btn_black_white.clicked.connect(workImage.b_w)

list_file.clicked.connect(showSelectImage)



# Показ
wind.show()
app.exec_()