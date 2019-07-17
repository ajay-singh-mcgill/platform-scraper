from crontab import CronTab

cron = CronTab(user='crawler')
cron.remove_all()

job = cron.new(command='python3 /home/crawler/appexchange/crawing/spider.py')
job.setall('0 6 * * *')

job2 = cron.new(command='python3 /home/crawler/appexchange/crawing/spider_microsoft.py')
job2.setall('0 12 * * *')

for entry in cron:
    print(entry)
cron.write()
