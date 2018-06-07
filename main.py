from googletrans import Translator


file = ""  # Put your filename here
dest_language = 'en'  # Destination language to translate to

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def get_lines(file):
    with open(file, encoding='utf-8') as file_pointer:
        lines_string = file_pointer.read()  # This is a single string of the file
        lines = lines_string.split('\n')  # This is a list of lines
    return lines


def extract_lines(lines):  # Returns the lines that need to be translated
    start_line = 0
    while lines[start_line][0:8] != "Dialogue":
        start_line += 1

    return lines[start_line:], start_line


def extract_string(lines):
    to_translate = []
    for line in lines:
        if '{' in line:  # For when the uses effects
            to_translate += [line[line.find('}') + 1:]]
        else:  # Standard dialogue line
            start_pos = find_nth(line, ',', 9)
            to_translate += [line[start_pos + 1:]]
    return to_translate


def translate(to_translate):
    translations = []
    batch_size = 50

    if len(to_translate) < batch_size:
        translator = Translator()
        translations += translator.translate(to_translate, dest=dest_language)
    else:
        max_value = 0
        for i in range(batch_size, len(to_translate), batch_size):
            translator = Translator()
            print("Processing translations", max_value, "to", i,)
            translations += translator.translate(to_translate[max_value:i], dest='en')
            max_value = i
        remainder = max_value + len(to_translate) % batch_size
        print("Processing translations", max_value, "to", remainder, )
        translations += translator.translate(to_translate[max_value:remainder], dest='en')
    return translations


def recombine(translations, lines_to_translate):
    index = 0
    new_lines = []
    try:
        for line in lines_to_translate:
            if '{' in line:  # For when the uses effects
                new_lines += ["".join((line[:line.find('}') + 1], translations[index].text))]
                """
                print(translations[index].text)
                print(new_lines[index])
                print()
                """
                index += 1
            else:
                start_pos = find_nth(line, ',', 9)
                new_lines += ["".join((line[:start_pos + 1], translations[index].text))]
                """
                print(translations[index].text)
                print(new_lines[index])
                print()
                """
                index += 1
    except:
        pass
    return new_lines


def add_header(start_line, raw_lines, translated_lines):
    header = raw_lines[:start_line]
    full_ass = header + translated_lines
    return full_ass


def write_file(full_ass):
    filename = "[Translated] " + file
    fp = open(filename, 'w', encoding='utf-8')
    for line in full_ass:
        fp.write(line + '\n')
    fp.close()


def usage():
    print("Invalid start parameters(s) \n"
          "Try 'python main.py [file].ass' \n"
          "or 'main.py [file].ass' on Windows \n"
          "or if running from file, specify a filename to translate \n", end="")


def main():
    raw_lines = get_lines(file)
    lines_to_translate, start_line = extract_lines(raw_lines)  # Returns the lines that need to be translated
    to_translate = extract_string(lines_to_translate)
    translated_lines = translate(to_translate)
    translated_dialogue = recombine(translated_lines, lines_to_translate)
    full_ass = add_header(start_line, raw_lines,  translated_dialogue)
    write_file(full_ass)


if __name__ == "__main__":
    import sys
    import os.path
    if len(sys.argv) == 1 and file != "":
        main()
    elif len(sys.argv) != 2:
        usage()
    elif os.path.exists(sys.argv[1]):
        file = sys.argv[1]
        main()
