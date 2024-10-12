# - підключення модулів
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os

from PIL import Image,ImageFilter,ImageEnhance

# - об'єкт-додаток та вікно програми.
app = QApplication([])

win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor (By Vitalik)')
win.show()

win.setStyleSheet("background-color: rgb(0,200,250)")

# Віджети - кнопки, надписи та список
btn_file = QPushButton("Папка")
btn_left = QPushButton("Ліворуч")
btn_right = QPushButton("Праворуч")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_blur = QPushButton("Розмиття")
btn_black_white = QPushButton("Ч/Б")
btn_emboss = QPushButton("Тиснення")
btn_brightness = QPushButton("Яскравість")
btn_contrast = QPushButton("Контрастність")

btn_file.setStyleSheet("background-color: rgb(0,250,0); color: rgb(0,0,250)")
btn_left.setStyleSheet("background-color: rgb(0,115,0)")
btn_right.setStyleSheet("background-color: rgb(0,120,0)")
btn_mirror.setStyleSheet("background-color: rgb(0,150,0)")
btn_sharp.setStyleSheet("background-color: rgb(0,175,0)")
btn_blur.setStyleSheet("background-color: rgb(0,250,0)")
btn_black_white.setStyleSheet("background-color: rgb(0,205,0)")
btn_emboss.setStyleSheet("background-color: rgb(0,210,0)")
btn_brightness.setStyleSheet("background-color: rgb(0,220,0)")
btn_contrast.setStyleSheet("background-color: rgb(0,250,0)")

lbl_picture = QLabel("Картинка")
lbl_picture.setStyleSheet("font-size: 25px; color: rgb(0,70,250)")

list_file = QListWidget()        # список віддетів
list_file.setStyleSheet("background-color: rgb(170,0,250); font-family: Times New Roman")

# Макет - Лінії
v1 = QVBoxLayout()
v2 = QVBoxLayout()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
main_layout = QHBoxLayout()

v1.addWidget(btn_file)         # у першому – кнопка вибору директорії та список файлів
v1.addWidget(list_file)

h1.addWidget(btn_left)         # кнопки з фільтрами
h1.addWidget(btn_right)
h1.addWidget(btn_mirror)
h1.addWidget(btn_sharp)
h1.addWidget(btn_black_white)
h1.addWidget(btn_emboss)
h1.addWidget(btn_brightness)
h1.addWidget(btn_contrast)

h2.addWidget(btn_blur)

v2.addWidget(lbl_picture)
v2.addLayout(h1)
v2.addLayout(h2)

main_layout.addLayout(v1)
main_layout.addLayout(v2)

win.setLayout(main_layout)

# -                                                                   [ Завдання №2 ]

# - змінна для збереження імені папки
workdir = ""

# - ---------------  функція вибору робочої папки
def chooseWorkgir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

# - --------------- Функція відбору імен файлів розширень
def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

# - --------------- Відповідає за вибір папки, відбір файлів та відображення їх у віджеті
def showfilenamesList():
    chooseWorkgir()
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    filenames = filter(os.listdir(workdir), extensions)
    list_file.clear()
    for file in filenames:
        list_file.addItem(file)


# -                                                                 [ Завдання №3 ]

class ImageProcessor():

    def __init__(self):
        self.image = None               # поточне зображення
        self.filename = None            # поточне ім'я файлу
        self.dir = None                 # шлях до робочої папки
        self.savedir = 'Modified/'      # ім'я підпапки для збереження змінених картинок


    # -                               завантаження картинки з папки за вибраним ім'ям у списку картинок
    def loadImage(self,filename,dir):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir,filename)   # Зі шляху до робочої папки та імені файлу сформуємо шлях до картинки
        self.image = Image.open(image_path)       # Відкриємо картинку (об'єкт Image), звернувшись за повним шляхом


    # -                  відображення поточного зображення у вікні програми
    def showImage(self):
        # Шлях до тимчасового зображення
        temp_image_path = os.path.join(workdir, self.savedir, self.filename)
        pixmapimage = QPixmap(temp_image_path)                               # - Повним шляхом до файлу створюємо об'єкт QPixmap спеціально для відображення графіки в інтерфейсі.
        w = lbl_picture.width()                                   # - Дізнаємося розміри поля для розміщення картинки
        h = lbl_picture.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)   # - Адаптуємо картинку під розміри поля
        lbl_picture.setPixmap(pixmapimage)                         # - Розміщуємо картинку у віджеті lb_image



    # -                  Збереження Картинки як файла в папку
    def saveImage(self):
        path = os.path.join(workdir, self.savedir)       # Формуємо шлях до папки для збереження

        if not os.path.exists(path):                     # Якщо  Папки для збереження ще немає (перевіряємо чи інснує)?
            os.mkdir(path)                                    # За сформованим шляхом створити нову папку

        image_path = os.path.join(path, self.filename)   # Формуємо шлях до картинки, що зберігається (з ім'ям файлу картинки!)
        self.image.save(image_path)                      # Зберігаємо картинку вбудованим методом класу Image


    # -              чорно біле
    def do_bw(self):
        self.image = self.image.convert("L")    #  Обробляємо поточну картинку вбудованим методом convert()
        self.saveImage()                        #  Зберегти змінений об'єкт Image як файл
        self.showImage()                        #  Відображаємо змінену картинку
    
    
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT) # Відзеркалення (Ліво - Право)
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення
    
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90) # Поворот на 90 градусів (наліво)
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення

    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270) # Поворот на 270 градусів (направо)
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN) # Робить зображення різким
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення
    

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR) # Замилює зображення
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення
    

    def do_emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS) # Зробити тиснення
        self.saveImage() # Зберігаємо зображення
        self.showImage() # Показуємо зображення


    def do_brightness(self, factor=1.5):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)  # Змінює яскравість зображення
        self.saveImage()  # Зберігаємо зображення
        self.showImage()  # Показуємо зображення

    def do_contrast(self, factor=1.5):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)  # Змінює контраст зображення
        self.saveImage()  # Зберігаємо зображення
        self.showImage()  # Показуємо зображення


    def do_brightness(self, factor):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)  # Змінює яскравість зображення
        self.saveImage()  # Зберігаємо зображення
        self.showImage()  # Показуємо зображення


    def do_contrast(self, factor):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)  # Змінює контраст зображення
        self.saveImage()  # Зберігаємо зображення
        self.showImage()  # Показуємо зображення

    


# - створення екземпляра класу
workimage = ImageProcessor()

def showSelectImage():
    if list_file.selectedItems():
        filename = list_file.selectedItems()[0].text()
        workimage.loadImage(filename, workdir)
        workimage.saveImage()  # Зберігаємо одразу оригінальне зображення в директорію "Modified"
        workimage.showImage()  # Відображаємо зображення

# Підключення Функції до кнопок
btn_file.clicked.connect(showfilenamesList) # кнопка папка

list_file.itemClicked.connect(showSelectImage) # превю фотки

btn_black_white.clicked.connect(workimage.do_bw) # чорно біле
btn_mirror.clicked.connect(workimage.do_mirror) # відзеркалення
btn_left.clicked.connect(workimage.do_left) # поворот наліво
btn_right.clicked.connect(workimage.do_right) # поворот направо
btn_sharp.clicked.connect(workimage.do_sharp) # різкість
btn_blur.clicked.connect(workimage.do_blur) # замилювання
btn_emboss.clicked.connect(workimage.do_emboss) # тиснення
btn_brightness.clicked.connect(workimage.do_brightness)
btn_contrast.clicked.connect(workimage.do_contrast)

app.exec()