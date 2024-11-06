# ФУДЗИЯМА - создание японских кроссвордов

## Описание

Программа "ФУДЗИЯМА" позволяет создавать японские кроссворды (нонограммы) из изображения с возможностью настройки параметров и экспорта результата в виде файлов в формате PDF.

## Установка и запуск

1. Убедитесь, что у вас установлены необходимые библиотеки (подробнее - в файле requirements.txt):
   - `matplotlib`
   - `numpy`
   - `PIL` (Pillow)

2. Запустите программу.

## Интерфейс программы

### Основные элементы

- **Выбрать файл**: Кнопка для выбора изображения.
- **Экспорт**: Кнопка для экспорта нонограммы в PDF файл.
- **Белое поле**: Поле для отображения метаданных выбранного изображения.
- **Слайдер**: Ползунок для выбора порога бинаризации изображения, для тонкой настройки. Порог определяет, какие пиксели будут считаться черными, а какие — белыми. Значение порога может варьироваться от 1 до 255
- **Radiobuttons**: Радиокнопки для выбора типа экспорта.
  - Только задача - пустая сетка для разгадывания головоломки
  - Только решение - уже закрашенные квадраты
  - Обе нонограммы
- **Checkbox**: Чекбокс для инверсии изображения (белые квадраты-пиксели станут черными и наоборот)..

### Метаданные изображения

После выбора изображения в белом поле отобразятся следующие метаданные:
- Путь к выбранному изображению.
- Размер изображения (если размер превышает 80x80 пикселей, программа при экспорте автоматически уменьшит его до указанного размера).

## Использование программы

1. **Выбор изображения**:
   - Нажмите кнопку "Выбрать файл". Для лучшей работы программы рекомендуется выбирать простые и контрастные изображения. Пример "tigr.png" находится в папке с проектом.
   - В открывшемся диалоговом окне выберите изображение в формате `.jpg`, `.jpeg`, `.png`, `.gif` или `.bmp`, нажмите OK.

2. **Настройка параметров**:
   - Установите необходимый порог бинаризации с помощью ползунка (по желанию).
   - Выберите тип экспорта с помощью радио кнопок. По умолчанию экспортируется только задача.
   - Если необходимо, установите флажок "Инвертировать" для инверсии изображения.

3. **Экспорт нонограммы**:
   - Нажмите кнопку "Экспорт".
   - В зависимости от выбранного режима будут созданы файлы:
     - TASK.pdf — файл с задачей (пустая сетка).
     - SOLVE.pdf — файл с решением (заполненная сетка).
    
После экспорта файлов программа продолжает работать, позволяя выбрать другое изображение или изменить настройки бинаризации. Чтобы завершить работу, просто закройте окно программы.

