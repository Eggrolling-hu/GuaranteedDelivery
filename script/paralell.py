import multiprocessing
import subprocess

# 这是一个简单的函数，它在一个子进程中执行一个命令


def run_command(cmd, cwd):
    _ = subprocess.run(cmd, shell=True, cwd=cwd)
    return "success"


if __name__ == "__main__":
    # 创建一个进程池
    pool = multiprocessing.Pool(6)

    # 定义开始的列表
    # 定义工作目录
    cwd = "D:\\code\\demo\\smp\\GuaranteedDelivery\\script"

    for i in range(7380, 11587):
        cmd = f"python ./extract_table.py {i} {i+1}"
        pool.apply_async(run_command, args=(cmd, cwd))

    pool.close()
    pool.join()
