import datetime
from crontab import CronTab

my_crons = CronTab(user=True)
for job in my_crons:
    sch = job.schedule(date_from=datetime.datetime.now())
    print(sch.get_next())
