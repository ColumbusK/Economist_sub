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
  <div style="margin:10px auto; width: 375px; height: 638px; border: 2px solid #999; overflow:hidden">
    <div style="margin:10px auto; width: 95%; height: 30%">
      <img src="cid:image1" alt="" style="width: 100%; height: 100%">
    </div>
    <div style="margin:10px auto; width: 80%; font-size:medium">
      <p><strong style="color: #ff548c;">{{username}}</strong>，你好。 新一期经济学人<strong>{{date}}</strong>刊已送达, 请查收! 享受阅读, 祝你天天好心情!</p>
      <p><strong style="color: red;">注意：</strong>本期经济学人页数较多，导致附件体积过大无法正常发送，因此以阿里云链接形式分享</p>
      <a href="https://www.aliyundrive.com/s/sSS7yNc34vn" style="text-decoration:none;">
      <strong style="color: skyblue;">https://www.aliyundrive.com/s/sSS7yNc34vn</strong>
    </a>
      <p>(PS：如果此项目确实帮助到了您，您可以点击邮件下方的 @哥伦布骑士 前往原视频页面为我一键三连或者分享给需要的人！谢谢啦！)
  !注意: 请不要将此订阅邮件设为垃圾邮件以免影响服务稳定性！</p>
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
