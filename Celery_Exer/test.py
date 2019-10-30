# coding=utf-8


from tasks import send_email, add

print("my other codes are here.")
send_email.delay(dict(to='celery@python.org'))
 
result = add.delay(10, 25)

print(result.status)
# he ready() method returns whether the task has finished processing or not:
print(result.ready())

result.get()

print(result.ready())

# You can wait for the result to complete, 
# but this is rarely used since it turns the asynchronous call into a synchronous one:
# result.get(timeout=3)




# import time
# from tasks import send_email, add

# print(send_email.delay(dict(to='celery@python.org')))
# answer = send_email.delay(dict(to='windard@windard.com'))

# while 1:
#     print('wait for ready')
#     if answer.ready():
#         break
#     time.sleep(0.5)
# print(answer.get())