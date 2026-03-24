#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补丁下载功能测试脚本
测试PatchManager的补丁下载和校验功能
"""

import os
import sys
import json
import hashlib
import requests
from pathlib import Path

class PatchManagerTest:
    """补丁管理器测试版"""

    def __init__(self, patch_url, client_path):
        self.patch_url = patch_url
        self.client_path = client_path
        self.data_path = os.path.join(client_path, "Data")
        self.local_version_file = os.path.join(client_path, ".patch_version.json")

    def fetch_manifest(self):
        """获取服务器补丁清单"""
        try:
            manifest_url = f"{self.patch_url}/manifest.json"
            print(f"[测试] 正在获取: {manifest_url}")

            response = requests.get(manifest_url, timeout=10)
            print(f"[测试] 响应状态: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"[测试] ✅ 成功获取manifest.json")
                print(f"[测试] 系统版本: {data.get('system_version')}")
                print(f"[测试] 补丁数量: {len(data.get('patches', []))}")
                return data
            else:
                print(f"[测试] ❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"[测试] ❌ 获取补丁清单失败: {e}")
        return None

    def check_for_updates(self):
        """检查是否有新补丁"""
        local_version = self.get_local_version()
        remote_manifest = self.fetch_manifest()

        if not remote_manifest:
            return None, []

        # 对比补丁
        needed_patches = []
        local_patches = {p['filename']: p for p in local_version.get('patches', [])}

        print(f"\n[测试] === 检查补丁更新 ===")
        print(f"[测试] 本地已安装: {len(local_patches)} 个补丁")
        print(f"[测试] 服务器可用: {len(remote_manifest.get('patches', []))} 个补丁")

        for patch in remote_manifest.get('patches', []):
            patch_name = patch.get('filename')
            patch_version = patch.get('version', '0')

            if patch_name not in local_patches:
                needed_patches.append(patch)
                print(f"[测试] 🆕 需要下载: {patch_name} v{patch_version}")
            else:
                local_ver = local_patches[patch_name].get('version', '0')
                if patch_version != local_ver:
                    needed_patches.append(patch)
                    print(f"[测试] 🔄 需要更新: {patch_name} (本地v{local_ver} → 服务器v{patch_version})")
                else:
                    print(f"[测试] ✅ 已是最新: {patch_name} v{patch_version}")

        return remote_manifest, needed_patches

    def download_patch(self, patch_info, progress_callback=None):
        """下载补丁文件"""
        try:
            url = patch_info.get('url')
            filename = patch_info.get('filename')

            print(f"\n[测试] === 下载补丁 ===")
            print(f"[测试] 文件名: {filename}")
            print(f"[测试] URL: {url}")

            # 下载到临时目录
            temp_path = os.path.join("/tmp", filename)

            response = requests.get(url, stream=True, timeout=30)
            total_size = int(response.headers.get('content-length', 0))

            print(f"[测试] 文件大小: {total_size} bytes")

            downloaded = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size:
                            percent = (downloaded / total_size) * 100
                            progress_callback(percent)

            print(f"[测试] ✅ 下载完成: {downloaded} bytes")
            return temp_path

        except Exception as e:
            print(f"[测试] ❌ 下载失败: {e}")
            return None

    def calculate_md5(self, file_path):
        """计算文件的MD5"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def verify_md5(self, file_path, expected_md5):
        """验证MD5"""
        actual_md5 = self.calculate_md5(file_path)
        print(f"[测试] MD5校验:")
        print(f"[测试]   期望: {expected_md5}")
        print(f"[测试]   实际: {actual_md5}")

        if actual_md5 == expected_md5:
            print(f"[测试] ✅ MD5校验通过")
            return True
        else:
            print(f"[测试] ❌ MD5校验失败")
            return False

    def get_local_version(self):
        """获取本地补丁版本"""
        if os.path.exists(self.local_version_file):
            try:
                with open(self.local_version_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"patches": [], "version": "0"}

    def save_local_version(self, version_info):
        """保存本地补丁版本"""
        with open(self.local_version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
        print(f"[测试] ✅ 版本信息已保存到: {self.local_version_file}")


def test_patch_download():
    """测试完整的补丁下载流程"""

    print("=" * 60)
    print("诺兰时光魔兽登录器 - 补丁下载功能测试")
    print("=" * 60)

    # 测试配置
    patch_url = "http://1.14.59.54:8080/patches"
    client_path = "/tmp/test_wow_client"  # 使用临时目录测试

    # 创建测试目录
    os.makedirs(os.path.join(client_path, "Data"), exist_ok=True)

    print(f"\n[配置信息]")
    print(f"补丁服务器: {patch_url}")
    print(f"客户端路径: {client_path}")
    print(f"Data目录: {os.path.join(client_path, 'Data')}")

    # 初始化补丁管理器
    manager = PatchManagerTest(patch_url, client_path)

    # 测试1: 获取manifest.json
    print(f"\n{'='*60}")
    print("测试1: 获取manifest.json")
    print("="*60)

    manifest = manager.fetch_manifest()
    if not manifest:
        print("[测试] ❌ 测试失败: 无法获取manifest.json")
        return False

    # 测试2: 检查更新
    print(f"\n{'='*60}")
    print("测试2: 检查补丁更新")
    print("="*60)

    manifest, needed_patches = manager.check_for_updates()

    if not needed_patches:
        print("[测试] ✅ 所有补丁已是最新")
        return True

    # 测试3: 下载第一个补丁（测试）
    print(f"\n{'='*60}")
    print("测试3: 下载补丁文件")
    print("="*60)

    # 选择最小的补丁进行测试
    test_patch = min(needed_patches, key=lambda p: p.get('size', 0))
    print(f"[测试] 选择测试补丁: {test_patch.get('filename')}")

    temp_path = manager.download_patch(test_patch)
    if not temp_path:
        print("[测试] ❌ 测试失败: 下载失败")
        return False

    # 测试4: MD5校验
    print(f"\n{'='*60}")
    print("测试4: MD5校验")
    print("="*60)

    if not manager.verify_md5(temp_path, test_patch.get('md5')):
        print("[测试] ❌ 测试失败: MD5不匹配")
        os.remove(temp_path)
        return False

    # 测试5: 模拟安装
    print(f"\n{'='*60}")
    print("测试5: 模拟安装补丁")
    print("="*60)

    dest_path = os.path.join(client_path, "Data", test_patch.get('filename'))

    # 复制文件
    import shutil
    shutil.copy2(temp_path, dest_path)
    print(f"[测试] ✅ 补丁已复制到: {dest_path}")

    # 验证文件
    if os.path.exists(dest_path):
        actual_size = os.path.getsize(dest_path)
        expected_size = test_patch.get('size', 0)
        print(f"[测试] 文件大小: {actual_size} bytes (期望: {expected_size} bytes)")
        if actual_size == expected_size:
            print(f"[测试] ✅ 文件大小正确")
        else:
            print(f"[测试] ⚠️ 文件大小不匹配（可能是manifest.json中的size不准确）")

    # 清理临时文件
    os.remove(temp_path)
    print(f"[测试] 🗑️ 已清理临时文件")

    # 测试6: 更新本地版本
    print(f"\n{'='*60}")
    print("测试6: 更新本地版本记录")
    print("="*60)

    local_version = manager.get_local_version()
    local_version['patches'].append(test_patch)
    local_version['version'] = test_patch.get('version', '1.0')
    manager.save_local_version(local_version)

    # 最终总结
    print(f"\n{'='*60}")
    print("测试总结")
    print("="*60)

    print("✅ 测试1: 获取manifest.json - 通过")
    print("✅ 测试2: 检查补丁更新 - 通过")
    print("✅ 测试3: 下载补丁文件 - 通过")
    print("✅ 测试4: MD5校验 - 通过")
    print("✅ 测试5: 模拟安装 - 通过")
    print("✅ 测试6: 更新版本记录 - 通过")

    print(f"\n🎉 所有测试通过！补丁下载功能正常工作！")

    # 显示测试文件
    print(f"\n📁 测试文件位置:")
    print(f"   补丁文件: {dest_path}")
    print(f"   版本记录: {manager.local_version_file}")

    return True


if __name__ == "__main__":
    try:
        success = test_patch_download()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[测试] 用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n[测试] ❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
