import time

from datagram_modules import MPDU, Datagrama, ControlSistema

control = ControlSistema()

control.stop()
time.sleep(5)
control.delete()
control.delete("sector:Envasado")
control.delete("sector:Empaque")
control.delete("sector:Limpieza")

print("Sistema finalizado.")