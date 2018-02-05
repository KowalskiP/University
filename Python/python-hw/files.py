student_list = []
name_dict = {}
family_dict = {}
year = ""
file_in = open('home.htm', 'r', encoding='cp1251')
file_out = open('result.txt', 'w', encoding='utf-8')
string_out = file_in.readlines()

for i in string_out:
        begin_year = i.find(">20")
        end_year = i.find("/h3>")

        if begin_year != -1 and end_year - begin_year > 0:
            if year == "":
                year = i[begin_stud + 4:end_stud]
                print(1)
                print(i)
                print(begin_stud + 4)
                print(end_stud)
                print(year)
            else:
                file_out.writelines(year)
                file_out.writelines(name_dict)
                year = ""
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
file_out.writelines(name_dict)
file_out.writelines(family_dict)
file_in.close()
file_out.close()
#with open('result.txt', 'w', encoding='utf-8') as file_holder:
#   for i in student_list:
#       file_holder.writelines(student_list)
#fileHolder=open('1.txt', 'r')
#stringOut=fileHolder.read(4)
#stringOut=fileHolder.readlines()
#fileHolder.close()

#student_list.append(student) 
            
