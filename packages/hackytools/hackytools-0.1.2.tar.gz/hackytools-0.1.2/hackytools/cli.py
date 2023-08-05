import os
import argparse
import sys
import platform
import subprocess
import regex as re




def frequency():
    path = f"/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    if os.path.exists(path):
        print(f"\x1b[4mCPU Freqs (0-{os.cpu_count()-1})\x1b[0m")
    for i in range(os.cpu_count()):
        path = f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq"
        if os.path.exists(path):
            with open(path) as f:
                data = int(f.read()) / 1000000
            print(f"  CPU {i}: {data:.2f} GHz")

def temperature():
    path = "/sys/class/thermal/thermal_zone/temp"
    if os.path.exists(path):
        with open(path) as f:
            data = int(f.read()) / 1000
        print(f"\x1b[4mTemperature\x1b[0m\n  {data:.1f}\u00b0C | {data * 9 / 5 + 32:.1f}\u00b0F")

    else:
        process = subprocess.run('sensors nvme-pci-0100 amdgpu-pci-0400', capture_output=True, shell=True)
        return_code = process.returncode

        if process.returncode != 0:
            return

        output = process.stdout.decode()
        
        cpu_pattern = re.compile(r'(?<=Composite: +\+)\d+\.\d+')
        gpu_pattern = re.compile(r'(?<=edge: +\+)\d+\.\d+')


        ctc = float(cpu_pattern.search(output).group())
        gtc = float(gpu_pattern.search(output).group())
        ctf = ctc * 9 / 5 + 32
        gtf = gtc * 9 / 5 + 32

        cpu_temp = f"{ctc}\u00b0C | {ctf}\u00b0F"
        gpu_temp = f"{gtc}\u00b0C | {gtf}\u00b0F"


        print(f"\x1b[4mCPU Temp\x1b[0m\n  {cpu_temp}\n\x1b[4mGPU Temp\x1b[0m\n  {gpu_temp}")

def hackystats(args):

    sys.stdout.write(f"\x1b[4m{platform.platform()}\x1b[0m\n\n")
    frequency()
    temperature()

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=hackystats)
    args = parser.parse_args(argv)
    if os.name == 'nt':
        sys.exit("This command only works on linux.")
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
