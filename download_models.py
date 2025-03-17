import os
import yaml
import requests
from git import Repo
import tqdm
from pathlib import Path

class ModelDownloader:
    def __init__(self, repo_url, yaml_dir, output_dir):
        """初始化下载器
        
        Args:
            repo_url: 仓库URL
            yaml_dir: yaml文件目录路径
            output_dir: 模型保存目录
        """
        self.repo_url = repo_url
        self.yaml_dir = yaml_dir
        self.output_dir = output_dir
        
    def clone_repo(self):
        """克隆仓库"""
        print("正在克隆仓库...")
        if not os.path.exists("X-AnyLabeling"):
            Repo.clone_from(self.repo_url, "X-AnyLabeling")
        print("仓库克隆完成")
            
    def get_yaml_files(self):
        """获取所有yaml文件路径"""
        yaml_path = os.path.join("X-AnyLabeling", self.yaml_dir)
        return [f for f in os.listdir(yaml_path) if f.endswith('.yaml')]
    
    def download_file(self, url, save_path):
        """下载单个文件
        
        Args:
            url: 下载链接
            save_path: 保存路径
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            
            with open(save_path, 'wb') as f:
                with tqdm.tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
                    for data in response.iter_content(block_size):
                        f.write(data)
                        pbar.update(len(data))
                        
            print(f"文件下载完成: {save_path}")
            return True
            
        except Exception as e:
            print(f"下载失败 {url}: {str(e)}")
            return False
            
    def process_yaml(self, yaml_file):
        """处理单个yaml文件
        
        Args:
            yaml_file: yaml文件名
        """
        yaml_path = os.path.join("X-AnyLabeling", self.yaml_dir, yaml_file)
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 获取模型名称作为文件夹名
        model_name = config.get('name', 'unknown')
        model_dir = os.path.join(self.output_dir, model_name)
        os.makedirs(model_dir, exist_ok=True)
        
        # 收集所有模型URL
        model_urls = []
        
        # 检查encoder
        if 'encoder' in config:
            if isinstance(config['encoder'], dict):
                model_urls.extend(self._extract_urls(config['encoder']))
            elif isinstance(config['encoder'], list):
                for enc in config['encoder']:
                    model_urls.extend(self._extract_urls(enc))
                    
        # 检查decoder
        if 'decoder' in config:
            if isinstance(config['decoder'], dict):
                model_urls.extend(self._extract_urls(config['decoder']))
            elif isinstance(config['decoder'], list):
                for dec in config['decoder']:
                    model_urls.extend(self._extract_urls(dec))
        
        # 下载所有模型文件
        for url in model_urls:
            if url:
                filename = url.split('/')[-1]
                save_path = os.path.join(model_dir, filename)
                if not os.path.exists(save_path):
                    print(f"正在下载: {url}")
                    self.download_file(url, save_path)
                else:
                    print(f"文件已存在,跳过: {save_path}")
                    
    def _extract_urls(self, config_dict):
        """从配置字典中提取所有URL
        
        Args:
            config_dict: 配置字典
        Returns:
            URL列表
        """
        urls = []
        for key, value in config_dict.items():
            if isinstance(value, str) and 'model_path' in key.lower():
                if value.startswith('http://') or value.startswith('https://'):
                    urls.append(value)
            elif isinstance(value, dict):
                urls.extend(self._extract_urls(value))
        return urls
    
    def run(self):
        """运行下载器"""
        # 克隆仓库
        self.clone_repo()
        
        # 获取所有yaml文件
        yaml_files = self.get_yaml_files()
        print(f"找到 {len(yaml_files)} 个yaml文件")
        
        # 处理每个yaml文件
        for yaml_file in yaml_files:
            print(f"\n处理yaml文件: {yaml_file}")
            self.process_yaml(yaml_file)

if __name__ == "__main__":
    # 配置参数
    REPO_URL = "https://github.com/CVHub520/X-AnyLabeling.git"
    YAML_DIR = "anylabeling/configs/auto_labeling"
    OUTPUT_DIR = "downloaded_models"
    
    # 创建并运行下载器
    downloader = ModelDownloader(REPO_URL, YAML_DIR, OUTPUT_DIR)
    downloader.run() 