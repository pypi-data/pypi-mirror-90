# -*- coding: utf-8 -*-
# @Team : SANY Heavy Energy DataTeam
# @Time    : 2020/10/22 16:02 下午
# @Author  : THao

import json
import os
import uuid
import warnings
import logging
import logging.handlers

import arrow
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def clean_limit_power_5min(data, max_power, limit_p=True):
    """
    对5分钟数据去除限功率、启停机前后、并网发生变化前后等状态的数据
    :param data:5分钟原始数据，pandas.DataFrame
    :param max_power: 额定功率
    :param limit_p:是否根据桨叶角度等去除限功率点
    :return: 去除之后的dataframe
    """
    df_power = data.copy()
    df_power['ys_index'] = df_power.index
    df_power = df_power[df_power['变流器发送的平均功率'] > 0]
    df_power = df_power.dropna(
        subset=[
            '平均风速',
            '变流器发送的平均功率']).reset_index(
        drop=True)

    # 去除限功率
    df_power = df_power[(df_power['平均限功率百分比'] == 100) &
                        (df_power['轴1桨叶实际位置平均值'] >= 0)]

    # 去除系统停机以及停机前后数据点
    df_power = df_power.sort_values(by='日期').reset_index(drop=True)
    df_power['System_ok_diff1'] = df_power['System OK'].diff()
    df_power = df_power.sort_values(
        by='日期', ascending=False).reset_index(
        drop=True)
    df_power['System_ok_diff2'] = df_power['System OK'].diff()
    condition1 = df_power['System_ok_diff1'] != 1
    condition2 = df_power['System_ok_diff2'] != 1
    condition3 = df_power['System OK'] != 0
    df_power = df_power[condition1 & condition2 & condition3]

    if limit_p:
        # 去除并网次数发生改变前后的数据点
        df_power = df_power.sort_values(by='日期').reset_index(drop=True)
        df_power['并网次数_diff'] = df_power['并网次数'].diff()
        nums = np.where(df_power['并网次数_diff'] != 0)[0].tolist()
        if len(nums) > 0:
            nums.pop(0)
        nums_1 = [x - 1 for x in nums]
        df_power = df_power[~(df_power.index.isin(nums))
                            & ~(df_power.index.isin(nums_1))]

        # 根据桨距角进行筛选
        df_power['平均桨距角'] = (df_power['轴1桨叶实际位置平均值'] + df_power['轴2桨叶实际位置平均值'] +
                             df_power['轴3桨叶实际位置平均值']) / 3

        condition1 = df_power['变流器发送的平均功率'] < max_power * 0.7
        condition2 = df_power['变流器发送的平均功率'] >= max_power * 0.7
        condition3 = df_power['变流器发送的平均功率'] < max_power * 0.8
        condition4 = df_power['变流器发送的平均功率'] >= max_power * 0.8
        condition5 = df_power['变流器发送的平均功率'] < max_power * 0.9
        condition6 = df_power['变流器发送的平均功率'] >= max_power * 0.9
        condition7 = df_power['平均桨距角'] < 0.5
        condition8 = df_power['平均桨距角'] < 1
        condition9 = df_power['平均桨距角'] < 5

        df_power = df_power[(condition1 & condition7) |
                            (condition2 & condition3 & condition8) |
                            (condition4 & condition5 & condition9) |
                            condition6]
    return df_power


def time_group(data, by='time', max_skip_sec=5):
    """
    # 对原始输入按照时间连续性分组，筛选满足条件的组别
    :param data: 原始数据，pandas.DataFrame
    :param by: 时间列名
    :param max_skip_sec: 最大间隔秒数，超过该秒数，则将划分为不同的组别
    :return: 分组后的pandas.DataFrame，增加组别号time_group与组内数据长度length
    """

    df = data.copy()
    df_result = None
    try:
        df['date_time'] = pd.to_datetime(df[by])
        df = df.sort_values('date_time')
        df['time_diff'] = [i.total_seconds()
                           for i in df['date_time'].diff()]  # 求前后时间差分的秒数
        df = df.iloc[1:].reset_index(drop=True)
        df['time_group'] = (df['time_diff'] > max_skip_sec).cumsum()  # 按照时间连续性分组
        temp = df.groupby('time_group', as_index=False)[
            'time_group'].agg({'length': 'count'})
        df_result = df.merge(temp, how='left', on='time_group')
    except Exception as e:
        print(e)
    return df_result


