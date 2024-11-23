# CloudflareSaaSOptim

Cloudflare 回源优选IP自动更新脚本

## 用法

1. 自行下载适合本机的[CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)并运行;
2. 复制`config.example.toml`为`config.toml`;
3. 修改`config.toml`中的配置;
4. 运行`run.py`.

## 配置

以下是一个简单的配置文件示例, 使用阿里云DNS:

```toml
[cloudflare_st]
result_file = "result.csv"

[dns_provider.alidns]
access_key_id = "YOUR ALIDNS ACCESS KEY ID"
access_key_secret = "YOUR ALIDNS ACCESS KEY SECRET"

[[dns]]
provider = "alidns"
domain = "a.example.org"
line = "default"

[[dns]]
provider = "alidns"
domain = "b.example.org"
line = "default"
```

你需要修改`dns_provider.alidns`下的`access_key_id`和`access_key_secret`为自己的API密钥. 

你可以通过新建RAM用户, 赋予其`AliyunDNSFullAccess`权限, 并创建AccessKey获得.

`dns`数组中可以添加多个DNS记录, 每个DNS记录必须包含 `provider`(DNS提供商), `domain`(域名) 两个字段, 此处还添加了`line`(解析线路) 配置.

**请注意, 并不是每个DNS服务商都支持此字段.**

## 支持的DNS服务商

- [x] 阿里云DNS

更多服务商请提交Issue或自行实现, 欢迎PR.