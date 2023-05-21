import pandas as pd
from fuzzywuzzy import fuzz


def merge_regions_and_herbs():
    df_soil_regions = pd.read_csv('data/region_soils.csv', header=None)
    df_herbs_info = pd.read_csv('data/herbs_info.csv', header=None)

    # Создание третьей таблицы
    df_result = pd.DataFrame(columns=['name', 'region', 'area', 'soil'])

    # Проход по каждой записи в таблице herbs_info
    for index, row in df_herbs_info.iterrows():
        herb_name = row[0]
        herb_area = row[1]

        # Нахождение совпадений по полю area (или его корню) между таблицами
        matching_regions = []
        matching_area = []
        matching_soil = []
        for idx, region_row in df_soil_regions.iterrows():
            region_name = region_row[0]
            region_area = region_row[1]
            region_soil = region_row[2]

            # Проверка на пустые значения
            if not pd.isnull(herb_area):
                # Сравнение area и его корня с использованием fuzzy matching
                if region_name not in matching_regions and fuzz.partial_ratio(herb_area, region_name) >= 70:
                    matching_regions.append(region_name)
                    matching_area.append(region_area)
                    matching_soil.append(region_soil)
                if region_area not in matching_regions and fuzz.partial_ratio(herb_area, region_area) >= 70:
                    matching_regions.append(region_name)
                    matching_area.append(region_area)
                    matching_soil.append(region_soil)
            else:
                matching_regions.append('')
                matching_area.append('')
                matching_soil.append('')

        temp_df = pd.DataFrame(
            {'name': [herb_name] * len(matching_regions), 'region': matching_regions, 'area': matching_area, 'soil': matching_soil})
        df_result = pd.concat([df_result, temp_df], ignore_index=True)

    # Вывод результата
    df_result.to_csv('data/name_region_area.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    merge_regions_and_herbs()