def split_list(list_x, n):
    """
    对输入的list_x平均分成n个子list
    :param list_x: list
    :param n: int
    :return: 嵌套list，[[], [], []]
    """
    if n > len(list_x):
        n1 = [1] * len(list_x)
    else:
        a1 = len(list_x) // n
        a2 = len(list_x) % n
        n1 = [a1] * (n - a2) + [a1 + 1] * a2
    res = list()
    s = 0
    for i in n1:
        res.append(list_x[s:s + i])
        s += i
    return res


def utc2bj(utc):
    """
    utc时间转换为北京时间，在utc时间上加8小时为北京时间
    :param utc: string, "%Y-%m-%dT%H:%M:%SZ"
    :return: string，"%Y-%m-%d %H:%M:%S"
    """
    from datetime import datetime
    from datetime import timedelta
    utc_format = "%Y-%m-%dT%H:%M:%SZ"
    bj_format = "%Y-%m-%d %H:%M:%S"
    utc = datetime.strptime(utc, utc_format)
    # 格林威治时间+8小时变为北京时间
    bj = utc + timedelta(hours=8)
    bj = bj.strftime(bj_format)
    return bj


def theoretical_pw_fit(theoretical_pw, real_pw, real_wname='平均风速',
                       theoretical_wname='Wind', theoretical_pname='Power'):
    """
    根据理论功率曲线，计算实际风速下功率值
    :param theoretical_pw: 理论功率曲线数据，pandas.DataFrame
    :param real_pw: 真实数据，需包含真实风速值，pandas.DataFrame
    :param real_wname: 真实数据中风速对应的列名，string
    :param theoretical_wname: 理论功率曲线数据中对应的风速列名，string
    :param theoretical_pname: 理论功率曲线数据中对应的功率列名，string
    :return: pandas.DataFrame， 新增一列predict_power
    """
    from sklearn import ensemble
    theoretical_power_curve = theoretical_pw.copy()
    df_real = real_pw.copy()
    model = ensemble.RandomForestRegressor(n_estimators=50)
    model.fit(theoretical_power_curve[theoretical_wname].values.reshape(-1, 1),
              theoretical_power_curve[theoretical_pname].values.reshape(-1, 1))
    predict_wind = df_real[real_wname].to_list()
    predict_power = model.predict(np.array(predict_wind).reshape(-1, 1))
    predict_power[np.where(np.array(predict_wind) < 3)] = 0
    df_real['predict_power'] = predict_power

    return df_real


def xy_fit(data, x_name, y_name, predict_x=None):
    """
    对指定的x_name与y_name，进行回归拟合，返回拟合之后的y值
    :param data: 原始数据数据，pandas.DataFrame
    :param x_name: x对应的列名
    :param y_name: y对应的列名
    :param predict_x: 需要预测的其他x值, list
    :return: 拟合之后的y值，list
    """
    from sklearn import ensemble
    df = data.copy()
    model = ensemble.RandomForestRegressor(n_estimators=50)
    model.fit(df[x_name].values.reshape(-1, 1), df[y_name].values.reshape(-1, 1))
    if not predict_x:
        predict_x = df[x_name].to_list()
    predict_y = model.predict(np.array(predict_x).reshape(-1, 1)).tolist()

    return predict_y


