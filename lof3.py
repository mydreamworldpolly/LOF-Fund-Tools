# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:06:30 2024

@author: polly
"""

import akshare as ak
import pandas as pd
import numpy as np
from flask import Flask, render_template_string
from concurrent.futures import ThreadPoolExecutor

def fetch_fund_data():
    """Fetch and process data from Akshare."""
    def fetch_lof_spot():
        return ak.fund_lof_spot_em()
    
    def fetch_value_estimation():
        return ak.fund_value_estimation_em()
    
    def fetch_purchase_info():
        return ak.fund_purchase_em().drop(columns=["序号", "基金简称"])
    
    with ThreadPoolExecutor() as executor:
        lof_future = executor.submit(fetch_lof_spot)
        value_estimation_future = executor.submit(fetch_value_estimation)
        purchase_info_future = executor.submit(fetch_purchase_info)
        
        fund_lof_spot_df = lof_future.result()
        fund_value_estimation_df = value_estimation_future.result()
        fund_purchase_df = purchase_info_future.result()

    fund_lof_spot_df = fund_lof_spot_df.reset_index()[['代码', '最新价', '成交额', '涨跌幅', '换手率']]
    lof_list = fund_lof_spot_df["代码"].values

    fund_value_estimation_df = fund_value_estimation_df[fund_value_estimation_df['基金代码'].isin(lof_list)]
    fund_value_estimation_df = fund_value_estimation_df.drop(fund_value_estimation_df.columns[[0, 4, 5, 6, 7, 8]], axis=1)
    fund_value_estimation_df = fund_value_estimation_df.rename(columns={fund_value_estimation_df.columns[2]: '估值'})

    result_df = pd.merge(fund_value_estimation_df, fund_lof_spot_df, left_on='基金代码', right_on='代码', how='left')
    result_df = result_df.drop(columns=['代码'])
    result_df = pd.merge(result_df, fund_purchase_df, on='基金代码', how='left')

    return result_df

def preprocess_data(df):
    """Preprocess the fetched data."""

    df = df.replace('---', np.nan)
    df['估值'] = df['估值'].astype(float)
    df['最新价'] = df['最新价'].astype(float)
    df['成交额'] = df['成交额'].fillna(0).astype(int)
    df['涨跌幅'] = df['涨跌幅'].astype(float)
    df['换手率'] = df['换手率'].astype(float)
    df['最新净值'] = df['最新净值/万份收益'].astype(float)
    df['购买起点'] = df['购买起点'].astype(int)
    df['日累计限定金额'] = df['日累计限定金额'].astype('int64')
    df['手续费'] = df['手续费'].astype(float)

    return df

def calculate_premium_rate(df):
    """Calculate the premium rate for the funds."""
    #计算基金溢价率。尽量用最新估值计算，如无法估值则用最新净值（QDII）
    def calc_rate(row):
        if pd.notnull(row['估值']):
            return row['最新价'] / row['估值'] - 1
        else:
            return row['最新价'] / row['最新净值'] - 1
    
    df['溢价率'] = df.apply(calc_rate, axis=1) * 100
    df['溢价率'] = df['溢价率'].round(2)
    df['溢价率abs'] = abs(df['溢价率'])

    return df

def filter_funds(df):
    """Filter funds based on trading volume and premium rate criteria."""
    #筛选成交额较高、折价或溢价明显、有潜在套利机会的基金
    df = df[df["成交额"] >= 500000]
    df = df[((df["溢价率"] >= 0.3) & (df["申购状态"] != "暂停申购")) | 
            ((df["溢价率"] <= -0.7) & (df["赎回状态"] != "暂停赎回"))]
    
    return df

def format_dataframe(df):
    """Format the dataframe columns and order."""
    df = df.sort_values(by='溢价率abs', ascending=False)
    new_column_order = [
        '基金代码', '基金名称', '溢价率', '成交额', '日累计限定金额', '换手率', 
        '手续费', '申购状态', '赎回状态', '最新价', '最新净值/万份收益', '估值', 
        '购买起点', '涨跌幅', '基金类型', '最新净值/万份收益-报告时间', 
        '最新净值', '下一开放日', '溢价率abs'
    ]
    df = df.reindex(columns=new_column_order)
    df = df.drop(columns=['购买起点', '下一开放日', '溢价率abs', '最新净值/万份收益'])
    df = df.rename(columns={'最新净值/万份收益-报告时间': '净值日期', '日累计限定金额': '限额'})

    return df

def main():
    """Main function to fetch, process, and display fund data."""

    # Display data using Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        # Fetch and process data
        result_df = fetch_fund_data()
        result_df = preprocess_data(result_df)
        result_df = calculate_premium_rate(result_df)
        result_df = filter_funds(result_df)
        result_df = format_dataframe(result_df)
        
        return render_template_string(
            """
            <!doctype html>
            <html lang="zh-cn">
              <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <title>基金信息</title>
              </head>
              <body>
                <h1>LOF套利分析工具 by Polly</h1>
                <table border="1">
                  <thead>
                    <tr>
                      {% for col in df.columns %}
                      <th>{{ col }}</th>
                      {% endfor %}
                    </tr>
                  </thead>
                  <tbody>
                    {% for row in df.iterrows() %}
                    <tr>
                      {% for cell in row[1] %}
                      <td>{{ cell }}</td>
                      {% endfor %}
                    </tr>
                    {% endfor %}
                  </tbody>
                </table>
              </body>
            </html>
            """,
            df=result_df
        )

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

# Run the main function
main()
