#this uses Environment Agency flood and river level data from the real-time data API (Beta)
from module import flooding,selector


if __name__ == "__main__":
    s = selector()
    print(s.station)
    a = flooding(s.station)
    a.table(open=True)
    a.plot()
