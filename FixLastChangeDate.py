import os
from datetime import datetime

doOne = False

if __name__ == '__main__':
    # Fix the last change date of the data files 
    groupdirs = [int(dir[4:]) for dir in os.listdir(os.getenv('POS_OUTPUT_DIRS')) if dir.startswith('Run_')]
    groupdirs = [groupnumber for groupnumber in groupdirs if groupnumber > 100000]
    groupdirs.sort()
    for groupnumber in groupdirs:
        groupdir_path = os.getenv('POS_OUTPUT_DIRS')+'/Run_'+str(groupnumber)
        rundirs = [int(dir[4:]) for dir in os.listdir(groupdir_path) if dir.startswith('Run_')]
        rundirs.sort()
        # Iterate on folders in run order (which must also be time order)
        for run in rundirs:
            print 'Edit run '+str(run)
            dir_path = groupdir_path+'/Run_'+str(run)
            status_fed_files = [dir for dir in os.listdir(dir_path) if dir.startswith('StatusFED')]
            if len(status_fed_files) == 0:
                print 'No status FED file found for run '+str(run)
            new_date = datetime(2022,1,1,0,0,0)
            with open(dir_path+'/'+status_fed_files[0]) as f:
                for line in f.readlines():
                    if line.startswith('Time'):
                        time_str = line.split()[2:6]
                        new_date = datetime.strptime(' '.join(time_str),'%b %d %H:%M:%S %Y')
                        break
            if new_date == datetime(2022,1,1,0,0,0):
                print 'Issue in finding date for run '+str(run)
                continue
            os.system('touch -t ' + new_date.strftime('%Y%m%d%H%M.%S')+ ' ' + dir_path+'/*')
            print 'New mtime is: '+datetime.fromtimestamp(os.path.getmtime(dir_path+'/PixelConfigurationKey.txt')).strftime('%d/%m/%Y %H:%M:%S')
            if doOne:
                break
        if doOne:
            break
