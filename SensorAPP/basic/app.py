import time
import board
import adafruit_dht


sensor = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperature_c = sensor.temperature
        #temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        print("Sıcaklık={0:0.1f}ºC, Nem={1:0.1f}%".format(temperature_c, humidity))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(1.0)
