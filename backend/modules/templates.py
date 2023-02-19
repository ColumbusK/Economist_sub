HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  </style>
</head>

<body style="width: 100vw; height: 640px">
  <div style="margin:10px auto; width: 375px; height: 980px; border: 2px solid #999; overflow:hidden">
    <div style="margin:10px auto; width: 95%; height: 30%">
      <img src="cid:image1" alt="" style="width: 100%; height: 100%">
    </div>
    <div style="margin:10px auto; width: 80%; font-size:medium">
      <p><strong style="color: #ff548c;">{{username}}</strong>，你好。 2.0版本网站已上线，新一期经济学人<strong>{{date}}</strong>刊已发布, 请查看! 享受阅读, 祝你天天好心情!</p>
      <p><strong style="color: red;">注意：</strong>全新2.0版本的站点已上线测试，请大家点击下方红色主力网站链接前往下载。为求不被和谐外刊采取资源托管无需跳转网盘，但加载时间较长请耐心等待加载</p>
      <a href="https://newstandshare.azurewebsites.net/" style="text-decoration:none;">
        <strong style="color: red; font-size: larger">主力站点</strong>
      </a>
      <a href="https://newstandshare.herokuapp.com/" style="text-decoration:none;">
        <strong style="color: skyblue;">备用站点</strong>
      </a>
      <p>(PS：如果此项目确实帮助到了您，您可以点击邮件下方的 @哥伦布骑士 前往原视频页面为我一键三连或者分享给需要的人！)
        后续请直接前往网站获取最新一期，注意收藏网址
        <a href="https://newstandshare.azurewebsites.net/" style="text-decoration:none;">
          https://newstandshare.azurewebsites.net
        </a>
      </p>
    </div>
    <div style="margin:0 auto; margin-top: 90px; width: 50%">
      <img src="cid:image2" alt="bilibili干杯（ ゜- ゜）つロ" style="width: 100%">
    </div>
    <a href="https://www.bilibili.com/video/BV17P4y1w7wq#reply119790207136" style="text-decoration:none;">
      <h4 style="margin-bottom: 20px; text-align: center; color: #05affe">@哥伦布骑士</h4>
    </a>
  </div>
</body>

</html>
"""
