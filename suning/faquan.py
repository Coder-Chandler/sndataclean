import time
import pandas as pd
import os


def log():
    pass


# 累计报表只需要下面几个活动归属名称
act_belongto_name = [
    '会员营销',
]
shiyebu_name = [
    '百货',
    '数码',
    '母婴',
    '汽车',
    '体育',
    '通讯',
    '冰洗',
    '小家电',
    '黑店',
    '电脑',
    '红孩子',
    '超市',
    '空调',
    '厨卫',
    '海外购',
]


class DataClean(object):
    def __init__(self, dirty_data_path):
        self.path = dirty_data_path

    def data_clean(self):
        # 读取文件路径至pandas转换为dataframe
        read_df = pd.read_excel(self.path)
        # 选取excel表中需要的字段
        df = read_df[['活动名称', '活动类型', '发起事业部', '发券量', '用券量', '用券金额', '付款金额']]
        # 整个df只要活动归属名称在act_belongto_name这个列表中的所有数据
        df = df[df['活动类型'].isin(act_belongto_name)]
        df['发起事业部'] = df['发起事业部'].fillna('xxx')
        print(df['发起事业部'].iloc[95])
        # 循环遍历df的所有索引
        # for i in df.index:
        #
        #     print(df['发起事业部'].iloc[i])
        #     # 判断如果是短信渠道就要删除'买家数4', '打开会员数', 'UV'这三个列的所有数据并赋值为0
        #     if df['发起事业部'].iloc[i] is None:
        #         for j in shiyebu_name:
        #             if j in df['活动名称'].iat[i]:
        #                 df['发起事业部'].iat[i] = j
        # print(df)


            # # 否则就要删除'计划发送会员数', '买家数2'这二个列的所有数据并赋值为0
            # if df['渠道'].iloc[i] != '短信':
            #     df['计划发送会员数'].iat[i] = 0
            #     df['买家数2'].iat[i] = 0
            #
            #     # 整个df只要活动归属名称在act_belongto_name这个列表中的所有数据
            #     df = df[df['活动归属名称'].isin(act_belongto_name)]
            #     # 对处理后的dataframe重新索引（删除一些数据，索引可能出错，比如出现0，1，2，3，12，13这样的断点）
            #     df = df.reset_index(drop=True)
            #     # 将处理好的数据导出为excel格式文件
            #     df.to_excel(os.path.dirname(self.path) + '/clean_data.xlsx')
            #     # 返回并调用pivot_baibiao函数生成数据透视表
            #     return self.pivot_baibiao(df)

    def pivot_baibiao(self, df):
        # 生成数据透视表按照求和聚合函数计算每一列数据
        pivot_ = pd.pivot_table(df, index='活动归属名称', aggfunc='sum')
        # 增加三列数据，按照要求计算新增列数据
        pivot_['营销数量'] = pivot_['打开会员数'] + pivot_['计划发送会员数']
        pivot_['贡献买家数'] = pivot_['买家数2'] + pivot_['买家数4']
        pivot_['转化率'] = pivot_['贡献买家数'] / pivot_['营销数量']
        # 将处理好的透视表保存为excel文件
        pivot_.to_excel(os.path.dirname(self.path) + '/clean_data_pivot.xlsx')
        return self.leiji_baobiao_output(pivot_)

    def leiji_baobiao_output(self, df):
        total_yingxiaonum = 0
        total_gxbuyer = 0
        excel_path = os.path.dirname(self.path) + '/example_output.xlsx'
        # 读取文件路径至pandas转换为dataframe
        read_df = pd.read_excel(excel_path, sheetname='leiji')

        for i in read_df.index:
            name = str(read_df['事业部'][i])
            for j in df.index:
                if name in str(j):
                    read_df['营销数量'].iat[i] = df['营销数量'][j]
                    read_df['贡献买家数'].iat[i] = df['贡献买家数'][j]
                    read_df['转化率'].iat[i] = df['转化率'][j]

        for j in read_df.index:
            name = str(read_df['事业部'][j])
            if name != '小计':
                total_yingxiaonum += read_df['营销数量'][j]
                total_gxbuyer += read_df['贡献买家数'][j]
            else:
                read_df['营销数量'].iat[j] = total_yingxiaonum
                read_df['贡献买家数'].iat[j] = total_gxbuyer
                read_df['转化率'].iat[j] = total_gxbuyer / total_yingxiaonum

                total_yingxiaonum = 0
                total_gxbuyer = 0
        read_df = read_df.fillna(0)
        for k in read_df.index:
            if read_df['贡献买家数指标'][k] and read_df['转化率指标'][k] not in [0, '-']:
                read_df['累计达成贡献买家数'].iat[k] = float(read_df['贡献买家数'][k]) / float(read_df['贡献买家数指标'][k])
                read_df['累计达成转化率'].iat[k] = float(read_df['转化率'][k]) / float(read_df['转化率指标'][k])

        heji_yingxiaonum = 0
        heji_gxbuyer = 0
        for v in read_df.index:
            if read_df['事业部'][v] == '小计':
                heji_yingxiaonum += read_df['营销数量'][v]
                heji_gxbuyer += read_df['贡献买家数'][v]
            if read_df['类目'][v] == '合计':
                read_df['营销数量'].iat[v] = heji_yingxiaonum
                read_df['贡献买家数'].iat[v] = heji_gxbuyer
                if read_df['营销数量'][v] and read_df['贡献买家数'][v] not in [0, '-']:
                    read_df['转化率'].iat[v] = float(read_df['贡献买家数'][v]) / float(read_df['营销数量'][v])

                read_df['累计达成贡献买家数'].iat[v] = float(read_df['贡献买家数'][v]) / float(read_df['贡献买家数指标'][v])
                read_df['累计达成转化率'].iat[v] = float(read_df['转化率'][v]) / float(read_df['转化率指标'][v])

            buyer_60 = read_df['累计达成贡献买家数'][v]
            zhuanhua_40 = read_df['累计达成转化率'][v]
            if buyer_60 >= 1 and zhuanhua_40 >= 1:
                read_df['达成评估'].iat[v] = 100
            if buyer_60 >= 1 and zhuanhua_40 < 1:
                read_df['达成评估'].iat[v] = 60 + zhuanhua_40 * 40
            if buyer_60 < 1 and zhuanhua_40 >= 1:
                read_df['达成评估'].iat[v] = buyer_60 * 60 + 40
            if buyer_60 < 1 and zhuanhua_40 < 1:
                read_df['达成评估'].iat[v] = buyer_60 * 60 + zhuanhua_40 * 40

        read_df.to_excel(os.path.dirname(self.path) + '/leiji_baobiao.xlsx')
        return


if __name__ == '__main__':
    t1 = time.time()
    path = '/Users/chandler/Documents/Projects/sndataclean/faquan/20180614faquan/faquan.xlsx'
    excel_path = path
    data_clean = DataClean(dirty_data_path=excel_path)
    df = data_clean.data_clean()
    # print('报表处理完成，保存路径与报表文件所在路径相同')
    # t2 = time.time()
    # print('报表处理用时 : {0}{1}'.format(t2 - t1, 's'))
    #
    # excel_path = '/Users/chandler/Documents/Projects/sndataclean/leiji/5.1-5.24_leiji/dirty_data.xlsx'

s = '/Users/chandler/Documents/Projects/sndataclean/leiji/6.1-6.13_leiji/6.12baobiao/dirty_data.xlsx'
