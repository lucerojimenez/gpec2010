GPEC is a software to obtain phase diagrams and other thermodynamic plots for binary mixtures, as calculated with equations of state. It can be helpful for either educational, academic or development purposes. It is easy to use and you do not have to provide any initial guesses or other inputs.

This is a rewriting from scratch version of the GPEC frontend, written in Python by Martín Gaitán as part of his final degree project on Computer Engineering at Universidad Nacional de Córdoba, Argentina.

## Attention ##

GPEC is under active development. Many features are still unimplemented and many others could change. So, at this time GPEC is at (very) Beta stage, and should not be used for production purposes.

## How to try it ##

**On Windows**

Just download the  _featured_ zip of the last beta version from the right panel, uncompress and run **aui.exe**.

**On Linux platforms**

There is not specific packages at the moment. But is straightforward to get GPEC running from the code. For example, on Ubuntu/Debian distribution you can do

```
$ sudo apt-get install python-matplotlib python-matplotlib-data python-numpy python-wxgtk2.8 wine subversion
$ svn checkout https://gpec2010.googlecode.com/svn/trunk/src gpec
$ cd gpec
$ python aui.py
```

## Screenshot and figures ##

See ExampleFigures

## Discussion List ##

Send feedback and keep updated about the project subscribing to  [our discussion list](http://groups.google.com.ar/group/gpec-discuss).

## Screencast ##

this video is a bit outdated at this time

<a href='http://www.youtube.com/watch?feature=player_embedded&v=DBX-FTpWc-c' target='_blank'><img src='http://img.youtube.com/vi/DBX-FTpWc-c/0.jpg' width='425' height=344 /></a>

## Documentation in course (in spanish) ##

http://gpec2010.googlecode.com/svn/trunk/docs/_build/html/index.html

## Cost estimation ##

&lt;wiki:gadget url="http://www.ohloh.net/p/484516/widgets/project\_cocomo.xml" height="240" border="0"/&gt;