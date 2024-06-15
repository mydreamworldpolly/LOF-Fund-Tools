# LOF-Fund-Tools
中国市场LOF基金套利工具，免费铲子，使用AKshare做数据源。Free LOF fund arbitrage tool,  using AKShare as the data source.

使用时需要有Python环境。安装以下库：To use this, you need to have a Python environment set up. Please install the following libraries:
akshare
flask
pandas
numpy

用浏览器访问http://127.0.0.1:5000 可以看到基金数据。  To view the fund data, you can access http://127.0.0.1:5000 in your web browser.

系统默认过滤条件：日成交量大于500000元，且溢价率大于0.3%或折价率大于0.7%的基金。如果有特殊需求可以修改filter_funds函数。
The system's default filter conditions are: daily trading volume greater than 500,000 yuan, and a premium rate greater than 0.3% or a discount rate greater than 0.7% for the funds. If you have special requirements, you can modify the filter_funds function.

系统默认以溢价率的绝对值排序，从上到下显示信息如图。
The system by default sorts the funds by the absolute value of the premium rate in descending order. The information is displayed from top to bottom as shown in the image.
<img width="1040" alt="image" src="https://github.com/mydreamworldpolly/LOF-Fund-Tools/assets/35619739/ec59d225-cfe4-4315-b085-2763a5a18159">
