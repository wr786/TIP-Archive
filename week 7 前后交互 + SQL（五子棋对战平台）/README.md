# 文件夹结构

```
│  dbInit.py						// 用于初始化数据库
│  main.py							// 主程序
│  README.md
│
├─data
│      userInfo.db					// 存放用户信息（密码经过sha256加密
│
├─static
│  │  login.html					// 登陆页
│  │  register.html					// 注册页
│  │
│  ├─css
│  │      general.css
│  │
│  ├─img
│  │      favicon.ico
│  │
│  └─js
│          drawMap.js				// 用来画棋盘
│          jquery.min.js			// jQuery
│
└─templates
        index.html					// 对战页面
        loginStatus.html			// 登陆状态
        registerStatus.html			// 注册状态
```

