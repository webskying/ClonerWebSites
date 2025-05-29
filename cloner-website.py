import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from tqdm import tqdm
import os
import re
import time

def download_file(url, local_path, headers, retry=3):
    for i in range(retry):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            if i == retry - 1:
                print(f"下载失败 {url}: {str(e)}")
            time.sleep(1)
    return False

def get_resource_links(soup, url):
    resources = []
    # CSS文件
    resources.extend([(link.get('href'), '.css', link) for link in soup.find_all('link', rel='stylesheet')])
    # JavaScript文件
    resources.extend([(script.get('src'), '.js', script) for script in soup.find_all('script', src=True)])
    # 图片文件
    resources.extend([(img.get('src'), '', img) for img in soup.find_all('img', src=True)])
    # 字体文件
    resources.extend([(link.get('href'), '', link) for link in soup.find_all('link', rel=['font', 'preload'])])
    # 图标文件
    resources.extend([(link.get('href'), '', link) for link in soup.find_all('link', rel=['icon', 'shortcut icon'])])
    # 内联样式中的url()
    for style in soup.find_all('style'):
        urls = re.findall(r'url\([\'"]?([^\'"]+)[\'"]?\)', style.string or '')
        resources.extend([(url, '', None) for url in urls])
    
    return resources

def clone_site(url, output_dir, visited=None):
    if visited is None:
        visited = set()
    
    if url in visited:
        return
    
    visited.add(url)
    print(f"\n正在克隆: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # 先确定页面保存路径
        page_path = os.path.join(output_dir, parsed_url.path.lstrip('/') or 'index.html')
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        
        # 获取并下载资源
        resources = get_resource_links(soup, url)
        
        with tqdm(total=len(resources), desc="下载资源") as pbar:
            for resource_url, ext, element in resources:
                if resource_url:
                    # 处理相对路径
                    full_url = urljoin(url, resource_url)
                    if full_url.startswith(('http://', 'https://')):
                        parsed_resource = urlparse(full_url)
                        # 解码URL，处理中文路径
                        local_path = os.path.join(output_dir, 
                                                parsed_resource.netloc,
                                                unquote(parsed_resource.path.lstrip('/'))) 
                        
                        if download_file(full_url, local_path, headers):
                            # 更新HTML中的路径
                            try:
                                if element is not None:
                                    rel_path = os.path.relpath(local_path, os.path.dirname(page_path))
                                    if ext == '.css':
                                        element['href'] = rel_path
                                    elif ext == '.js':
                                        element['src'] = rel_path
                                    elif 'src' in element.attrs:
                                        element['src'] = rel_path
                                    elif 'href' in element.attrs:
                                        element['href'] = rel_path
                            except Exception as e:
                                print(f"更新路径失败: {str(e)}")
                
                pbar.update(1)
        
        # 收集子页面链接
        subpages = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.startswith('/') or href.startswith(domain):
                subpages.append(urljoin(url, href))
        
        # 保存修改后的HTML
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        # 递归克隆子页面
        for subpage in subpages:
            if subpage.startswith(domain):
                clone_site(subpage, output_dir, visited)
                
    except Exception as e:
        print(f"克隆出错: {str(e)}")

if __name__ == "__main__":
    site_url = "https://your-target-website.com"    # 目标网站URL
    output_dir = "path/to/output/directory"         # 输出目录
    clone_site(site_url, output_dir)
    print(f"\n网站克隆完成！文件保存在: {output_dir}")
