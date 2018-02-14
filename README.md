# Voice Stream Activity Detection(VSAD)

Here is an application about voice activity detecation in real time. The reason why I write  this application is that I found there is many examples about voice acitvity detection(VAD) online but few in real time.

This application base on python3.6 and I am not sure whether this work well on python2.X.

If you would like to any comments, please email me at jack.feng.liu@gmail.com.

## Dependencies

* 1 If your OS base on Debian, please run the following command:

    `sudo apt install portaudio19-dev`

* 2 Install Python external library

    `pip install -r requirements.txt`

* 3 (Optional) If you want to bundles this application and all its dependencies into a single packages, you can run following command:

    `pip install pyinstaller`

## HOW TO

You can run `python VSAD.py` directly.

Also, you can run `pyinstaller -F VSAD.spec` to build first. and then run the `VSAD` in `./dist/` directory. In this way, this program can detach from the python environment.