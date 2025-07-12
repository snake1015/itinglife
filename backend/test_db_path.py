#!/usr/bin/env python3
"""
测试数据库路径配置
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from database import DATABASE_URL, get_database_url

def test_db_config():
    """测试数据库配置"""
    print("=== 数据库配置测试 ===")
    print(f"当前数据库URL: {DATABASE_URL}")
    print(f"动态获取的URL: {get_database_url()}")
    
    # 检查环境变量
    env_db_url = os.getenv("DATABASE_URL")
    if env_db_url:
        print(f"环境变量DATABASE_URL: {env_db_url}")
    else:
        print("环境变量DATABASE_URL: 未设置")
    
    # 检查data目录
    if os.path.exists("data"):
        print("✓ data目录存在")
        if os.path.exists("data/app.db"):
            file_size = os.path.getsize("data/app.db")
            print(f"✓ data/app.db存在，大小: {file_size} 字节")
        else:
            print("✗ data/app.db不存在")
    else:
        print("✗ data目录不存在")
    
    # 检查当前目录
    if os.path.exists("app.db"):
        file_size = os.path.getsize("app.db")
        print(f"✓ 当前目录app.db存在，大小: {file_size} 字节")
    else:
        print("✗ 当前目录app.db不存在")
    
    # 检查Docker路径
    if os.path.exists("/app"):
        print("✓ /app目录存在（Docker环境）")
        if os.path.exists("/app/data/app.db"):
            file_size = os.path.getsize("/app/data/app.db")
            print(f"✓ /app/data/app.db存在，大小: {file_size} 字节")
        else:
            print("✗ /app/data/app.db不存在")
    else:
        print("✗ /app目录不存在（非Docker环境）")

if __name__ == "__main__":
    test_db_config() 