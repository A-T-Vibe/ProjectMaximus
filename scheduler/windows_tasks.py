"""
Register ProjectMaximus posting jobs with Windows Task Scheduler.
Run once as Administrator: python scheduler/windows_tasks.py
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = sys.executable
MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")

POST_TIMES = ["08:00", "16:00", "18:00"]
STATS_TIME = "09:00"


def register_task(name, time_str, args):
    cmd = [
        "schtasks", "/create",
        "/tn", name,
        "/tr", f'"{PYTHON_EXE}" "{MAIN_SCRIPT}" {args}',
        "/sc", "DAILY",
        "/st", time_str,
        "/f",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Registered: {name} at {time_str}")
    else:
        print(f"Failed to register {name}: {result.stderr}")


def register_all():
    for i, t in enumerate(POST_TIMES):
        register_task(
            name=f"ProjectMaximus_Post_{t.replace(':', '')}",
            time_str=t,
            args="--post",
        )

    register_task(
        name="ProjectMaximus_Stats",
        time_str=STATS_TIME,
        args="--collect-stats",
    )

    print("\nAll tasks registered. View them in Windows Task Scheduler.")
    print("To remove all tasks: python scheduler/windows_tasks.py --remove")


def remove_all():
    names = [f"ProjectMaximus_Post_{t.replace(':', '')}" for t in POST_TIMES]
    names.append("ProjectMaximus_Stats")
    for name in names:
        result = subprocess.run(["schtasks", "/delete", "/tn", name, "/f"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Removed: {name}")
        else:
            print(f"Could not remove {name} (may not exist)")


if __name__ == "__main__":
    if "--remove" in sys.argv:
        remove_all()
    else:
        register_all()
