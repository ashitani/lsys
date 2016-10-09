#!/usr/bin/env python
# coding: utf-8

'''
 http://aidiary.hatenablog.com/entry/20131125/1385385271
 http://aidiary.hatenablog.com/entry/20131126/1385466122
'''
import re
import math
from random import *
import random
import copy

class turtle_render():
    '''
    render using python standard library "turtle"
    '''
    def __init__(self,txt,stack):
        import turtle
        self.t = turtle
        self.txt = txt
        self.stack = stack

    def push(self):
        self.stack.append(list(self.t.pos())+[self.t.heading()])

    def pop(self):
        if len(self.stack)==0:
            return
        c=self.stack.pop()
        self.t.penup()
        self.t.goto(c[0],c[1])
        self.t.setheading(c[2])
        self.t.pendown()


    def init_screen(self,initial_pos,initial_angle):
        self.t.clear()
        self.t.speed(0)
        self.t.delay(0)
        self.t.hideturtle()
        self.t.penup()
        self.t.goto(initial_pos[0],initial_pos[1])
        self.t.pendown()
        self.t.setheading(initial_angle) # set initial direction to "upward"

    def render(self,
                iteration=5,
                animation=False,
                length=20, angle=90,
                initial_pos=[0,0],
                initial_angle=90,
                random_seed=None,
                display=True):
        import turtle
        self.init_screen(initial_pos,initial_angle)

        random.seed(random_seed)

        if animation==False:
            turtle.tracer(0, 0)
        for c in list(self.txt):
            if c=="F" or c=="A" or c=="B":
                if type(length)==str:
                    self.forward(eval(length))
                else:
                    self.t.forward(length)
            if c=="f" or c=="a" or c=="b":
                self.t.penup()
                if type(length)==str:
                    self.forward(eval(length))
                else:
                    self.t.forward(length)
                self.t.pendown()
            elif c=="+":
                self.t.left(angle)
            elif c=="-":
                self.t.right(angle)
            elif c=="[":
                self.push()
            elif c=="]":
                self.pop()
        if animation==False:
            self.t.update()
        print "Finished render. Push key to exit"
        raw_input()

class jupyter_render():
    '''
    render for jupyter notebook
    using svgwrite
    '''

    def __init__(self,txt,stack, filename="dummy.svg"):
        import svgwrite

        self.sw=svgwrite
        self.txt = txt
        self.stack = stack
        self.filename=filename
        self.svg_txt=""

    def push(self):
        self.stack.append(list(self.pos)+[self.heading])

    def pop(self):
        if len(self.stack)==0:
            return
        c=self.stack.pop()
        self.pos=c[0:2]
        self.heading=c[2]

    def init_screen(self,initial_pos,initial_angle):
        self.size=[400,400]
        self.scale= 2.0/3.0
        self.center=[self.size[0]/2,self.size[1]/2]
        self.dr=self.sw.Drawing(self.filename,self.size)
        self.pos=initial_pos
        self.heading=initial_angle

    def render_pos(self,pos):
        return [self.center[0]+self.scale*pos[0],self.center[1]-self.scale*pos[1]]

    def forward(self,length,draw=True):
        pos0=self.render_pos(self.pos)
        newpos=self.pos
        newpos[0]+= length*math.cos(self.heading/180.0*math.pi)
        newpos[1]+= length*math.sin(self.heading/180.0*math.pi)
        pos1=self.render_pos(newpos)
        if draw:
            self.dr.add(self.dr.line(pos0,pos1, stroke=self.sw.utils.rgb(0,0,0),stroke_width=1))
        self.pos=newpos

    def render(self,
                iteration=5,
                length=20, angle=90,
                initial_pos=[0,0],
                initial_angle=90,
                display=True,
                random_seed=None):
        self.init_screen(initial_pos,initial_angle)

        random.seed(random_seed)

        for c in list(self.txt):
            if c=="F" or c=="A" or c=="B":
                if type(length)==str:
                    self.forward(eval(length))
                else:
                    self.forward(length)
            if c=="f" or c=="a" or c=="b":
                if type(length)==str:
                    self.forward(eval(length),draw=False)
                else:
                    self.forward(length,draw=False)
            elif c=="+":
                if type(angle)==str:
                    self.heading+=eval(angle)
                else:
                    self.heading+=angle
            elif c=="-":
                if type(angle)==str:
                    self.heading-=eval(angle)
                else:
                    self.heading-=angle
            elif c=="[":
                self.push()
            elif c=="]":
                self.pop()

        self.svg_txt=self.dr.tostring()
        if display:
            from IPython.display import SVG,display
            display(SVG(self.svg_txt))

    def save_svg(self,filename="dummy.svg"):
        with open(filename,"w") as fw:
            fw.write(self.svg_txt)

    def get_svg(self):
        return self.svg_txt


class Lsys:
    def __init__(self, txt, rule=[], mode="jupyter"):
        self.txt=txt
        self.rule=rule
        self.stack=[]
        self.mode=mode
        self.random_seed=None

    def set_seed(self,value):
        self.random_seed=value

    def apply_rule(self, iteration=5):
        ans=self.txt
        for i in range(iteration):
            to_string=[]
            if self.rule==[]:
                return ans
            for index,r in enumerate(self.rule):
                com=re.split(r'->',r)
                ans=ans.replace(com[0],"%d"%index)
                to_string.append(com[1])
            for index,r in enumerate(self.rule):
                ans=ans.replace("%d"%index, to_string[index])
        return ans

    def render(self,
                iteration=5,
                length=20, angle=90,
                initial_pos= [0,0],
                initial_angle=90,
                display=True
                ):
        initial_pos = copy.copy(initial_pos)

        txt=self.apply_rule(iteration)
        self.stack=[]

        if self.mode=="turtle":
            self.r = turtle_render(txt, self.stack)
        elif self.mode=="jupyter":
            self.r = jupyter_render(txt, self.stack)

        self.r.render(length=length, angle=angle,
                 initial_pos=initial_pos,
                 initial_angle=initial_angle,
                 display=display, random_seed=self.random_seed)

    def get_svg(self):
        if self.mode!="jupyter":
            print("Error: get_svg is not supported for mode: %s" % self.mode)
            return
        return self.r.get_svg()

    def save_svg(self,
                filename="dummy.svg"
                ):

        if self.mode!="jupyter":
            print("Error: save_svg is not supported for mode: %s" % self.mode)
            return

        self.r.save_svg(filename)

    def get_img(self):
        if self.mode!="jupyter":
            print("Error: get_png is not supported for mode: %s" % self.mode)
            return
        import cairosvg
        import StringIO
        from PIL import Image
        txt=self.r.get_svg()
        png=cairosvg.svg2png(bytestring=txt)
        fpng=StringIO.StringIO(png)
        im=Image.open(fpng)
        return im

if __name__ == '__main__':
    l=Lsys("X",["X->F-[[X]+X]+F[+FX]-X","F->FF"],mode="turtle")
    l.render(iteration=5,length=6, angle=22.5, initial_pos=[0,-300])

