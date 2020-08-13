import getpass
import os
from subprocess import Popen, PIPE, STDOUT
class windows_connect:
    def __init__(self):
        self.username=input("Input your username (just the username like adam01) :")
        self.password = getpass.getpass('Enter password for '+self.username)

    def unmount_drive(self,target_dir):
        cmd1=['sudo umount '+target_dir]
        um = Popen(cmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, stderr = um.communicate()
        if not bool(um.returncode):
            print("Unmounted "+target_dir)
            return(True)
        else:
            print("Could not unmount")
            print(stderr)
            return(False)


    def create_dir(self,target_dir):
        cmd2=['mkdir -p ' + target_dir]
        cr = Popen(cmd2, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, stderr = cr.communicate()
        if not bool(cr.returncode):
            print("Created "+target_dir)
            return(True)
        else:
            print("Something went wrong")
            print(stderr)
            return(False)

    def mount_drive(self,source_dir,target_dir):
        dir_struct=source_dir.split('/')
        print("Windows drive "+str(source_dir)+" will be mounted as "+target_dir)
        print("This might sometimes take upto 5 mins")
        cmd = ['sudo mount -t cifs -o cruid=labuser,gid=2100,uid=2100,domain=changehere,username='+self.username+' '+source_dir+' '+target_dir]
        mn = Popen(cmd, shell=True , stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, stderr = mn.communicate(input=self.password.encode())
        if not bool(mn.returncode):
            print(source_dir+"is now mapped at "+target_dir)
            print(mn.stdout)
            return(True)
        else:
            print('Something went wrong')
            print(mn.stderr)
            return(False)

    def map_drive(self,drive_location):
        for loc in drive_location.split(','):
            loc1=loc.rstrip('/')
            dir_struct=loc.split('/')
            source_dir='"'+loc1+'"'
            target_dir='"/home/labuser/workspace/windows_drive/'+dir_struct[2]+"_"+dir_struct[-1]+'"'
            self.unmount_drive(target_dir)
            self.create_dir(target_dir)
            self.mount_drive(source_dir,target_dir)
