# pi_pir_webthing
A web connected PIR motion sensor on Raspberry Pi

This project provides a [webthing API](https://iot.mozilla.org/wot/) to a PIR motion sensor such as [descriped here](https://cdn-learn.adafruit.com/downloads/pdf/pir-passive-infrared-proximity-motion-sensor.pdf).  

The pi_pir_webthing package exposes an http webthing endpoint which supports detecting motion via http. E.g. 
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:9544/properties 

{
   "motion": true,
   "last_motion": "2020-09-28T08:04:02.330388"
}
```

The RaspberryPi/PIR sensor hardware setup and wiring may look like [HC SR501 example](https://github.com/grro/pi_pir_webthing/blob/master/docs/layout.png). 

To install the software you may use Docker or [PIP](https://realpython.com/what-is-pip/) package manager such as shown below
** Docker approach**
```
sudo docker run --privileged -p 9544:9544 -e gpio=14 grro/pi_pir_webthing:0.1.0
```

** PIP approach**
```
sudo pip install pi_pir_webthing
```


After this installation you may start the webthing http endpoint inside your python code or via command line using 
```
sudo pir --command listen --port 9544 --gpio 14
```
Here, the webthing API will be bind on port 9544 and be connected to the PIR pin using gpio 14

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit. 
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary. 
```
sudo pir --command register --port 9544 --gpio 14
```  
