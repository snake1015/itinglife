#!/usr/bin/env python3
"""
测试数据库路径配置
"""

import os
from database import DATA_DIR, DATABASE_FILE, DATABASE_URL

def test_db_config():
    """测试数据库配置"""
    print("=== 数据库配置测试 ===")
    print(f"数据目录: {DATA_DIR}")
    print(f"数据库文件: {DATABASE_FILE}")
    print(f"数据库URL: {DATABASE_URL}")
    
    # 检查目录是否存在
    if os.path.exists(DATA_DIR):
        print(f"✓ 数据目录存在: {DATA_DIR}")
    else:
        print(f"✗ 数据目录不存在: {DATA_DIR}")
    
    # 检查数据库文件是否存在
    if os.path.exists(DATABASE_FILE):
        print(f"✓ 数据库文件存在: {DATABASE_FILE}")
        file_size = os.path.getsize(DATABASE_FILE)
        print(f"  文件大小: {file_size} 字节")
    else:
        print(f"✗ 数据库文件不存在: {DATABASE_FILE}")
    
    # 检查权限
    if os.access(DATA_DIR, os.W_OK):
        print(f"✓ 数据目录可写: {DATA_DIR}")
    else:
        print(f"✗ 数据目录不可写: {DATA_DIR}")

if __name__ == "__main__":
    test_db_config() 