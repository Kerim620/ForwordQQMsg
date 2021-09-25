# ForwordQQMsg
该项目配合go-cqhttp实现转发QQ消息到微信

## 原理

使用go-cqhttp监听QQ消息，使用nonebot框架设置监听规则并转发推送QQ消息，推送渠道有pushplus和企业微信渠道。

## 使用方式
1. 下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)，配置config.yml文件：第4、5行填入账号密码，89行的universal填入`ws://127.0.0.1:8881/ws/`，其他均不用设置，完成后运行go-cqhttp。注意，go-cqhttp用来登录QQ监听消息，所以占用一个设备端，默认ipad端。

2. 推送渠道建议使用企业微信渠道，具体可查看 [wechatpush：更便捷地推送微信消息](https://www.zzzjoy.cn/%E9%A1%B9%E7%9B%AE/wechatpush%EF%BC%9A%E6%9B%B4%E4%BE%BF%E6%8D%B7%E5%9C%B0%E6%8E%A8%E9%80%81%E5%BE%AE%E4%BF%A1%E6%B6%88%E6%81%AF/)前半部分教程获取企业微信相关配置。选用pushplus也行，自行上pushplus官网注册
3. 配置config.py，具体怎么填都在文档注释中，自行查看。
4. 运行main.py文件即可。

## 局限

1. go-cqhttp未发布稳定版本，每次更新都会停止程序。
2. 目前只支持转发文本消息和图片消息。视频消息，QQ表情，语音消息等等等等都不支持。

## 效果图

![QQ图片20210925145616](https://gitee.com/zzzjoy/My_Pictures/raw/master/202109251520737.png)

