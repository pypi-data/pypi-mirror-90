"""a vary mary Xmas

mary crismas heare are some proliminary extensions for Xmas
"""
import typing
from os.path import dirname, realpath, join
from tkinter import PhotoImage
from tkinter import Canvas as tkCanvas
from time import sleep
from random import randint, choice, random, gauss
from functools import partial



from AMcomandPack.geo.extensions.extensionFiles import SceneElement


class present(SceneElement):
    """a present

        marry Xmas 
        this is a Xmas present and sublcass of SceneElement
        """
    
    def __init__(self, x: float, y: float, name: str=f"Xmas present", presentName: int=0):
        """constructor

            @param x: the x pos of the present
            @type x: int

            @param y: the y pos of the present
            @type y: int

            @param name: the name of the present
            @type name: str

            @param id: what present to use
            @type id: int
            """
        assert hasattr(x, "__float__"), f"param x must be float not {type(x)}"
        assert hasattr(y, "__float__"), f"param y must be float not {type(y)}"
        assert hasattr(name, "__str__"), f"param name must be string not {type(name)}"
        assert hasattr(presentName, "__int__"), f"param presentName must be float not {type(presentName)}"

        SceneElement.__init__(self, name=name)

        self.x, self.y = x, y
        """the position of the present"""
        self.image = PhotoImage(file=f"{dirname(realpath(__file__))}/images/Xmas/present{presentName}.png")
    
    def render(self):
        "render image"
        self.subRenders.append(self.cv.create_image(self.x, self.y, self.image))

class XmasTree(SceneElement):
    """an XmasTree

        marry Xmas 
        this is a Xmas Tree and sublcass of SceneElement
        """
    
    def __init__(self, x: float, y: float, name: str=f"Xmas Tree", TreeName: int=0):
        """constructor

            @param x: the x pos of the Tree
            @type x: int

            @param y: the y pos of the Tree
            @type y: int

            @param name: the name of the Tree
            @type name: str

            @param id: what Tree to use
            @type id: int
            """
        assert hasattr(x, "__float__"), f"param x must be float not {type(x)}"
        assert hasattr(y, "__float__"), f"param y must be float not {type(y)}"
        assert hasattr(name, "__str__"), f"param name must be string not {type(name)}"
        assert hasattr(TreeName, "__int__"), f"param TreeName must be float not {type(TreeName)}"

        SceneElement.__init__(self, name=name)

        self.x, self.y = x, y
        """the position of the present"""
        self.image = PhotoImage(file=f"{dirname(realpath(__file__))}/images/Xmas/XmasTree{TreeName}.png")
    
    def render(self):
        "render image"
        self.subRenders.append(self.cv.create_image(self.x, self.y, self.image))

