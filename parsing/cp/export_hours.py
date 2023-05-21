from datetime import datetime
import requests

from bs4 import BeautifulSoup

import csv

tmp_regions = """Алтайский край--1511736
Амурская область--2027487
Архангельская область--581049
Астраханская область--580497
Белгородская область--578072
Брянская область--571476
Владимирская область--473247
Волгоградская область--472757
Вологодская область--472459
Воронежская область--472045
Еврейская автономная область--2026643
Забайкальский край--2019326
Ивановская область--580960
Иркутская область--2023469
Кабардино-Балкарская--2026643
Калининградская область--554234
Калужская область--553915
Камчатский край--1501321
Карачаево-Черкесская Республика--552924
Кемеровская область--1503901
Кировская область--548408
Костромская область--543878
Краснодарский край--542420
Красноярский край--795140
Курганская область--1501321
Курская область--538560
Ленинградская область, г. Санкт-Петербург--498817
Липецкая область--535121
Магаданская область--2123628
Московская область, г. Москва--511196
Мурманская область--524305
Ненецкий автономный округ--553766
Нижегородская область--520555
Новгородская область--520555
Новосибирская область--1496747
Омская область--1496153
Оренбургская область--515003
Орловская область--550785
Пензенская область--511565
Пермский край--511196
Приморский край--505269
Псковская область--504341
Республика Адыгея (Адыгея)--483142
Республика Алтай--1511736
Республика Башкортостан--479561
Республика Бурятия--479561
Республика Дагестан--558418
Республика Ингушетия--558418
Республика Калмыкия--558418
Республика Карелия--558418
Республика Коми--558418
Республика Марий Эл--558418
Республика Мордовия--505269
Республика Саха (Якутия)--558418
Республика Северная Осетия - Алания--558418
Республика Татарстан (Татарстан)--558418
Республика Тыва--558418
Республика Хакасия--558418
Ростовская область--558418
Рязанская область--520555
Самарская область--520555
Саратовская область--1501321
Сахалинская область--558418
Свердловская область--558418
Смоленская область--1501321
Ставропольский край--558418
Тамбовская область--558418
Тверская область--558418
Томская область--552924
Тульская область--520555
Тюменская область--1501321
Удмуртская Республика--1501321
Ульяновская область--558418
Хабаровский край--1501321
Ханты-Мансийский автономный округ - Югра--558418
Челябинская -область--552924
Чеченская Республика--552924
Чувашская Республика - Чувашия--558418
Чукотский автономный округ--558418
Ямало-Ненецкий автономный округ--558418
Ярославская область--520555""".split("\n")

regions = [r.split("--")[0] for r in tmp_regions]
towns = [r.split("--")[1] for r in tmp_regions]


def get_hours_town(town_id, month):
    r = requests.get(f"https://dateandtime.info/ru/citysunrisesunset.php?id={town_id}&month={month}&year=2022").text

    soup = BeautifulSoup(r, "html.parser")
    table_body = soup.find_all("table", class_="sunrise_table")[1].find("tbody")

    rows = table_body.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    row = data[0]

    start_time = datetime.strptime(row[1].split("\n")[0], "%H:%M")
    end_time = datetime.strptime(row[2].split("\n")[0], "%H:%M")

    return (end_time - start_time).seconds // 60 // 60


res = []

for i in range(len(regions)):
    region = regions[i]
    town = towns[i]

    tmp = []
    for j in range(1, 11, 3):
        tmp.append(get_hours_town(town, j))

    res.append({
        "region": region,
        "hours": tmp
    })

    print(res[i])

with open('profiles1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["Регион", "Зима", "Весна", "Лето", "Осень"]

    writer.writerow(field)

    for el in res:
        region = el["region"]
        hours = el["hours"]
        writer.writerow([region, hours[0], hours[1], hours[2], hours[3]])