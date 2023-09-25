import os

N = 4
root = f'imgs/try_{N}/'
second = f'try_{N}_origin'
files = os.listdir(root+second)

for file in files:
    src = os.path.join(root, second, file)
    dst = os.path.join(root, second, f'try_{N}_'+file)
    os.rename(src, dst)

print(os.listdir(root+second))