"""extension generals

general extensions of SceneElements used by other extensions and renersing scripts
"""

import typing
from time import time
from threading import Thread
#from AMcomandPack.geo.tk import Canvas

#do some other stuff if you want
#            >>> element.mainloop() #if it has a rendering script
#        or 
#            >>> element.render() #if it is staticly renered mainloop can alsow be used but has more overhead

class SceneElement:
    """ element of scene

        a scene element is a custom element that can be aded to scene and edited
        
        sintax for usage is somthing like this
            >>> cv = am.geo.Canvas(...)
            >>> element = am.geo.extensions.SceneElement()#create scene element
            >>> cv.addSceneElement(element)
        
        do some other stuff if you want
            >>> element.mainloop() #if it has a rendering script

        of if it dosnt have a rendering scrpt
            >>> element.render() #if it is staticly renered mainloop can alsow be used but has more overhead
        """
    subRenders: typing.List[int] = []
    """contains all the subrenders"""
    def __init__(self,name: str=f"element from {time()}") -> None:
        """constructor
        
            @param name: the name of the SceneElement
            @type name: string"""
        assert hasattr(name, "__str__"), f"param name must be str not {type(name)}"
        self.name = name
        "the name of the element"
        self.active = False
        "weather or not script is currently active"
    
    def __del__(self):
        "delete element"
        self.endMainLoop()
        self._clear()


    def endMainLoop(self):
        """terminate rendering script

            termitate the rendeing scipt however the custom script must implement the termination if self.active is False"""

        self.active = False

    def _addToScene(self, canvas):
        """add element to scene
            """
        canvas.elements.append(self)
        self.cv = canvas
        """the canvas the Ement exists in"""
    
    def render(self):
        """render staticly
        
            render the element staticly so no change if you want to edit over time use renderingScript
            this dose absolutyl nothing as it schuld be overriden by subclass"""
        pass

    def _clear(self):
        """remove all reners"""
        for subrender in self.subRenders:
            self.cv.delete(subrender)
    
    def renderingScript(self, *args, **kwargs):
        """script to edit renders

            a script to edit the render run from thread this is suposed to be overidden by subclass
            """
        self.render()

    def mainLoop(self, *args, **kwargs):
        """run rendering script

            run rendering script in Thread if rendering script is not overriden it will be the same as render
            therfor if you want to staticly render somthing use render as less overhead is involved

            @param args and kwargs: are the parameters and keyword arguments used by the the rendering script so see that for what they do"""
        self.active = True
        self.execThread = Thread(target=self.renderingScript,
                                 args=args,
                                 kwargs=kwargs, 
                                 daemon=True,
                                 name=f"sceneElement {self.name} mainloop thread")
        "thread running renderingScript"
        self.execThread.start()
