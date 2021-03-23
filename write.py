import time
for i in range(5):
    seconds = time.time()
    local_time = time.ctime(seconds)
    with open('./txts/test.txt', 'a') as f:
        f.write(local_time + '\n')
        f.write(str(i) + '\n')
