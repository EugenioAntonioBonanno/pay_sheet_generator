from objects import Session, Day
# code length time

# name sessions

w57 = Session("W57", "1 hour", "4:25")
w75 = Session('W75', "1 hour", "5:20")
w48 = Session('W48', '1 hour', '6:40')
w45 = Session('W45', '1 hour', '7:35')
ext = Session("Homework period", '.5 hour', "900")
ext = Session("Homework period", '.5 hour', "900")


w60 = Session('W60', '1 hour', '1:50')
w61 = Session('W61', '1 hour', '2:45')
pe = Session('PE', '.5 hour', "901")
w71 = Session('W71', '1 hour', '4:25')
w66 = Session('w66', '1 hour', '5 20')
w49 = Session('W49', '2 hours', '6:40')
ext = Session("Homework period", '.5 hour', "900")
ext = Session("Homework period", '.5 hour', "900")

f70 = Session('F70', '2 hours', '1:45')
w67 = Session('W67', '1 hour', '4:25')
w52 = Session('W52', '1 hour', '5:20')
w46 = Session('w46', '1 hour', '7:35')
ext = Session("Homework period", '.5 hour', "900")
ext = Session("Homework period", '.5 hour', "900")



ext = Session("Homework period", '.5 hour', "900")

mon = [w57, w75, w48, w45, ext, ext]

wed = [pe, w60, w61, pe, w71, w66, w49, ext, ext]

fri = [f70, w67, w52, w46, w49, ext, ext]

monday = Day("Monday", mon)

