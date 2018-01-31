def print_file_data(file_data,name,name1):
    for line in range(len(file_data)):
        if file_data[line]==name:
            for j in range(line,len(file_data)):
                if file_data[j]!=name1:
                    print file_data[j]
                else:
                    return 0

def print_file_data1(file_data):
    for line in file_data:
        for l in range(len(line)):
            print line[l]

file_data1=list(i.strip().split('\n') for i in open('make1.txt'))
#print file_data1
#num=print_file_data(file_data1,['LITERAL TABLE'],['SYMBOL TABLE'])
#num=print_file_data(file_data1,['SYMBOL TABLE'],['INTERMEDIATE CODE'])
print_file_data1(file_data1)



