# lsys

L-System library for python and jupyter notebook

# example

```python
from lsys import Lsys

l=Lsys("X",["X->X[F+X][F-X]","F->FF"])
l.set_seed(0)
l.render(iteration=6,length="randint(1,15)", angle="randint(-50,50)*0.2+20", initial_pos=[0,-300])
```

![result](https://github.com/ashitani/lsys/blob/master/mytree.png)

# Sample notebooks

- [Demonstration](https://github.com/ashitani/lsys/blob/master/Fractal.ipynb)
- [Tutorial](https://github.com/ashitani/lsys/blob/master/Tutorial.ipynb)

# Requirements

- Jupyter notebook
- [svgwrite](https://pypi.python.org/pypi/svgwrite)
- [cairosvg](http://cairosvg.org/)
- [Pillow](https://pillow.readthedocs.io/en/3.4.x/)

# Acknowledgement

- [aidiary](http://aidiary.hatenablog.com/entry/20131125/1385385271) for introducing L-System and showing examples.

# License

MIT
