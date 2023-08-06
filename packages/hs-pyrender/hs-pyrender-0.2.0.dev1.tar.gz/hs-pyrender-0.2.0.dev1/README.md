# PyRender
This is a Rendering engine made in Python by Arnav


## Installing
You Can Install it either by running the command

`git clone https://github.com/HotShot0901/PyRender`
If you have git installed

OR

You can Download the latest ZIP or any release.

Run `python test.py` (in CMD) to check your Installation.

OR

You can use pip.

`pip install hs-pyrender`

### If downloaded from GIT
You could paste the **pyrender** sub-folder in `Python_Dir/Lib/site-packages` to use it in your project.

Or, you could also make a sub-project in the main **PyRender** and use `from pyrender import *`.

## Usage
To import: `from pyrender import *`

Making a Renderer: `renderer=PyRender(dimension)` dimension could be **(640, 360)**

Vector2's: They are very essencial to rendering. They tell the position and dimension of the shape.

Drawing: `renderer.drawRect(posX, posY, dimX, dimY, Color(r, g, b), DrawMode.Top)`

Frame loop:

    for _ in range(180):
        renderer.rotate(math.randins(_))
        renderer.drawRect(posX, posY, dimX, dimY, Color(r, g, b), DrawMode.Top)

        renderer.nextFrame(delCurr=True)


Rendering: `renderer.render(renderPath, videoTitle)`

You will get your video in **renderPath/frames/videoTitle.mp4**

Finally:

    from pyrender import *
    renderer=PyRender((640, 360))

    for _ in range(180):
        renderer.rotate(math.randins(_))
        renderer.drawRect(posX, posY, dimX, dimY, Color(r, g, b), DrawMode.Top)

        renderer.nextFrame(delCurr=True)

    renderer.render("E:", "video")
