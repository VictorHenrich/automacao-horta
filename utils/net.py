import network
import time
from core import config


class Network:
    __WLAN_INSTANCE = None

    @classmethod
    def check_wifi_connection(cls):
        if cls.__WLAN_INSTANCE is None:
            return False

        else:
            return cls.__WLAN_INSTANCE.isconnected()

    @classmethod
    def connect_to_wifi(
        cls,
        network_name=config.WIFI_NAME,
        network_password=config.WIFI_PASSWORD,
        wait=5,
        is_new=False,
    ):
        if cls.__WLAN_INSTANCE is None or is_new is False:
            wlan = network.WLAN(network.STA_IF)

            wlan.active(True)

            if not wlan.isconnected():
                wlan.connect(network_name, network_password)

                for _ in range(wait):
                    if wlan.isconnected():
                        break

                    time.sleep(1)

            if wlan.isconnected():
                cls.__WLAN_INSTANCE = wlan

                print("Wifi conectado com sucesso!")

            else:
                wlan.active(False)

                raise Exception(f"Falha ao se conectar na rede Wifi")

        return cls.__WLAN_INSTANCE
