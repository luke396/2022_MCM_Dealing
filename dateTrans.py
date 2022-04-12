import pandas as pd

'''对初始日期格式进行更改'''


def dataTrans(date_in):
    date_out = []
    for i in date_in:
        [m, d, y] = i.split('/')
        y = '20' + y
        i_out = '-'.join((y, m, d))
        date_out.append(i_out)
    return date_out


if __name__ == '__main__':
    data1 = pd.read_csv('BCHAIN-MKPRU.csv')
    data2 = pd.read_csv('LBMA-GOLD.csv')
    date_in1 = data1['Date'].values
    date_in2 = data2['Date'].values
    data1['Date'] = dataTrans(date_in1)
    data2['Date'] = dataTrans(date_in2)
    data1.to_excel('BCHAIN-MKPRU_DateChanged.xlsx', index=False)
    data2.to_excel('LBMA-GOLD_DateChanged.xlsx', index=False)
