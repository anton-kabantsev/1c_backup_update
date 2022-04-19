import win32com.client
CONN_STRING = r'File="C:\Users\Антон\Documents\1C\DemoAccounting";Usr="АбрамовГС (директор)";'
com = win32com.client.Dispatch("V83.ComConnector")
buh = com.connect(CONN_STRING)
system = buh.NewObject("SystemInfo")
print(buh.Метаданные.Синоним)
print(buh.Метаданные.Версия)
print(system.ВерсияПриложения)
