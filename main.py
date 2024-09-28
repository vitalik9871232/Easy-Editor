from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import os

app = QApplication([]) 
wind = QWidget()
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


btn_file.clicked.connect(showFilenamesList)


# Показ
wind.show()
app.exec_()