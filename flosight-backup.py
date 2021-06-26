import subprocess
import sys
import datetime
import os, pdb, time
from stat import S_ISREG, ST_CTIME, ST_MODE
from pathlib import Path


current_time = datetime.datetime.now()
backup_directory = f"{os.getcwd()}/backups/flosight/"
container_id = "e960eb376abd"

def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), destination)

os.chdir(os.getcwd())
# Get list of all files only in the given directory
list_of_files = filter( lambda x: os.path.isfile(os.path.join(backup_directory, x)),os.listdir(backup_directory))

# Sort list of files based on last modification time in ascending order
list_of_files = sorted( list_of_files, key = lambda x: os.path.getmtime(os.path.join(backup_directory, x)))
print(f"List of files is :\n{list_of_files}")

#result = subprocess.run([sys.executable, "-c", f"sudo docker cp c640f68b91be:/data/ /home/production/deployed/automated-backup-scripts/backups/flosight/flosight-backup-{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute}-{current_time.second}"], capture_output=True, text=True)
folder_name = f"{os.getcwd()}/backups/flosight/flosight-backup-{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute}-{current_time.second}"
result = subprocess.check_output(f"sudo docker cp {container_id}:/data/ {folder_name}", stderr=subprocess.STDOUT, shell=True)
#print("stdout:", result.stdout)
#print("stderr:", result.stderr)
make_archive(folder_name, f"{folder_name}.zip")
shutil.rmtree(folder_name)

if len(list_of_files) >= 3:
    os.remove(f"{os.getcwd()}/backups/flosight/{list_of_files[0]}")
