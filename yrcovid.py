import csv
import requests
import operator
import datetime
import matplotlib.pyplot as plt

mun = 0
munArr = ["", "Aurora", "East Gwillimbury", "Georgina", "King", "Markham", "Newmarket", "Richmond Hill", "Vaughan", "Whitchurch-Stouffville"]

def intro():
    print("COVID-19 Case Counter (York Region)")
    print("v0.0.2 (06/11/2021) - Owen Bowden (the404)")
    print("------------------------------------------")
    print("Select municipality to show data for:")
    print("[1]: Aurora")
    print("[2]: East Gwillimbury")
    print("[3]: Georgina")
    print("[4]: King")
    print("[5]: Markham")
    print("[6]: Newmarket")
    print("[7]: Richmond Hill")
    print("[8]: Vaughan")
    print("[9]: Whitchurch-Stouffville")
    print("[0]: York Region")

def getInput():
    try: 
        global mun
        mun = int(input("Enter selection: "))
        if(mun >= 0 and mun <= 9):
            return
        else: 
            print("Out of range!")
            getInput()
    except: 
        print("Not a number!")
        getInput()

intro()
getInput()

print("Getting raw case data...")
url = "https://ww4.yorkmaps.ca/COVID19/Data/YR_CaseData.csv"
raw = requests.get(url)
with open('raw.csv', 'wb') as f:
    f.write(raw.content)

raw = open('raw.csv','r')
dateAdjusted = open('temp.csv', 'w')
reader = csv.reader(raw,delimiter=',')
writer = csv.writer(dateAdjusted,delimiter=',')

print("Adjusting date formats...")
for row in reader:
    try:
        date = datetime.datetime.strptime(row[5], '%m/%d/%Y')
        row[5] = date.isoformat().split("T", 1)[0]
    except:
        continue
    writer.writerow(row)

dateAdjusted = open('temp.csv', 'r')
reader = csv.reader(dateAdjusted,delimiter=',')

print("Sorting...")
sortedlist = sorted(reader, key=operator.itemgetter(5))

data = [[],[]]
i = -1;
for row in sortedlist:
    if munArr[mun] in row[3]:
        if row[5] not in data[0]:
            data[0].append(row[5])
            i += 1;
            data[1].append(0)
        data[1][i] += 1

filledData = [[],[]]

date = datetime.datetime.strptime("2020-02-29", "%Y-%m-%d").date()
for i in range(len(data[0])):
    currentDate = datetime.datetime.strptime(data[0][i], "%Y-%m-%d").date()
    while (date != currentDate):
        filledData[0].append(date.isoformat().split("T", 1)[0])
        filledData[1].append(0)
        date += datetime.timedelta(days=1)
    filledData[0].append(data[0][i])
    filledData[1].append(data[1][i])
    date += datetime.timedelta(days=1)


finalDate = datetime.datetime.strptime((filledData[0][len(filledData[0]) - 1]), "%Y-%m-%d")
today = datetime.date.today()

while(finalDate.date() != today):
    print(str(finalDate.date()) + " " + str(today))
    finalDate += datetime.timedelta(days=1)
    filledData[0].append(finalDate.isoformat().split("T", 1)[0])
    filledData[1].append(0)


for i in range(len(filledData[0])):
    print(str(filledData[0][i]) + ": " + str(filledData[1][i]))

print("Creating graph...")
left = range(len(filledData[0]))
plt.bar(left, filledData[1], tick_label = filledData[0], width = 0.6, color = ['purple'])
plt.tight_layout()
plt.xticks(rotation = 90)
plt.xlabel('Date')
plt.ylabel('Number of daily new cases')
if(munArr[mun]==""):
    plt.title('COVID-19 Case Data for York Region')
else:
    plt.title('COVID-19 Case Data for ' + munArr[mun])
plt.locator_params(axis='x', nbins=80)
#plt.locator_params(axis='y', nbins=max(filledData[1]))

plt.locator_params(axis='y', nbins=30)
ax = plt.gca()
plt.margins(0)
plt.grid(zorder=3)
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()
