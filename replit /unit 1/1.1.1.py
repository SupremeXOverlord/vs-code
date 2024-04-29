import turtle as trtl;


painter = trtl.Turtle()
painter.pensize(10)

#square
painter.goto(90,0)
painter.goto(90,90)
painter.goto(0,90)
painter.goto(0,0)

#triangle
painter.penup()
painter.goto(90,90)
painter.pendown()
painter.goto(45,125)
painter.goto(0,90)

#guy
painter.penup()
painter.goto(-50,45)
painter.pendown()
painter.circle(20)
painter.goto(-50,45)
painter.goto(-50,-10)
painter.goto(-60,-30)
painter.goto(-50,-10)
painter.goto(-40,-30)






wn = trtl.Screen()
wn.mainloop()
