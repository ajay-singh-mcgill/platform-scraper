from crontab import CronTab

cron = CronTab(user='crawler')
cron.remove_all()

#job = cron.new(command='python3 /home/crawler/appexchange/cron_test.py')
#job.minute.every(1)
#for entry in cron:
#    print(entry)
cron.write()