def init_logger(log_path, log_name, max_gigabyte=5, backup_count=1):
    """
    初始化日志
    :param log_path: 日志存放路径
    :param log_name: 日志文件名
    :return: 初始化日志对象
    :param max_gigabyte: 单个文件最大GB，默认5
    :param backup_count: 备份数量，默认1
    """
    os.makedirs(log_path, exist_ok=True)
    date_fmt = '%a, %d %b %Y %H:%M:%S'
    format_str = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(format_str, date_fmt)
    handler = logging.handlers.RotatingFileHandler(os.path.join(log_path, log_name),
                                                   maxBytes=1024 * 1024 * max_gigabyte, backupCount=backup_count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def ago_month(n, now):
    """
    根据给定日期的月份，获取其前n月的第一天和最后一天的日期
    :param n:需要计算月份的前n月，int
    :param now:需要计算的月份，"%Y-%m-%d"，str
    :return:当前月份的前n月的第一天和最后一天，"%Y-%m-%d"，str
    """
    from datetime import datetime
    from datetime import timedelta
    import calendar

    now = datetime.strptime(now, '%Y-%m-%d')
    month_start = datetime(now.year, now.month, 1)
    month_end = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
    for i in range(n):
        month_end = month_start - timedelta(days=1)
        month_start = datetime(month_end.year, month_end.month, 1)

    month_start = month_start.strftime('%Y-%m-%d')
    month_end = month_end.strftime('%Y-%m-%d')

    return month_start, month_end


def get_args(days=30):
    """
    返回模型计算所需要数据的起止时间
    :param days:当前时间前days天作为start_time,当前时间为end_time，如果调用该方法时为某月的1日，且days为30，则
    start_time、end_time分别为上月的1日与最后一天的日期
    :return:包含开始与结束时间的字典，dict，例：{'start_time': '2020-11-04', 'end_time': '2020-12-05'}
    """
    args = dict()
    if days == 30 and arrow.now().strftime('%d') == '01':
        now_time = arrow.now().strftime('%Y-%m-%d')
        start_time, end_time = ago_month(1, now_time)
        args['start_time'] = start_time
        args['end_time'] = end_time
    else:
        end_time = arrow.now()
        start_time = end_time.shift(days=-days).strftime('%Y-%m-%d')
        end_time = end_time.strftime('%Y-%m-%d')
        args['start_time'] = start_time
        args['end_time'] = end_time

    task_args = os.getenv('TaskArgs')
    if task_args and isinstance(json.loads(task_args), dict):
        task_args = json.loads(task_args)
        if 'start_time' in task_args and 'end_time' in task_args:
            args = task_args

    return args


def get_file_path(file_local_path, file_upload_path, farm, name, args, png_name, file_type='png'):
    """
    获取文件在本地与云端保存的完整路径名
    :param file_local_path: 本地文件路径，str
    :param file_upload_path: 云端文件路径，str
    :param farm: 风场名，例如：SXZFFC，str
    :param name: 机组号、机型号或其他标示名，str
    :param args: 模型计算的开始与结束时间组成的字典，例如：{'start_time': '2020-11-04', 'end_time': '2020-12-05'}，dict
    :param png_name: 图片或其他文件名，例如：区分子图与主图，湍流图分为玫瑰图和线图，则png_name分别为：turbulence_rose和turbulence_line，str
    :param file_type: 文件类型，例如：png，csv等，str
    :return:
    """
    local_path = '{}/sanydata_frpc_{}_{}_{}_{}.{}'.format(file_local_path, farm, name, png_name,
                                                          uuid.uuid1(), file_type)
    # 上传cos的路径
    upload_path = '{}/{}/{}_{}_{}_{}_{}.{}'.format(file_upload_path, farm, name, png_name, args['start_time'],
                                                   args['end_time'], uuid.uuid1(), file_type)

    return local_path, upload_path


def put_plt_json(dt, stub, file_local_path, file_upload_path, plt_data_json, farm, file_name, json_name, args):
    """
    上传绘图的json数据文件
    :param dt: grpc接口对象
    :param stub: 接口url地址
    :param file_local_path: 本地json文件路径
    :param file_upload_path: 云端json文件路径
    :param plt_data_json: 绘图的json数据
    :param farm: 风场名，str
    :param file_name: 机组号、机型号或其他标示名，str
    :param json_name: 绘图数据的json名，例如：区分子图与主图，湍流图分为玫瑰图和线图，则json_name分别为：turbulence_rose和turbulence_line，str
    :param args: 模型计算的开始与结束时间组成的字典，例如：{'start_time': '2020-11-04', 'end_time': '2020-12-05'}，dict
    :return: 上传绘图文件的结果
    """
    local_json_file, upload_json_path = get_file_path(file_local_path, file_upload_path, farm, file_name,
                                                      args, json_name, 'json')

    json_out = open(local_json_file, "w")
    json_out.write(json.dumps(plt_data_json))
    json_out.close()
    cos_json_path = dt.put_files(stub, [local_json_file], [upload_json_path])
    cos_json_path = cos_json_path[0] if 'put_file error' not in cos_json_path[0] else None

    return cos_json_path
