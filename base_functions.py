import pandas
import pprint
from pathlib import Path


PRICELIST_CUSTOM = Path.cwd().joinpath('data').joinpath('prices_custom.xlsx')

pp = pprint.PrettyPrinter(indent=3)


def read_excel_column(excelfile, col):
    column = pandas.read_excel(
        excelfile,
        index_col=None,
        usecols=col,
        na_filter=False
        )
    category = column.columns[0]
    column = column.to_dict('tight')['data']

    product_price = {}
    for item in column:
        if len(item[0]) < 1:
            continue
        product_price.update({item[0]: item[1]})
    return {category: product_price}


def read_pricelist_custom():

    file_loc = PRICELIST_CUSTOM

    price_list_custom = {}
    price_list_custom.update(read_excel_column(file_loc, "B:C"))  # Кол-во уров
    price_list_custom.update(read_excel_column(file_loc, "E:F"))  # Форма
    price_list_custom.update(read_excel_column(file_loc, "H:I"))  # Топпинг
    price_list_custom.update(read_excel_column(file_loc, "K:L"))  # Ягоды
    price_list_custom.update(read_excel_column(file_loc, "N:O"))  # Декор

    text_label = pandas.read_excel(
        file_loc,
        index_col=None,
        usecols='Q:Q',
        na_filter=False).to_dict('split')['data'][0][0]

    price_list_custom.update({'Надпись': text_label})  # Надпись

    return price_list_custom


# pp.pprint(read_pricelist_custom())
