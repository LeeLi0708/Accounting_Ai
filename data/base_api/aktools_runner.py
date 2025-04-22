import subprocess
import sys

def run_aktools():
    """
    启动 python -m aktools 并在后台运行（不阻塞主程序）
    """
    try:
        # 在新控制台窗口中启动 aktools（Windows）
        process = subprocess.Popen(
            [sys.executable, "-m", "aktools"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return process
    except Exception as e:
        print(f"启动 aktools 失败: {e}")
        return None

# if __name__ == "__main__":
#     # 启动 aktools
#     aktools_process = run_aktools()