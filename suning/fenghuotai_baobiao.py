import random
import string
# seed = '1234567890!@#$%^&*(abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+=-?><L}'
seed = '1234567890!@#$%^&*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ}'
sa = []
for i in range(16):
    sa.append(random.choice(seed))
salt = ''.join(sa)
print(salt)
