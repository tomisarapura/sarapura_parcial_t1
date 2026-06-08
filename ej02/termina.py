import time

from datagram_modules import MPDU, Datagrama, ControlSistema

control = ControlSistema()

control.stop()
time.sleep(5)
control.delete()

print("Sistema finalizado.")