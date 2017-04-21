for r in range(0, 7) :
    for c in range(0, 8) :
        filename = str(r) + "-" + str(c) + ".JPG"
        xmlname = "L5-" + str(r) + "-" + str(c) + ".cell"
        f = open(xmlname, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<cell img="1/' + filename + '">\n')
        f.write('</cell>\n')
        f.close() 