import pandas as pd
def print_hi(name):
    # Чтение CSV-файла
    df = pd.read_csv('data/regions.csv')

    # Проверка и исправление ошибки во втором столбце
    df['область'] = df['область'].apply(lambda x: ' '.join(sorted(set(x.split()), key=x.split().index)))

    # Сохранение изменений в CSV-файле
    df.to_csv('new.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
