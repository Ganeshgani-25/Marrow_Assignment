import psutil # type: ignore
import argparse
import time
import csv
import json
import os

# Function for getting system data
def get_system_performance():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = {
        "total" : memory.total,
        "used" : memory.used,
        "free" : memory.free,
        "percent" : memory.percent
    }

    # Loops through each mounted filesystem and collecting disk usage data
    disk_usage = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage.append({
            "mountpoint" : partition.mountpoint,
            "total" : usage.total,
            "used" : usage.used,
            "free" : usage.free,
            "percent" : usage.percent
        })

    # For retrieving and sorting 5 top CPU_consuming processes
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]

    top_processes = [
        {'pid': proc.info['pid'], "name": proc.info['name'],"cpu_percent":proc.info['cpu_percent']}
        for proc in processes
    ]

    return {
        "cpu_usage": cpu_usage, "memory_usage" : memory_usage, "disk_usage": disk_usage, "top_processes": top_processes
    }

# function to write report to a file
def write_report(data, file_format, file_name):
    if file_format == "text":
        with open(file_name, "w") as file:
            file.write(f"CPU usage: {data['cpu_usage']}%\n")
            file.write("Memory_usage:\n")
            file.write(f" total: {data['memory_usage']['total']/(1024**3):.2f}GB\n")
            file.write(f" used: {data['memory_usage']['used']/(1024**3):.2f}GB\n")
            file.write(f" free: {data['memory_usage']['free']/(1024**3):.2f}GB\n")
            file.write(f" percent: {data['memory_usage']['percent']}%\n")
            file.write("Disk_usage:\n")
            for disk in data['disk_usage']:
                file.write(f" {disk['mountpoint']}: {disk['percent']}%used\n")
            file.write("Top 5 CPU_consuming processes:\n")
            for process in data['top_processes']:
                file.write(f" PID{process['pid']} - {process['name']}: {process['cpu_percent']}%\n")
    # if file format is JSON
    elif file_format == "json":
        with open(file_name, "w")as file:
            json.dump(data, file, indent=4)
    # if file format is CSV
    elif file_format == "csv":
        with open(file_name, "w", newline='')as file:
            writer = csv.writer(file)
            writer.writerow(["CPU Usage", data['cpu_usage']])
            writer.writerow([])
            writer.writerow(["Memory usage"])
            writer.writerow(["total", "used", "free", "percent"])
            writer.writerow([data['memory_usage']['total'], data['memory_usage']['used'], data['memory_usage']['free'], data['memory_usage']['percent']])

            writer.writerow([])
            writer.writerow(["Disk usage"])
            writer.writerow(["mountpoint", "total", "used", "free", "percent"])
            for disk in data['disk_usage']:
                writer.writerow([
                    disk['mountpoint'],
                    disk['total'],
                    disk['used'],
                    disk['free'],
                    disk['percent']
                ])
            writer.writerow([])
            writer.writerow(["Top 5 CPU_consuming processes"])
            writer.writerow(["PID", "Name", "CPU percent"])
            for process in data['top_processes']:
                writer.writerow([process['pid'], process['name'], process['cpu_percent']])   

def main():
    parser = argparse.ArgumentParser(description = "Monitor System performance and generate a report")
    parser.add_argument("--interval", type=int, default=5, help="Monitoring intervals in seconds")
    parser.add_argument("--format", choices=["text", "json", "csv"], default="text", help = "Output file format")
    parser.add_argument("--output", default = "system_report", help="output file name without extension")
    args = parser.parse_args()

    while True:
        try:
            data = get_system_performance()
            if data['cpu_usage'] > 80:
                print("Warning: High CPU usage is detected..")
            if data['memory_usage']['percent'] > 75:
                print("Warning: High memory usage is detected..")
            for disk in data['disk_usage']:
                if disk['percent'] > 90:
                    print(f"Warning: High disk usage is detected on {disk['mountpoint']}!")

            file_name = f"{args.output}.{args.format}"
            write_report(data, args.format, file_name)

            print(f"Report generated at: {file_name}")
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Monitoring stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
            

    
    


