# Studio Filters

A clone of Zoom's Studio Effects feature written in Python.

## Dependencies

Make sure to install Python 3 and PyPi (pip) before installing any dependencies. To verify these are installed, make sure the `python3` and `pip`/`pip3` commands exist.

If your computer uses the `pip3` command, replace `pip` with `pip3` in the following dependency installation instructions.

 - `MSS` (screen capture at a high FPS): run `pip install mss==2.0.22`
 - `Flask` (streaming results of the filter): run `pip install flask`
 - `dlib` (face recognition dependency): follow instructions at [https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
 - `face-recognition` (find faces and mark landmarks): run `pip install face-recognition`
 - `Open CV Python` (preparing screen capture for face recognition): run `pip install opencv-python`
 - `NumPy` (preparing screen capture for face recognition): `pip install numpy`

## Usage

1.

```
git clone https://github.com/xtrp/studio-filters
```

2.

```
cd path/to/studio-filters/
```

3.

Open a video, camera feed, or photo that you'd like to filter (ex: a Zoom window, the Camera or Photo Booth app, etc.).

Move the application with the image/video you'd like to filter to the top left of your screen. Make note of the pixel position and pixel dimensions of the image/video to be filtered, in the format of: `(top left Y coordinate, top left X coordinate, height, width)`.

4.

Edit the `main.py` file, and rewrite line 3 so that the `SCREENSHOT_COORDS` variable is defined as the position and dimensions that was noted in the previous instruction.

5.

Run the program:

```
python3 main.py
```

6.

Open [http://localhost:5000/](http://localhost:5000/) in your browser and make sure that the previous window with the image/video to be filtered is not covered or moved. The opened page in your browser should show a live-filtered version of the content at the specified dimensions on your screen. Depending on the specs of your machine, whether an external monitor is being used, and whether your machine is charging, there may be a slight delay in the filter output on the browser side.

## Editing Colors of Each Filter

If you'd like to change the color of the filtered eyeliner, digital eyebrows, lipstick, or mustache, open `main.py` and find the relevant lines under the following comments: `eyebrows`, `lipstick`, `eyeliner`, `mustache`.

These lines of code should all end with something like `fill=(0,0,0,0)`. Here, replace the tuple of four values (ex: `(0,0,0,0)`) with the new RGBA value of the color you'd like instead of the existing one.

For example, if you'd like the lipstick to be bright red, locate the lines of code under the `# lipstick` line, and make sure the lines include `fill=(255, 0, 0, 255)` instead of the existing color value.

## Troubleshooting

**This program has not been tested on Windows or Linux.** There may be a number of problems when running this program on these platforms.

If there are issues with defining the dimensions and position of the image/video to be filtered on your screen, try checking the format again, and take note of the pixel ratio of your device (ex: some Apple Retina displays have a pixel ratio of two).

## License and Contributing

See `LICENSE` for licensing information.

Give this repo a ⭐️ if you like it, and always feel free to contribute or submit an issue if you have one.
