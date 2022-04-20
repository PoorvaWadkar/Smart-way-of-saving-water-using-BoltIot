import conf, json , time 
from boltiot import Sms, Bolt

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

while True:
    print("Reading a sensor value...")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    if data["success"] !=1:
            print("There was an error while retriving the data.")
            print("This is the error : " +data['value'])
            time.sleep(10)
            continue
    print("Sensor value is " + str(data['value']))
    
    try:
        sensor_value = int(data['value'])
    except Exception as e:
        print("There was an error while parsing the response :" ,e)
        continue
    
    try:
        if sensor_value  > conf.threshold:
            print("Making request to Twilio to send SMS...")
            response = sms.send_sms("Water tank is about to overflow. Turn off the water supply immediately.")
            print("Response recieved from Twilio  is: " +str(response))
            response = mybolt.digitalWrite('0','HIGH')
            time.sleep(5)
            response = mybolt.digitalWrite('0','LOW')
            print(response)
	      
    except Exception as e:
        print("Error occurred : Below are the details")
        print(e)
    time.sleep(10)
	    
	
