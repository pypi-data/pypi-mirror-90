import os

import numpy as np
import pandas as pd

from mksc.core import reader


def load_data(mode='all', local=True):
    """
    加载配置文件指定数据源，返回数据
    Args:
        mode: 数据集读取类别。
            --“all”: 读取带标签的全部数据集
            --“apply": 读取不带标签的数据集
        local: 是否读取本地pickle对象文件
    Returns:
        data: 配置文件数据框
    """
    cfg = reader.config()
    if mode == 'all':
        mode = 'data'
        sql = cfg.get('DATABASE', 'SQL')
        file = cfg.get('PATH', 'DATA_FILE')
        engine = cfg.get('DATABASE', 'ENGINE_URL')
    elif mode == "apply":
        sql = cfg.get('DATABASE', 'APPLY_SQL')
        file = cfg.get('PATH', 'APPLY_DATA_FILE')
        engine = cfg.get('DATABASE', 'APPLY_ENGINE_URL')
    else:
        raise ValueError("Wrong mode type passed, only accepted [all/apply]")

    if os.path.exists(os.path.join(os.getcwd(), "data", f"{mode}.pickle")):
        file = os.path.join(os.getcwd(), "data", f"{mode}.pickle")

    if local:
        data = reader.file(file)
    else:
        data = pd.read_sql(sql, engine)

    # 大小写标准化
    for c in data.select_dtypes(include=['object']).columns:
        data[c] = data[c].str.lower()

    # 空值标准化
    data.replace("", np.nan, inplace=True)
    data.replace("null", np.nan, inplace=True)
    data.replace("none", np.nan, inplace=True)
    data.replace("na", np.nan, inplace=True)
    return data

def get_variable_type():
    """
    根据指定变量类型的配置表，返回各类型的变量列表

    Returns:
        numeric: 数值型变量列表
        category: 类别型变量列表
        datetime: 日期型变量列表
        label_name: 标签列
        id: 唯一标识列
    """
    variable_type = pd.read_csv("config/variable_type.csv", encoding='gbk')
    label_var = variable_type[variable_type.iloc[:, 2] == 'label']
    numeric_var = variable_type[(variable_type.iloc[:, 2] == 'numeric') & (variable_type.iloc[:, 1] == 1)]
    category_var = variable_type[(variable_type.iloc[:, 2] == 'category') & (variable_type.iloc[:, 1] == 1)]
    datetime_var = variable_type[(variable_type.iloc[:, 2] == 'datetime') & (variable_type.iloc[:, 1] == 1)]
    label_name = label_var['Variable'].tolist()[0]
    numeric = list(numeric_var['Variable'])
    category = list(category_var['Variable'])
    datetime = list(datetime_var['Variable'])
    return numeric, category, datetime, label_name
    
def variable_classify(feature):
    """
    对数据框feature的变量进行分类，返回各类别的变量列表

    Args:
        feature: 待分类的数据框

    Returns:
        numeric_var: 数值型变量列表
        category_var: 类别性变量列表
        datetime_var: 日期型变量列表
    """
    numeric_var = feature.select_dtypes(exclude=['object', 'datetime']).columns
    category_var = feature.select_dtypes('object').columns
    datetime_var = feature.select_dtypes('datetime').columns
    return numeric_var, category_var, datetime_var
