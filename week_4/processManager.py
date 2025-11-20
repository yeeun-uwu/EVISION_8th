import psutil


print(f"[+] Starting Process Manager...\n")
print(f"{'PID':<8}    {'Name':<30}    {'Memory(MB)':>10}    {'Path'}")
print("="*80)
for proc in psutil.process_iter(attrs = ['pid', 'name', 'memory_info', 'exe']):
    try:
        info = proc.info
        pid = info['pid']
        name = info['name']
        memory = info['memory_info'].rss / (1024 * 1024)  # Convert to MB
        path = info['exe'] if info['exe'] else ""
        if len(name) > 28:
            name = name[:25] + '...'

        print(f"{pid:<8}    {name:<30}    {memory:>10.2f}    {path}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess
    ):
        pass    