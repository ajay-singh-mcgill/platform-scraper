from crontab import CronTab

cron = CronTab(user='crawler')
cron.remove_all()

job = cron.new(command='python3 /home/crawler/appexchange/crawing/spider.py')
job.every(12).hours()
for entry in cron:
    print(entry)
cron.write()
