# LOF-Fund-Tools
中国市场LOF基金套利工具，免费铲子，使用AKshare做数据源。
使用时需要有Python环境。安装以下库：
akshare
flask
pandas
numpy

用浏览器访问http://127.0.0.1:5000 可以看到基金数据。  系统默认过滤条件：日成交量大于500000元，且溢价率大于0.3%或折价率大于0.7%的基金。数据来源：https://xueqiu.com/8228564016/147153325
如果有特殊需求可以修改filter_funds函数。
系统默认以溢价率的绝对值排序，如图。
<img width="1040" alt="image" src="https://github.com/mydreamworldpolly/LOF-Fund-Tools/assets/35619739/ec59d225-cfe4-4315-b085-2763a5a18159">

作为一个极其简易的工具，每次刷新时会获取数据，网页显示较慢，敬请谅解。希望它可以帮助更多的小散户获得LOF套利的机会，不用花钱买铲子。
附主动型LOF套利框架总结，QDII套利也可以参考。
![image](https://github.com/mydreamworldpolly/LOF-Fund-Tools/assets/35619739/2536c091-850d-4cf6-9d99-e447e5b4957f)



Free LOF fund arbitrage tool,  using AKShare as the data source.

To use this, you need to have a Python environment set up. Please install the following libraries:

akshare
flask
pandas
numpy

To view the fund data, you can access http://127.0.0.1:5000 in your web browser.

The system's default filter conditions are: daily trading volume greater than 500,000 yuan, and a premium rate greater than 0.3% or a discount rate greater than 0.7% for the funds. If you have special requirements, you can modify the filter_funds function.

The system by default sorts the funds by the absolute value of the premium rate in descending order. The information is displayed as shown in the image.

As an extremely simple tool, it will fetch data each time it refreshes, so the webpage may load slowly. Please understand. Hopefully, it can help more retail investors get opportunities for LOF arbitrage without having to pay for shovels (tools).
