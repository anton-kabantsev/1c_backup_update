import win32com.client
CONN_STRING = r'File="C:\Users\Антон\Documents\1C\DemoAccounting";Usr="АбрамовГС (директор)";'
buh = win32com.client.Dispatch("V83.ComConnector")
buh.connect(CONN_STRING)
SystemInfo = buh.NewObject("Query", ' ')
print(SystemInfo.AppVersion)
# trade = cntr.Connect («File=""c:\InfoBases\Trade»»; Usr=""Director»»;»)     'Получить внешнее соединение
# trade_goods = trade.Справочники.Товары
# trade_goods = СправочникТоваров.СоздатьГруппу()