Eagle SCR to KiCad lib
--
A Python command line tool for converting an electronic part specified in AutoDesk Eagle's scripting format to a KiCad library file.

Example
--
In this example, we'll convert an ```STM32F405RGT6``` part, specified in an Eagle script file (found in [this zip](http://www.farnell.com/cad/1724597.zip) provided by [Farnell](http://uk.farnell.com/stmicroelectronics/stm32f405rgt6/mcu-32bit-cortex-m4-168mhz-lqfp/dp/2064363?st=stm32F405rgt6)) to a KiCad library.
```shell
$ virtualenv venv
# (VirtualEnv sets up a new python environment)
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
# (pip installs the dependencies into the venv)
(venv) $ python scr-to-kicad-lib.py /path/to/STM-STM32F405RGT6.scr > STM32F405RGT6.lib
# (You may get some warnings about unsupported commands - the Eagle SCR parsing library doesn't handle everything yet)
(venv) $
```

Success! Looks like it generated a KiCad library file with one part:

```shell
(venv) $ head -6 STM32F405RGT6.lib
EESchema-LIBRARY Version 2.3
#encoding utf-8
#
# STM32F405RGT6
#
DEF STM32F405RGT6 U 0 40 Y Y 1 F N
```

If you load this .lib into KiCad with the library manager, you can see the converted part:

![Converted part in KiCad](https://raw.githubusercontent.com/derpston/eagle-scr-to-kicad-lib/master/docs/kicad_part.png "Converted part in KiCad")

For comparison purposes, here's the same part as drawn by Eagle after executing the original .scr file: 

![Original part in Eagle](https://raw.githubusercontent.com/derpston/eagle-scr-to-kicad-lib/master/docs/eagle_part.png "Original part in Eagle")
