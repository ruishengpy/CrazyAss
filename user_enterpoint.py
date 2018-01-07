import getpass,os,subprocess
import time,hashlib

from django.contrib.auth import authenticate
import sys
class UserPortal(object):
    '''用户命令行端交互入口'''


    def __init__(self):
        self.user = None
    def user_auth(self):
        '''完成用户交互'''
        retry_count=0
        while retry_count<3:
            username=input('username:').strip()
            if len(username)==0:continue
            password=getpass.getpass('password:').strip()
            if len(password)==0:
                print('Password can not  be null.')
                continue
            user=authenticate(username=username,password=password)
            if user and password:
                self.user=user
                # print('welcome login ......')
                return
            else:
                print('invalid username  or password.')
            retry_count+=1
        else:
            print('too many attempts')

    def interactive(self):
        '''交互函数'''
        self.user_auth()
        exit_flag=False
        if self.user:
            exit_flag = False
            while not exit_flag:
                # print(self.user.bind_hosts.select_related())
                # print(self.user.host_groups.select_related())
                for index,host_group in enumerate(self.user.host_groups.all()):
                    print('%s. %s[%s]' %(index,host_group.name,host_group.bind_hosts.all().count()))
                print('%s Ungrouped:[%s]'% (index+1,self.user.bind_hosts.select_related().count()))
                user_input=input('choose Group:').strip()
                if len(user_input)==0:continue
                if user_input=='q':break
                if user_input.isdigit():
                    user_input=int(user_input)
                    if user_input >=0 and user_input< self.user.host_groups.all().count():
                        select_group=self.user.host_groups.all()[user_input]
                    elif user_input == self.user.host_groups.all().count():
                        select_group=self.user
                    else:
                        print('invalid group')
                        continue
                    while True:
                        for index,bind_host in enumerate(select_group.bind_hosts.all()):
                            print('%s.  %s' %(index,bind_host))
                        user_input2=input('please input host number:').strip()
                        if len(user_input2) == 0: continue
                        if user_input2.isdigit():
                            user_input2 = int(user_input2)
                            if user_input2 >= 0 and user_input2 < select_group.bind_hosts.all().count():
                                select_bindhost=select_group.bind_hosts.all()[user_input2]
                                print('loging host',select_bindhost)
                                md5_str=hashlib.md5(str(time.time()).encode()).hexdigest()

                                login_cmd='sshpass -p "{password}" ssh {username}@{ip_addr} -o "StrictHostKeyChecking=no" -Z {md5_str}'.format(password=select_bindhost.host_user.password,username=select_bindhost.host_user.username,ip_addr=select_bindhost.host.
ip_addr,md5_str=md5_str)
                                print(login_cmd)
                                time.sleep(5)
                                #start session log
                                reault=models.SessionLog.objects.create(user=self.user,host_user=select_bindhost,session_tag=md5_str)
                                print(reault)
                                #start session tracker script
                                session_tracker_script=settings.SESSION_TRACKER_SCRIPT
                                tracker_obj=subprocess.Popen('%s %s' %(session_tracker_script,md5_str),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=settings.BASE_DIR)
                                ssh_instance=subprocess.call(login_cmd,shell=True)
                                print('''''''''''logout''''''''''''''''''''''''''''''''')
                                # print('tracker session output:',tracker_obj.stdout.read().decode(),tracker_obj.stderr.read().decode())

                        if user_input2=="b":
                            break
                        if user_input2=="q":
                            exit_flag=True
                            break


            if exit_flag:sys.exit()


if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyAss.settings")
    import django
    django.setup()
    from django.conf import settings
    from audit import models
    portal=UserPortal()
    portal.interactive()
