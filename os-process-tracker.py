import os
import smtplib
import psutil
import time
import keyboard
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('USER_EMAIL')
EMAIL_PASSWORD = os.environ.get('USER_PASS')

msg = EmailMessage()
msg['Subject'] = 'System process tracker'
msg['From'] = EMAIL_ADDRESS
msg['To'] = input("Enter your email id:")
interval=int(input("After how many minutes would you like to receive email notifications?:"))
print("To stop the program give the keyboard interrupt (Ctrl+C)!!!")
names_before,names_after,pids_before,pids_after=[],[],[],[]
process_dict_before,process_dict_after={},{}
for proc in psutil.process_iter():
    try:
        processName = proc.name()
        processID = proc.pid
        names_before.append(processName)
        pids_before.append(processID)       
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
process_dict_before=dict(zip(pids_before,names_before))
set_pids_before=set(pids_before)
#later stages
while True:
    try:
        time.sleep(interval*60)
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                processID = proc.pid
                names_after.append(processName)
                pids_after.append(processID)      
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        process_dict_after=dict(zip(pids_after,names_after))
        set_pids_after=set(pids_after)
        result_set=set_pids_before-set_pids_after
        if len(result_set)!=0:
            string="Processes that ended:\nPID\tProcess name"
            for pid in result_set:
                string=string+"\n"+str(pid)+"\t"+process_dict_before[pid]
            msg.set_content(string)
        else:
            string="No process have stopped in the last "+str(interval)+" minutes!"
            msg.set_content(string)

        names_before=names_after
        pids_before=pids_after
        process_dict_before=process_dict_after

        names_after=[]
        pids_after=[]
        process_dict_after={}
        set_pids_before=set_pids_after.copy()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("You have a new email!")
    except KeyboardInterrupt:
        break
