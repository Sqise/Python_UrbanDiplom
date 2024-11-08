import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image

# ===============================================================
# ИМПОРТ


# Функция для выбора файла
def select():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Выберите изображение",
                                                    filetypes=[
                                                        ("Только", ("*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"))])
    if selected_file_path:
        metadata_text_field.delete(1.0, tk.END)
        metadata = {}
        width, height = Image.open(selected_file_path).size

        metadata['Выбрано'] = str(selected_file_path)
        metadata['Размер '] = f"{width} x {height}"

        for key, value in metadata.items():
            metadata_text_field.insert(tk.END, f"{key}: {value}\n")

        if width > 80 or height > 80:
            if width >= height:
                messagebox.showwarning("Предупреждение",
                                       f"Размер файла слишком большой; нонограмма "
                                       f"будет уменьшена до {80} x {int(80 * height / width)}")
            if width < height:
                messagebox.showwarning("Предупреждение",
                                       f"Размер файла слишком большой; нонограмма "
                                       f"будет уменьшена до {int(80 * width / height)} x {80}")

    select_button2.configure(state=tk.ACTIVE)
    return selected_file_path

# ===============================================================
# ЭКСПОРТ


def export():
    # Загрузка и обработка изображения в соответствие с порогом
    binary_img = image_to_array(selected_file_path, int(slider.get()))

    # Генерация подсказок
    row_hints, col_hints = generate_hints(binary_img)

    if selected_option.get() == 'Только решение':
        # Визуализация и сохранение кроссворда в PDF (= РЕШЕНИЕ)
        draw_nonogram(row_hints, col_hints, binary_img, 'gray', output_full_pdf)

    elif selected_option.get() == 'Только задача':
        # Визуализация и сохранение пустой сетки в PDF (= ЗАДАЧА)
        arr = binary_img
        arr[:] = 1
        draw_nonogram(row_hints, col_hints, arr, 'binary', output_empty_pdf)

    else:  # Визуализация обоих файлов - и ЗАДАЧИ и РЕШЕНИЯ
        draw_nonogram(row_hints, col_hints, binary_img, 'gray', output_full_pdf)
        arr = binary_img
        arr[:] = 1
        draw_nonogram(row_hints, col_hints, arr, 'binary', output_empty_pdf)

# ===============================================================
# ОБРАБОТКА


# Преобразование изображения в черно-белый формат и двоичный массив
def image_to_array(selected_file_path, threshold):
    # Открытие изображение и преобразование его в оттенки серого
    img = Image.open(selected_file_path).convert('L')

    # Административное ограничение размера
    width, height = img.size
    if width > 80 or height > 80:
        max_size = (80, 80)
        img.thumbnail(max_size)

    # Преобразование в numpy массив (0 - черный, 1 - белый)
    img = np.array(img)
    if not inverse.get():  # Если не отмечено "Инвертировать"
        binary_img = (img > threshold).astype(int)
    else:  # Если не отмечено "Инвертировать"
        binary_img = (img < threshold).astype(int)
    return binary_img


# Функция для генерации подсказок для строк и столбцов
def generate_hints(binary_img):
    row_hints = []
    col_hints = []

    # Подсказки для всех строк
    for row in binary_img:
        hint = []
        count = 0
        # Подсказки для конкретной строки:
        for pixel in row:
            if pixel == 0:  # Черный пиксель
                count += 1
            else:
                if count > 0:
                    hint.append(count)
                count = 0
        if count > 0:
            hint.append(count)
        row_hints.append(hint if hint else [0])

    # Подсказки для всех столбцов
    for col in binary_img.T:  # Транспонирование для обработки столбцов
        hint = []
        count = 0
        # Подсказки для конкретного столбца:
        for pixel in col:
            if pixel == 0:  # Чёрный пиксель
                count += 1
            else:
                if count > 0:
                    hint.append(count)
                count = 0
        if count > 0:
            hint.append(count)
        col_hints.append(hint if hint else [0])

    return row_hints, col_hints


# Визуализация кроссворда и сохранение в PDF
def draw_nonogram(row_hints, col_hints, binary_img, cmap, export_pdf):
    fig, ax = plt.subplots()

    # Размер сетки
    grid_height = len(row_hints)  # Длина списка (не более 80)
    grid_width = len(col_hints)  # Длина списка (не более 80)

    # Создание изображения для сетки кроссворда
    ax.imshow(binary_img, cmap=cmap)

    # Настройка осей
    ax.set_xticks(np.arange(-0.5, grid_width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid_height, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)

    # Удаление ненужных меток на осях
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    # Добавление необходимых подсказок для строк и столбцов
    for i, hint_row in enumerate(row_hints):
        ax.text(-1, i, f"{'  '.join(map(str, hint_row))}", va='center', ha='right', fontsize=2)

    for j, hint_col in enumerate(col_hints):
        ax.text(j, -1, f"{'\n'.join(map(str, hint_col))}", va='bottom', ha='center', fontsize=2)

    # Сохранение в PDF
    fig.tight_layout()
    plt.savefig(export_pdf, format='pdf', bbox_inches='tight')


# ===============================================================
# ОКНО ПРОГРАММЫ

# Само окно
root = tk.Tk()
root.title("ФУДЗИЯМА - создание японских кроссвордов")
root.geometry("640x360+640+360")
root.iconbitmap("Fuji_s.ico")
root.resizable(False, False)

# Фоновое изображение в окне
background_image = Image.open("Fuji_s.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=str(background_photo))
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Кнопки для выбора файла и экспорта
select_button1 = tk.Button(root, text="Выбрать файл".center(14), command=select)
select_button1.place(x=25, y=200)

select_button2 = tk.Button(root, state=tk.DISABLED, height=3, text="Экспорт".center(20), command=export)
select_button2.place(x=25, y=235)

# Многострочное поле для данных
metadata_text_field = tk.Text(root, height=4, width=60)
metadata_text_field.place(x=130, y=200)

# Метка настроек
label_name = 'Настройки экспорта:'
label = tk.Label(root, text='Настройки экспорта:'.center(26))
label.place(x=250, y=273)

# Слайдер порога бинаризации
slider = tk.Scale(root, from_=1, to=255, orient='horizontal', length=300,
                  label='Порог преобразования (бинаризации)'.center(60), variable=tk.IntVar(value=128))
slider.place(x=25, y=298)

# Radiobutton
selected_option = tk.StringVar()  # Переменная для хранения выбранного значения
selected_option.set('Только задача')  # Установка варианта по умолчанию

option1 = tk.Radiobutton(root, text='Только задача', variable=selected_option, value='Только задача')
option2 = tk.Radiobutton(root, text='Только решение', variable=selected_option, value='Только решение')
option3 = tk.Radiobutton(root, text='Обе нонограммы', variable=selected_option, value='Обе нонограммы')
option1.place(x=355, y=300)
option2.place(x=355, y=330)
option3.place(x=486, y=300)

# Checkbox
inverse = tk.BooleanVar()  # Переменная для хранения состояния чекбокса
checkbox = tk.Checkbutton(root, text="Инвертировать", variable=inverse)
checkbox.place(x=500, y=330)

selected_file_path = ""  # Путь к изображению выбирает пользователь
output_full_pdf = "SOLVE.pdf"  # РЕШЕНИЕ
output_empty_pdf = "TASK.pdf"  # ЗАДАЧА

# Запуск главного цикла
root.mainloop()
