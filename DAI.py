import time, random, requests
import atexit
import threading
import DAN

import UWB

ServerURL = 'https://5.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Position_Device'
DAN.profile['df_list']=['Position_Sensor']
DAN.profile['d_name']= 'Dummy_Titi1'

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

car1_uwb = UWB.UWB()

# It will call this function when the code is shutdowned
def end():
    print("Stop")
    car1_uwb.end()
atexit.register(end)

t = threading.Thread(target=car1_uwb.distance)
t.start()

while True:
    try:
        time.sleep(1)
        rX, rY = car1_uwb.triposition()
        rX, rY = [round(float(rX), 3), round(float(rY), 3)]
        print(rX, rY)
        IDF_data = [rX, rY]
        DAN.push ('Position_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================

        # ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        # if ODF_data != None:
        #     print (ODF_data[0])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

