import pandas as pd


def fix_data():
    # Чтение CSV-файла
    df = pd.read_csv('data/medicinal_herbs_data.csv', header=None)

    # Удаление нумерации и символа "-"
    df[0] = df[0].str.replace(r'^\d+\.\s*', '', regex=True)  # Удаление нумерации
    # Удаление символа "-" и всего, что следует за ним
    df[0] = df[0].str.split('-', n=1).str[0].str.strip()

    # Сохранение изменений в CSV-файле
    df.to_csv('fixed_medicinal_herbs_data.csv', index=False, header=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fix_data()