class SnowyBackground(SceneElement):
    """Xmas snowy Background

        a snowy backround with snow flakes falling down
        """
    
    def __init__(self, name:str="snowy Backround", density: float=1, maxFlakesPerTick:int=1, tickTime: float=.1):
        """constructor

            @param name: the name of the backround dosnt do anything
            @type name: str

            @param density: the snow flake denscity schort version the higher the number, the higher the probability of the a snow flake spawning
                            betwean 0 and 1
            @type dinsity: float

            @param maxFlakesPerTick: how many flakes spawn per tick as a cap
            @type maxFlakesPerTick: int

            """
        SceneElement.__init__(self, name=name)
        assert hasattr(density, "__float__"), f"param density must be float not {type(density)}"
        self.density = float(density)
        "how probable snow flakes spawn"
        assert 1 >= density >= 0, f"invalid range for param density, density must be betwean 0 and 1 not {density}"

        assert hasattr(maxFlakesPerTick, "__int__"), f"param maxFlakesPerTick must be int not {type(maxFlakesPerTick)}"
        self.maxFlakesPerTick = int(maxFlakesPerTick)
        "max amount of flakes spawned per tick"
        if maxFlakesPerTick < 0: ValueError(f"param maxFlakesPerTick must be greater 0 not {maxFlakesPerTick}")

        assert hasattr(tickTime, "__float__"), f"param tickTime must be float not type {type(tickTime)}"
        self.tickTime = float(tickTime)
        """how long a tick lasts

            the lenth of time in seconds of the tick
            a tick is the time in that is waited before trying to create a new snow flake with sucessprobability density
            """
        if self.tickTime <= 0: ValueError(f"param tickTime must be greater 0 not {tickTime}")
        """how long the tick lasts

            how long a tick lasts a tick is the time periond betwean attempted spawns
            witch hava a density chance to suksead
            """


    def renderingScript(self, top:int, bottom:int, left:int, right:int, size:int=15, randFun=randint, flakeId:typing.List[int]=[0], flakeIdSelector=choice, yspeed:int=gauss, yspeedParams=(3, 1)) -> None:
        """add snow flackes

            let it snow let it snow let it snow
            no assersions as of now

            @param top: the top to snow spaneing
            @type top: int, func
            @param bottom : the layer they fall to
            @type top: int, func
            @param left: the left most place they spawn from
            @type left: int, func
            @param right: the right most x the flacke spawn at
            @type right: int, func
            @param size: the size of the flakes
            @type size: int, func

            @param randFun: custom random function default to random.randint
                            takes 2 arguments
            @type randFun: function 2 arguments

            @param flakeId: a list of the intagers of the flakes must be valid flaks
            @type: flakeId: list<int>

            @param flakeIdSelector: random selection of flaeIds default random.coice
            @type flakeIdSelector: func(lakeId:list<int>)->int

            @param flakeIdSelector: random func to to select flakeIds form
            @param yspeed: random func for y movement
            @param yspeedParams: params passed to yspeed"""
        
        assert hasattr(top, "__int__")    or hasattr(top, "__call__"),    f"param top must be int or function not {type(top)}"
        assert hasattr(bottom, "__int__") or hasattr(bottom, "__call__"), f"param bottom must be int or function not {type(bottom)}"
        assert hasattr(yspeed, "__float__") or hasattr(yspeed, "__call__"),f"param yspeed must be float or function not {type(yspeed)}"

        assert hasattr(left, "__int__"),   f"param left must be int not {type(left)}"
        assert hasattr(right, "__int__"),   f"param right must be int not {type(top)}"

        assert hasattr(size, "__int__") or hasattr(size, "__call__"),   f"param top must be int or function not {type(size)}"
        assert hasattr(randFun, "__call__"), f"param randFun must be function not {type(randFun)}"
        assert hasattr(flakeIdSelector, "__call__"), f"param flakeIdSelector must be function not {type(flakeIdSelector)}"

        assert isinstance(flakeId, list) and len(flakeId) > 0, f"flakeId must be a list of intagers of len > 0 not {flakeId}"

        topFun = top if hasattr(top, "__call_") else (lambda x: int(top))
        bottomFun = bottom if hasattr(bottom, "__call_") else (lambda x: int(bottom))
        leftFun = int(left)
        rightFun = int(right)
        sizeFun = size if hasattr(size, "__call__") else (lambda x: int(size))
        yspeedFun = yspeed if hasattr(yspeed, "__call__") else (lambda *args: float(yspeed))
        
        def addFlake():
            "add the flakes"
            x = randFun(rightFun, leftFun)
            y = topFun(x)
            flakeNum = flakeIdSelector(flakeId)

            dy = yspeedFun(*yspeedParams)/2
            if dy < 0:
                dy = -dy
            
            nsize = sizeFun(x)
            path = join(dirname(realpath(__file__)), f"images/Xmas/snowFlake{flakeNum}.png")
            img = PhotoImage(file = path).subsample(nsize, nsize)

            flake = self.cv.create_image(x, y, img)# 
            self.subRenders.append(flake)
            bottom = bottomFun(x)

            def move(y, flake):
                y -= dy
                if y < bottom:
                    self.cv.delete(flake)
                    return

                self.cv.delete(flake)
                flake = self.cv.create_image(x, y, img)
                #pos = tkCanvas.coords(self.cv, flake)[1]
                self.cv.after(30, lambda: move(y, flake))

            move(y, flake)
        
        while self.active:
            if random() < self.density and self.cv.master.ready:
                addFlake()
                continue
            sleep(self.tickTime)

    
        

