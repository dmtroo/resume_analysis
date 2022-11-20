def parse(fileName):

    with open(fileName, encoding="utf-8") as file:
        fileData = file.read()

    # replace the target strings and write file again
    fileData = fileData.replace("\\n", "\n")
    fileData = fileData.replace("\\t", "  ")

    with open(fileName, 'w', encoding="utf-8") as file:
        file.write(fileData)

    # add the analysis file to a two-dimensional array
    with open(fileName, encoding="utf-8") as textFile:
        lines = [line.split() for line in textFile]
        del lines[0:10]  # deletes first 11 lines

    # write file again
    with open(fileName, 'w', encoding="utf-8") as file:
        for line in lines:
            file.write(str(line))

    return lines
