class Order:
    def __init__(self,orderid,bikeid,userid,start_time,start_location_x,start_location_y,end_time,end_location_x,end_location_y,track):
        self.orderid=orderid
        self.bikeid=bikeid
        self.userid=userid
        self.start_time=start_time
        self.start_location_x=start_location_x
        self.start_location_y=start_location_y
        self.end_time=end_time
        self.end_location_x=end_location_x
        self.end_location_y=end_location_y
        self.track=track