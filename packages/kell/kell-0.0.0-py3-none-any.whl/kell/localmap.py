from typing import Union, Tuple, Callable
from anabel import jit

def localmap(
            dim:Union[int,Tuple[Tuple[int,int]]]=None,
            main:str="main",
            jacx:str=None,
            form:str="x,y,s=s,p=p,**e->x,y,s"
            statevar:str="state",
            paramvar:str="params",
            origin=None, 
            order =None):
    """
    Wraps a basic local map generator.
    
    This wrapper carries out the following operations:
        
        - adds an `origin` attribute to the generated function according to the
          `dim` specified.

        - adds a `shape` attribute based on dimensions given in `dim`
          
        - adds option to wrapped function to expose closed-over local variables
          as an attribute.
    """


    def _decorator(func):
        @wraps(func)
        def wrapper(*args, _expose=False, _jit=False, _form_as:str=None, _curry=False, **kwds):
            loc = func(*args, **kwds)

            if origin is None:
                assert dim is not None
                if isinstance(shape,int):
                    shape = ((dim, 1), (dim,1))
                else:
                    xshape, yshape = dim
                    if isinstance(xshape,int):
                        xshape = (xshape, 1)
                    if isinstance(yshape,int):
                        yshape = (yshape, 1)
                    shape = (xshape, yshape)
                x0, y0 = anp.zeros(xshape), anp.zeros(yshape)
                origin = x0, y0, loc[statevar], loc[paramvar]

            else:
                if isinstance(origin,str):
                    origin = loc[origin]
                shape = origin[0].shape, origin[1].shape
            
            main = loc[name]

            #-transformations------------------
            # if _form_as is not None:
            #     main = reform(main, form, _form_as)
                
            if _jit:
                main = jit(main)
            #----------------------------------
            if expose:
                main.closure = loc

#             main.params = loc[paramvar]
            main.origin = origin
            main.shape  = shape
            
            return main

    return wrapper

def reform(func:Callable, form:str, newform:str):
    old_args, old_out = form.split("->")

    old_out = old_out.replace(" ","").split(",")


    new_args, new_out = newform.split("->")
    new_out = new_out.replace(" ","").split(",")

    indices = ",".join(old_out.index[new] for new in new_out)

    return exec(f"def reformed({}): return func({})[{indices}]")









