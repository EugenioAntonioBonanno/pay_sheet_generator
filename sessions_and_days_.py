import pickle
from objects import Session
# code length time


w57 = Session("W57", "1 hour", "4:25")
w75 = Session('W75', "1 hour", "5:20")
w48 = Session('W48', '1 hour', '6:40')
w45 = Session('W45', '1 hour', '7:35')
w60 = Session('W60', '1 hour', '1:50')
w61 = Session('W61', '1 hour', '2:45')
w71 = Session('W71', '1 hour', '4:25')
w66 = Session('w66', '1 hour', '5 20')
w49 = Session('W49', '2 hours', '6:40')
f70 = Session('F70', '2 hours', '1:45')
w67 = Session('W67', '1 hour', '4:25')
w52 = Session('W52', '1 hour', '5:20')
w46 = Session('w46', '1 hour', '7:35')



PE = Session('PE', '.5 hour', "901")
Ext = Session("Homework period", '.5 hour', "900")


print(W57.length)