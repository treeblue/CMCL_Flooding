#this uses Environment Agency flood and river level data from the real-time data API (Beta)
from module import flooding

# "1029TH"
# "720763"

if __name__ == "__main__":
    ID = input("Input Station ID:")
    a = flooding(ID)
    a.table(open=True)
    a.plot()
