import pandas

df = pandas.read_csv('barista - Sheet1.csv')
print(df)

for i in df:
    print(i[-1])