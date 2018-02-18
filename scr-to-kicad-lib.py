import eaglescr
import argparse
import sys

library_header = "EESchema-LIBRARY Version 2.3\n#encoding utf-8"
part_header = "#\n# %s\n#"
library_footer = "#\n#End Library"

# Mapping of Eagle pin rotation angles to KiCad pin orientations.
rotations = {0: "R", 180: "L", 90: "U", 270: "D"}

# Mapping of Eagle pin types to KiCad pin types.
pintypes = {
        "I/O": "B" # Bidirectional
    ,   "Pas": "P" # Passive
    ,   "Pwr": "W" # Power input
    }

def guess_rectangle(lines):
    """Atempt to guess whether a list of lines forms a rectangle, and if so
    return the coordinates of the bounding box for this rectangle. Returns
    None otherwise."""
    
    # Get the coordinates of the bounding box formed by these lines.
    min_x = min([min(o.x1, o.x2) for o in lines])
    max_x = max([max(o.x1, o.x2) for o in lines])
    min_y = min([min(o.y1, o.y2) for o in lines])
    max_y = max([max(o.y1, o.y2) for o in lines])
    
    # Verify that each line is /on/ the bounding box.
    for line in lines:
        if line.x1 in [min_x, max_x]:
            continue
        if line.x2 in [min_x, max_x]:
            continue
        if line.y1 in [min_y, max_y]:
            continue
        if line.y2 in [min_y, max_y]:
            continue

        return None

    return ((min_x, min_y), (max_x, max_y))

argparser = argparse.ArgumentParser(description="Parse an Eagle SCR file and "\
    "convert it to a KiCad symbol.")
argparser.add_argument('path', metavar='path-to-scr-file', type=str, \
    help="Path to an Eagle SCR file.")
args = argparser.parse_args()

# Eagle SCR parser.
scrparser = eaglescr.Parser()

# Load and parse the Eagle SCR file.
for line_index, line in enumerate(open(args.path)):
    if not scrparser.handle_line(line):
        print >> sys.stderr, "Unsupported command on line %d: %s" % (line_index, repr(line))

print library_header

for partname, sym in scrparser.context['symbols'].items():
    print part_header % partname
    print "DEF %s %s 0 40 Y Y 1 F N" % (partname, sym.device.prefix)
    print "F0 \"%s\" 0 -100 50 H V C CNN" % sym.device.prefix
    print "F1 \"%s\" 0 100 50 H V C CNN" % partname
    print "$FPLIST"
    print " *%s*" % sym.device.package.name
    try:
        print " *%s*" % sym.device.attributes['Package']
    except KeyError:
        pass
    print "$ENDFPLIST"

    print "DRAW"

    # Attempt to make a rectangle from the symbol lines, because many
    # components will have a rectangular symbol. If not, just draw the lines
    # individually.
    rectangle = guess_rectangle(sym.lines)
    if rectangle:
        (x1, y1), (x2, y2) = rectangle
        print "S %d %d %d %d 1 1 1 f" % (x1, y1, x2, y2)
    else:
        for line in sym.lines:
            print "P 2 0 1 1 %d %d %d %d N" % (line.x1, line.y1, line.x2,
                line.y2)

    # List all the pins.
    for pin in sym.pins.values():
        try:
            rotation = rotations[pin.rotation]
        except KeyError:
            rotation = "R"
            print "# Warning: Failed to look up rotation value of %d for "\
                "pin %s, assuming %s" % (pin.rotation, pin.name, rotation)

        try:
            pintype = pintypes[pin.pintype]
        except KeyError:
            pintype = "U" # assume "unspecified", should be a safe value
            print "# Warning: Failed to look up pin type of %s for "\
                "pin %s, assuming %s" % (pin.pintype, pin.name, pintype)

        print "X %s %s %d %d 200 %s 40 40 1 1 %s" % ( pin.name,
            pin.device_pin_number, pin.pos_x, pin.pos_y, rotation, pintype)

    print "ENDDRAW"
    print "ENDDEF" 

print library_footer

