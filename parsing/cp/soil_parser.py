import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse

def parsing():
    # Отправляем GET-запрос на страницу с таблицей
    url = 'https://egrpr.esoil.ru/content/2poc.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Находим таблицу с данными
    table = soup.find('table', {'border': '1'})

    # Создаем словарь для хранения регионов и соответствующих типов почв
    data = {}

    # Итерируемся по строкам таблицы
    for row in table.find_all('tr'):
        cells = row.find_all('td')

        # Проверяем, что строка содержит ссылку
        if len(cells) > 0 and cells[0].find('a'):
            link = cells[0].find('a')

            # Получаем текст ссылки (название субъекта РФ)
            subject = link.get_text(strip=True)

            # Переходим по ссылке для получения таблицы с почвами
            sub_url = urllib.parse.urljoin(url, link['href'])
            sub_response = requests.get(sub_url)
            sub_soup = BeautifulSoup(sub_response.content, 'html.parser')

            # Находим таблицу с почвами
            sub_table = sub_soup.find('table', {'border': '1', 'cellspacing': '0', 'cellpadding': '0'})

            # Итерируемся по строкам таблицы с почвами
            for sub_row in sub_table.find_all('tr'):
                sub_cells = sub_row.find_all('td')

                # Проверяем, что строка содержит ссылку на тип почвы
                if len(sub_cells) > 0 and sub_cells[0].find('a'):
                    sub_link = sub_cells[0].find('a')

                    # Получаем текст ссылки (тип почвы)
                    soil_type = sub_link.get_text(strip=True)

                    # Добавляем тип почвы к соответствующему региону в словаре data
                    if subject in data:
                        data[subject].append(soil_type)
                    else:
                        data[subject] = [soil_type]

    # Записываем результаты в CSV-файл
    with open('results/fixed_soils.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Название субъекта РФ', 'Типы почв'])

        for subject, soil_types in data.items():
            writer.writerow([subject, ', '.join(soil_types)])

    print("Парсинг завершен. Результаты сохранены в файле 'результат.csv'.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parsing()