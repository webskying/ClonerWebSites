# 网站克隆工具 (Site Cloner)

一个强大的Python网站克隆工具，用于下载和本地化网站内容，支持资源文件下载和路径重写。
![Image text](https://github.com/webskying/ClonerWebSites/blob/main/clonerwebsite.gif)
## 功能特点

- 🚀 支持完整网站克隆，包括子页面递归下载
- 📦 自动下载并本地化CSS、JavaScript、图片等资源文件
- 🔄 智能处理相对路径和绝对路径
- 🎯 支持中文URL路径
- 📱 模拟真实浏览器请求
- ⚡ 带进度条的下载显示
- 🛠 自动创建目录结构
- 💪 支持断点重试机制

## 环境要求

- Python 3.6+

## 依赖库

```bash
pip install requests
pip install beautifulsoup4
pip install tqdm
```

## 主要依赖说明

- `requests`: 处理HTTP请求
- `beautifulsoup4`: HTML解析
- `tqdm`: 显示进度条
- `urllib`: URL处理（Python标准库）
- `os`: 文件系统操作（Python标准库）
- `re`: 正则表达式（Python标准库）

## 使用方法

1. 克隆或下载代码到本地
2. 安装所需依赖
3. 修改主程序中的配置：

```python
if __name__ == "__main__":
    site_url = "https://your-target-website.com"    # 目标网站URL
    output_dir = "path/to/output/directory"         # 输出目录
    clone_site(site_url, output_dir)
```

## 功能说明

### 资源下载支持
- CSS样式文件
- JavaScript脚本
- 图片资源
- 字体文件
- 网站图标
- 内联样式中的URL资源

### 特殊处理
- 自动处理相对路径和绝对路径
- URL解码支持（处理中文路径）
- 保持原始目录结构
- 资源文件路径重写
- 失败重试机制

## 注意事项

1. 请确保有足够的磁盘空间
2. 注意网站的robots.txt规则
3. 建议设置适当的下载延迟，避免对目标服务器造成压力
4. 某些网站可能限制爬虫访问
5. 部分动态加载的资源可能无法获取

## 代码示例

```python
# 基础使用
clone_site("https://example.com", "./output")

# 自定义配置示例
headers = {
    'User-Agent': 'Your Custom User Agent',
    'Accept': 'text/html,application/xhtml+xml...',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
```

## 错误处理

- 下载失败时会自动重试（默认3次）
- 每次重试之间有1秒延迟
- 错误信息会打印到控制台

## TODO功能

- [ ] 添加并发下载支持
- [ ] 支持下载限速
- [ ] 添加更多文件类型支持
- [ ] 支持自定义过滤规则
- [ ] 添加断点续传功能

## 许可证

MIT License

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 免责声明
代码仅供学习，不涉及任何商业用途！

本工具仅供学习和研究使用，请勿用于非法用途。使用本工具时请遵守相关网站的使用条款和robots.txt规则。
