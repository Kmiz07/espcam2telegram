# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import gc,machine
print(gc.mem_free())
import wifi
print(gc.mem_free())
print("se reinicio por %s" % (machine.reset_cause()))
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Alarma por (%s)' % str(machine.wake_reason()))
wifi.main()
