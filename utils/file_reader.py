import yaml
import os
from xlrd import open_workbook

class YamlReader:
    def __init__(self,yamlfile):
        if os.path.exists(yamlfile):
            self.yamlfile=yamlfile
        else:
            raise FileNotFoundError("文件不存在！")
        self._data=None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlfile, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data


class SheetTypeError(Exception):
    pass

class ExcelReader:
    """
    读取excel文件中的内容。返回list。

    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    # 以下实例展示了zip的使用方法：
                    # >> > a = [1, 2, 3]
                    # >> > b = [4, 5, 6]
                    # >> > c = [4, 5, 6, 7, 8]
                    # >> > zipped = zip(a, b)  # 打包为元组的列表
                    # [(1, 4), (2, 5), (3, 6)]
                    # >> > zip(a, c)  # 元素个数与最短的列表一致
                    # [(1, 4), (2, 5), (3, 6)]
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data


if __name__ == '__main__':
    y = 'C:\\Users\cheng_chen\\PycharmProjects\\UIAutoTest\\config\\config.yml'
    reader = YamlReader(y)
    print(reader.data)

    e = 'C:\\Users\\cheng_chen\\PycharmProjects\\UIAutoTest\\data\\baidu.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)

