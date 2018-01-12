# 自动化测试框架使用说明

该框架主要使用selenium进行web的自动化测试，但不仅仅限制于UI的自动化测试，请保持与aicp的ui自动化测试联合使用，可达到最佳的效果。


# 使用说明

## 安装部署
```
//进行测试
python setup.py test
//安装到库里
python setup.py install
//生成安装包到dist目录下
python setup.py sdist
```

## 驱动driver的安装

需要下载相关的driver放到系统path路径下
Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/