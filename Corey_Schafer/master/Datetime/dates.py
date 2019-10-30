import datetime
import pytz

# Naive
# datetime.datetime.now()
now = datetime.datetime.now()
print("datetime.datetime.now(): ", now)
print("type(now): ", type(now))

# String strftime()
print("datetime.datetime.now().strftime(): ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# datetime.datetime()
myDateTime = datetime.datetime(2015, 1, 12, 23, 9, 12, 946118)
print("myDateTime: ", myDateTime)

# datetime.datetime.now().date()
date1 = datetime.datetime.now().date()
print("datetime.datetime.now().date(): ", date1)

# datetime.date(2001,9 ,11)
d = datetime.date(2001, 9, 11)
print("datetime.date(2001, 9, 11): ", d)
print("type(d): ", type(d))

# datetime.date.today()
tday = datetime.date.today()
print("datetime.date.today(): ", tday)

# weekday() - Monday is 0 and Sunday is 6
print("tday.weekday(): ", tday.weekday())

# isoweekday() - Monday is 1 and Sunday is 7
print("tday.isoweekday(): ", tday.isoweekday())


# datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

tdelta = datetime.timedelta(days=1, hours=12)
print("tday + tdelta: ", tday + tdelta)

# date2 = date1 + timedelta
# timedelta = date1 + date2

bday = datetime.date(2018, 12, 31)

till_bday = bday - tday
print("till_bday = bday - tday: ", till_bday.days)

t = datetime.time(9, 30, 45, 100000)

# dt = datetime.datetime.today()
# dtnow = datetime.datetime.now()
# print(dir(datetime.datetime))
# print(dt)
# print(dtnow)

dt = datetime.datetime(2016, 7, 24, 12, 30, 45, tzinfo=pytz.UTC)
# print(dir(dt))

dt_utcnow = datetime.datetime.now(tz=pytz.UTC)
# print(dt_utcnow)

dt_utcnow2 = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
# print(dt_utcnow2)

# dt_mtn = dt_utcnow.astimezone(pytz.timezone('US/Mountain'))
# print(dt_mtn)

dt_mtn = datetime.datetime.now()

mtn_tz = pytz.timezone('US/Mountain')
dt_mtn = mtn_tz.localize(dt_mtn)

# print(dt_mtn)

dt_east = dt_mtn.astimezone(pytz.timezone('US/Eastern'))
# print(dt_east)

print(dt_mtn.strftime('%B %d, %Y'))

dt_str = 'July 24, 2016'
dt = datetime.datetime.strptime(dt_str, '%B %d, %Y')
print(dt)

# strftime - Datetime to String
# strptime - String to Datetime
