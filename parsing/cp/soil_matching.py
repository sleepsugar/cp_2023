import csv
import re


def match_name_soil():
    # Открываем исходный CSV-файл для чтения и новый CSV-файл для записи
    with open('data/herbs_info.csv', 'r', newline='') as input_file, open('data/name_soils.csv', 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        # Записываем заголовки в новый файл
        writer.writerow(next(reader))

        # Обрабатываем каждую строку исходного файла
        for row in reader:
            # Разбиваем строку по всем знакам препинания и создаем список
            row_list = re.split(r'[^\w\s]', row[2])

            # Записываем новую строку в новый файл с разбитым списком
            writer.writerow([row[0], ', '.join(row_list)])

    print("Запись в файл завершена.")

def match_region_soil():
    # Открываем исходный CSV-файл для чтения и новый CSV-файл для записи
    with open('data/region_soils.csv', 'r', newline='') as input_file, open('data/output_region_soils.csv', 'w',
                                                                          newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # match_name_soil()
    match_region_soil()
