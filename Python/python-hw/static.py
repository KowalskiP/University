student_list = []
name_dict = {}
family_dict = {}
year = ""
file_in = open('home.htm', 'r', encoding='cp1251')
file_out = open('result.txt', 'w', encoding='utf-8')
string_out = file_in.readlines()
for i in string_out:
        begin_year = i.find("<h3>")
        end_year = i.find("</h3>")
        if begin_year != -1 and end_year - begin_year > 0:
            if year == "":
                year = i[begin_year + 4:end_year] + '\n'
            else:
                file_out.writelines(year)
                keys = name_dict.keys()
                keys = list(keys)
                keys.sort()
                for j in keys:
                    s = j + '-' + str(name_dict[j]) + '\n'
                    file_out.writelines(s)
                name_dict.clear()
                year = i[begin_year + 4:end_year] + '\n'
        begin_stud = i.find("/\">")
        end_stud = i.find("</a>")
        if begin_stud != -1 and end_stud - begin_stud > 0:
            student = i[begin_stud + 3:end_stud].split()
            if student[1] in name_dict:
                name_dict[student[1]] += 1
            else:
                name_dict[student[1]] = 1
            last_chars = student[0][-2:]
            if last_chars in family_dict:
                family_dict[last_chars] += 1
            else:
                family_dict[last_chars] = 1
file_out.writelines(year)
keys = name_dict.keys()
keys = list(keys)
keys.sort()
for j in keys:
    s = j + '-' + str(name_dict[j]) + '\n'
    file_out.writelines(s)
keys = family_dict.keys()
keys = list(keys)
keys.sort()
for j in keys:
    s = j + '-' + str(family_dict[j]) + '\n'
    file_out.writelines(s)
file_in.close()
file_out.close()
