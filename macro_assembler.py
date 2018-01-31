import itertools as it
import re
import pprint
pp=pprint.PrettyPrinter(indent=0)




reg_32={'eax':0,'ecx':1,'edx':2,'ebx':3,'esp':4,'ebp':5,'esi':6,'ebi':7}
reg_16 = { 'ax':0,'cx':1,'dx':2,'bx':3,'sp':4,'bp':5,'si':6,'di':7}
r32 = { 'eax':'000','ecx':'001','edx':'010','ebx':'011','esp':'100','ebp':'101','esi':'110','ebi':'111'}
r16 = { 'ax':'000','cx':'001','dx':'010','bx':'011','sp':'100','bp':'101','si':'110','di':'111'}
r8 =  { 'al':'000','cl':'001','dl':'010','bl':'011','ah':'100','ch':'101','dh':'110','bh':'111'}
mod = ['00','01','10','11']

mov_i={"r32,r32":{"mov_op":"mov1","size":2},
        "r32,mem":{"mov_op":"mov2","size":4},
        "r32,imm":{"mov_op":"mov3","size":4},
        "mem,r32":{"mov_op":"mov4","size":3},
        "r16,r16":{"mov_op":"mov5","size":1},
        "r16,mem":{"mov_op":"mov6","size":2},
        "r16,imm":{"mov_op":"mov7","size":3},
        "mem,r16":{"mov_op":"mov8","size":3}}

mov_fix={"r32,r32":{"no_op": 2 ,"operands": ["r32","m32"] ,"opcode": "89","i_size": 2},
            "r32,m32":{"no_op": 2 ,"operands": ["r32","m32"] ,"opcode": "8B","i_size": 6},
            "m32,r32":{"no_op": 2 ,"operands": ["m32","r32"] ,"opcode": "89","i_size": 6},
            "r16,r16":{"no_op": 2 ,"operands": ["r16","r16"] ,"opcode": "6689","i_size": 3},
            "m16,r16":{"no_op": 2 ,"operands": ["m16","r16"] ,"opcode": "6689","i_size": 7},
            "r16,m16":{"no_op": 2 ,"operands": ["r16","m16"] ,"opcode": "668B","i_size": 7}}

mov_not_fix={"r32,imm32":{"no_op": 2 ,"operands": ["r32","imm32"] ,"opcode": "B8","i_size": 5},
                "r16,imm16":{"no_op": 2 ,"operands": ["r16","imm16"] ,"opcode": "66B8","i_size": 4},
                "r32,m321":{"no_op": 2 ,"operands": ["r32","m32"] ,"opcode": "B8","i_size": 4},
                "r16,m161":{"no_op": 2 ,"operands": ["r16","m16"] ,"opcode": "66B8","i_size": 4}}
print '***'
print mov_fix["r32,r32"]["opcode"]

all_register={"ax":"r16","cx":"r16","dx":"r16","bx":"r16","sp":"r16","bp":"r16","si":"r32","di":"r16","eax":"r32","ecx":"r32","edx":"r32","ebx":"r32","esp":"r32","ebp":"r32","esi":"r32","ebi":"r32"}






#==============================================seperate data=========================================
def seperate_data_section(file_data):
    data_section=[]
    data_sec=[]
    section_data=[]
    data=""
    for i in range(len(file_data)):
        if file_data[i]==['section .data']:
            for j in range(i,len(file_data)):
                if file_data[j]!=['section .bss']:
                    for k in file_data[j]:
                        data_sec=(filter(lambda x: x!='"',k))
 #                   print data_sec
                    data_section.append([data_sec])
                else:
                    for line in range(len(data_section)):
                        data=map(lambda x:x.split(' '),data_section[line])
                        for i in data:
                            section_data.append(i)
#                    pp.pprint(section_data)
                    return section_data
    return 0

def seperate_bss_section(file_data):
    bss_section=[]
    bss_sec=[]
    section_bss=[]
    data=""
    for i in range(len(file_data)):
        if file_data[i]==['section .bss']:
            for j in range(i,len(file_data)):
                if file_data[j]!=['section .text']:
                    for k in file_data[j]:
                        bss_sec=filter(lambda x:x!='"',k)
                    bss_section.append([bss_sec])
                else:
                    for line in range(len(bss_section)):
                        data=map(lambda x:x.split(' '),bss_section[line])
                        for i in data:
                            section_bss.append(i)
                    return section_bss
    return 0



#=====================================================literal function===============================

def text_literal_table(text_section):
    literal_table=[]
    temp=[]
    for line in text_section:
        for i in range(len(line)):
            if line[i].isdigit():
                temp.append(line[i])
                hex_val=hex(int(line[i]))[2:].upper()
                if len(hex_val)==1:
                    hex_val1='0000000'+hex_val
                else:
                    hex_val1='000000'+hex_val
                temp.append(hex_val)
                temp.append(hex_val1)
                literal_table.append(temp)
                temp=[]
    return(literal_table)



def create_literal_hex(literal_hex):
    hex_data=[]
    for i in range(len(literal_hex)):
        hex_literal=filter(lambda x:x!='x',literal_hex[i])
        hex_data.append(hex_literal)
    return hex_data
#===========================================================symbol table===================================================

def search_text_section(text_section):
    symbol=[]
    data_type=[]
    size=[]
    address=[]
    def_undef=[]
    value=[]
    for line in text_section:
        for j in line[0]:
            if j==':':
                symbol.append(filter(lambda x:x!=':',line[0]))
                data_type.append('_')
                value.append('_')
                size.append('_')
                address.append(0)
                def_undef.append('D')
        if line[0]=='global':
            symbol.append(line[0])
            data_type.append(line[1])
            value.append('_')
            size.append('_')
            address.append(0)
            def_undef.append('D')
        if line[0]=='extern':
            symbol.append(line[0])
            data_type.append(line[1])
            value.append('_')
            size.append('_')
            address.append(0)
            def_undef.append('D')
    text_symbol_data=concat_symbol_data(symbol,data_type,value,size,address,def_undef)
    return text_symbol_data

def search_bss_section(bss_section):
    symbol=[]
    data_type=[]
    size=[]
    address=[]
    def_undef=[]
    value=[]
    for line in bss_section:
        symbol.append(line[0])
        data_type.append(line[1])
        value.append('_')
        def_undef.append('D')
        if line[1]=='resd':
            size.append(int(line[2])*4)
        if line[1]=='resb':
            size.append(int(line[2])*1)
        if line[1]=='resq':
            size.append(int(line[2])*2)
        if line[1]=='resw':
            size.append(int(line[2])*8)
    address=find_address(size)
    address=map(lambda x:hex(int(x)),address)
    address=create_literal_hex(address)
    for i in range(len(address)):
        if(len(address[i]))==2:
            address[i]='000000'+address[i]
        else:
            address[i]='00000'+address[i]
    bss_symbol_data=concat_symbol_data(symbol,data_type,value,size,address,def_undef)
    return bss_symbol_data

def search_data_section(data_section):
    line_data=[]
    symbol=[]
    data1=""
    data_type=[]
    value=[]
    def_undef=[]
    size=[]
    cnt=1
    address=[]
    #address.append('00000000')
    for line in data_section:
        symbol.append(line[0])
        data_type.append(line[1])
        data=""
        for i in range(2,len(line)):
            data+=line[i]
            data+=' '
        if line[1]=='db':
            data1=filter(lambda x:x!=',' and x!='1' and x!='0',data)
            data=data1
            size.append(len(data)-1)
        if line[1]=='dd':
            for i in range(len(data)):
                if data[i]==',':
                    cnt+=1
            size.append(4*(cnt))
        value.append(data)
        def_undef.append("D")
    address=find_address(size)
    address=map(lambda x:hex(int(x)),address)
    address=create_literal_hex(address)
    for i in range(len(address)):
        if len(address[i])==2:
            address[i]='000000'+address[i]
        else:
            address[i]='00000'+address[i]
    symbol_data_section=concat_symbol_data(symbol,data_type,value,size,address,def_undef)
    return symbol_data_section
def find_address(size):
    val=0
    address=[0]
    for i in range(len(size)-1):
        val+=size[i]
        address.append(val)
    return address

def concat_symbol_data(symbol,data_type,value,size,address,def_undef):
    symbol_data1=[]
    for i in range(len(size)):
        symbol_data=[i]
        symbol_data.append(symbol[i])
        symbol_data.append(data_type[i])
        symbol_data.append(value[i])
        symbol_data.append(size[i])
        symbol_data.append(address[i])
        symbol_data.append(def_undef[i])
        symbol_data1.append(symbol_data)
    return symbol_data1


def create_symbol_in_dictionary(symbol_data):
    dict1={}
    dict2={}
    dict3={}
    dict4={}
    dict5={}
    dict6={}
    dict7={}
    for i in range(len(symbol_data)):
        dict1[i]=symbol_data[i][0]
        dict2[i]=symbol_data[i][1]
        dict3[i]=symbol_data[i][2]
        dict4[i]=symbol_data[i][3]
        dict5[i]=symbol_data[i][4]
        dict6[i]=symbol_data[i][5]
        dict7[i]=symbol_data[i][6]
        print i,'\t\t',dict1[i],'\t\t',dict2[i],'\t\t',dict3[i],'\t\t',dict4[i],'\t\t',dict5[i],'\t\t',dict6[i],'\t\t',dict7[i]

#============================================================intermediate code=====================================================

def search_symbol(symbol_name):
    for i in range(len(symbol_data)):
        if symbol_data[i][1]==symbol_name:
            return symbol_data[i][0]

def search_immediate(immediate_val):
    for i in range(len(literal_table_main)):
        if literal_table_main[i][0]==immediate_val:
            return literal_table_main[i][0]

def create_intermediate(file_text_data):
    address=0
    intermediate_code=[['_' for i in range(4)]for j in range(len(file_text_data))]
    i=0
    for i in range(len(file_text_data)):
        intermediate_code[i][0]=i
        intermediate_code[i][3]=''.join(list(map(lambda x:x+' ',file_text_data[i])))
        if len(file_text_data[i])>1:
            if file_text_data[i][0]=='mov':
                if file_text_data[i][1] in r32 and file_text_data[i][2] in r32:
                    #print file_text_data[i]
                    opcode_mov=mov_i["r32,r32"]["mov_op"]
                    opcode_mov+=' '+"r32,r32"
                    intermediate_code[i][2]=opcode_mov
                    address+=mov_i["r32,r32"]["size"]
                    intermediate_code[i][1]=address
                elif file_text_data[i][1] in r16 and file_text_data[i][2] in r16:
                    opcode_mov=mov_i["r16,r16"]["mov_op"]
                    opcode_mov+=' '+"r16,r16"
                    intermediate_code[i][2]=opcode_mov
                    address+=mov_i["r16,r16"]["size"]
                    intermediate_code[i][1]=address
                elif file_text_data[i][1] in r32 and check_memory(file_text_data[i][2]):
                    opcode_mov=mov_i["r32,mem"]["mov_op"]
                    if file_text_data[i][2][-1]==']':
                        symbol=search_symbol(file_text_data[i][2][1:-1])
                    else:
                        symbol=search_symbol(file_text_data[i][2])
                    opcode_mem=opcode_mov+' '+'r32,sym'+str(symbol)
                    intermediate_code[i][2]=opcode_mem
                    address+=mov_i["r32,mem"]["size"]
                    intermediate_code[i][1]=address
                elif file_text_data[i][1] in r16 and check_memory(file_text_data[i][2]):
                    opcode_mov=mov_i["r16,mem"]["mov_op"]
                    if file_text_data[i][2][-1]==']':
                        symbol=search_symbol(file_text_data[i][2][1:-1])
                    else:
                        symbol=search_symbol(file_text_data[i][2])
                    opcode_mem=opcode_mov+' '+'r32,sym'+str(symbol)
                    intermediate_code[i][2]=opcode_mem
                    address+=mov_i["r32,mem"]["size"]
                    intermediate_code[i][1]=address
                elif file_text_data[i][1] in r32 and check_immediate(file_text_data[i][2]):
                    opcode_mov=mov_i["r32,imm"]["mov_op"]
                    address+=mov_i["r32,imm"]["size"]
                    intermediate_code[i][1]=address
                    immediate=search_immediate(file_text_data[i][2])
                    opcode=opcode_mov+' '+'r32,imm'+str(immediate)
                    intermediate_code[i][2]=opcode
                elif file_text_data[i][1] in r16 and check_immediate(file_text_data[i][2]):
                    opcode_mov=mov_i["r32,imm"]["mov_op"]
                    address+=mov_i["r32,imm"]["size"]
                    intermediate_code[i][1]=address
                    immediate=search_immediate(file_text_data[i][2])
                    opcode=opcode_mov+' '+'r32,imm'+str(immediate)
                    intermediate_code[i][2]=opcode
            if file_text_data[i][0]=='ret':
                intermediate_code[i][1]=1
                intermediate_code[i][2]='op12'
            if file_text_data[i][0]=='call' and check_memory(file_text_data[i][1]):
                intermediate_code[i][2]='op13'
                intermediate_code[i][1]='sym'+str(search_symbol(file_text_data[i][1]))
            if file_text_data[i][0]=='push' and file_text_data[i][1] in r32:
                intermediate_code[i][1]=1
                intermediate_code[i][2]='op14 r32'
            if file_text_data[i][0]=='push' and check_memory(file_text_data[i][1]):
                intermediate_code[i][1]=5
                intermediate_code[i][1]='op14 sym'+str(search_symbol(file_text_data[i][1]))
            if file_text_data[i][0]=='call' and check_memory(file_text_data[i][1]):
                intermediate_code[i][1]=5
                intermediate_code[i][1]='op15 sym'+str(search_symbol(file_text_data[i][1]))
        else:
            if file_text_data[i][0]=='ret':
                intermediate_code[i][1]=1
                intermediate_code[i][2]='op12'
    return intermediate_code


#===================================================================lst file===========================================



def lst_data_table(data_symbol,program):
    lst_data=[[None for i in range(3)]for j in range(len(data_symbol))]
    for i in range(len(data_symbol)):
        lst_data[i][0]=data_symbol[i][5]
        if data_symbol[i][2]=='db':
            value1=data_symbol[i][3]
            list1=[]
            list1=list(map(lambda x:((hex(ord(x))[2:])) .upper(),value1))
            for j in range(len(list1)):
                if list1[j]=='20':
                    list1[j]='00'
            list1=''.join(list1)
            lst_data[i][1]=list1
            #print list1
        elif data_symbol[i][2]=='dd':
            value1=list(map(lambda x:x,(data_symbol[i][3]).split(',')))
            #print value1
            list1=[]
            list1=(list(map(lambda x:('000000000'+(hex(int(x))[2:])).upper(),value1)))
            list1=''.join(list1)
            lst_data[i][1]=list1
            #print list1
        lst_data[i][2]=''.join(map(lambda x:x+' ',(program[i+1])))
    return lst_data

def lst_bss_table(bss_symbol,data_symbol,program):
    lst_bss=[[None for i in range(3)]for j in range(len(bss_symbol))]
    for i in range(len(bss_symbol)):
        lst_bss[i][0]=bss_symbol[i][5]
        if bss_symbol[i][2]=='resd':
            lst_bss[i][1]='<res 0000000'+hex(int(bss_symbol[i][4]))[2:].upper()+'>'
        elif bss_symbol[i][2]=='resb':
            lst_bss[i][1]='<res 0000000'+hex(int(bss_symbol[i][4]))[2:].upper()+'>'
        lst_bss[i][2]=''.join(map(lambda x:x+' ',(program[len(data_symbol)+i+2])))
    return lst_bss


def check_memory(program_line1):
    #print program_line1
    for i in range(len(symbol_data)):
        #print symbol_data[i],program_line1
        if ((program_line1==symbol_data[i][1]) or (program_line1==('['+symbol_data[i][1]+']')) or (program_line1==('byte['+symbol_data[i][1]+']')) or (program_line1==('dword['+symbol_data[i][1]+']'))):
            return True
    return False

def check_symbol(program_line1):
    for i in range(len(symbol_data)):
        if program_line1==symbol_data[i][1]:
            return True
        else:
            return False
def return_symbol_address(symbol):
    for i in range(len(symbol_data)):
        if symbol==symbol_data[i][1]:
            return symbol_data[i][5]
    return '0'
    print "symbol not defined"

def check_immediate(program_line1):
    if program_line1.isdigit():
        return True
    else:
        False


def find_opcode_mov(program_line):
    if program_line==[]:
        return str(0)
    if program_line[0] in r32 and program_line[1] in r32:
        val0=r32[program_line[0]]
        val1=r32[program_line[1]]
        res=mod[3]+val1+val0
        res1=res[0:4]
        res2=res[4:]
        res1=hex(int(res1,2))[2:].upper()
        res2=hex(int(res2,2))[2:].upper()
        opcode=mov_fix["r32,r32"]["opcode"]
        return opcode+res1+res2
    elif program_line[0] in r16 and program_line[1] in r16:
        val0=r16[program_line[0]]
        val1=r16[program_line[1]]
        res=mod[3]+val1+val0
        res1=res[0:4]
        res2=res[4:]
        res1=hex(int(res1,2))[2:].upper()
        res2=hex(int(res2,2))[2:].upper()
        opcode=mov_fix["r16,r16"]["opcode"]
        return opcode+res1+res2
    elif program_line[0] in r32 and check_memory(program_line[1]):
        if program_line[0]=="eax":
            opcode="A1"
            if program_line[1][0]=='[':
                symbol_address=return_symbol_address(program_line[1][1:-1])
                return opcode+'['+symbol_address+']'
            else:
                symbol_address=return_symbol_address(program_line[1])
                opcode=mov_not_fix["r32,m321"]["opcode"]
                return opcode+'['+symbol_address+']'
        else:
            val0=r32[program_line[0]]
            res=mod[0]+val0+"101"
            res1=res[0:4]
            res2=res[4:]
            res1=hex(int(res1,2))[2:].upper()
            res2=hex(int(res2,2))[2:].upper()
            opcode=mov_fix["r32,m32"]["opcode"]
            if program_line[1][0]=='[':
                address_symbol=return_symbol_address(program_line[1][1:-1])
            else:
                address_symbol=return_symbol_address(program_line[1])
                opcode=mov_not_fix["r32,m321"]["opcode"]
                val0=int(opcode,16)+reg_32[program_line[0]]
                val0=hex(val0)[2:].upper()
                return val0+'['+address_symbol+']'
            return str(opcode+res1+res2)+'['+str(address_symbol)+']'
    elif program_line[0] in r16 and check_memory(program_line[1]):
        if program_line[0]=="ax":
            if program_line[1][0]=='[':
                address_symbol=return_symbol_address(program_line[1][1:-1])
                return '66A1'+'['+address_symbol+']'
            else:
                address_symbol=return_symbol_address(program_line[1])
                address_symbol=address_symbol[len(address_symbol)/2:len(address_symbol)]
                opcode=mov_not_fix["r16,m161"]["opcode"]
                val0=int(opcode,16)+reg_16[program_line[0]]
                val0=hex(val0)[2:].upper()
                return val0+'['+address_symbol+']'
        else:
            val0=r16[program_line[0]]
            res=mod[0]+val0+"101"
            res1=res[0:4]
            res2=res[4:]
            res1=hex(int(res1,2))[2:].upper()
            res2=hex(int(res2,2))[2:].upper()
            opcode=mov_not_fix["r16,m161"]["opcode"]
            if program_line[1][0]=='[':
                address_symbol=return_symbol_address(program_line[1][1:-1])
                opcode=mov_fix["r16,m16"]
                return opcode+res1+res2+'['+address_symbol+']'
            else:
                address_symbol=return_symbol_address(program_line[1])
                address_symbol=address_symbol[(len(address_symbol)/2):len(address_symbol)]
                val0=int(opcode,16)+reg_16[program_line[0]]
                #val0 = int(opcode,16)+int(hex(int(r16[program_line[0]]))[2:],16)
                val0=hex(val0)[2:].upper()
                return val0+'['+address_symbol+']'
    elif program_line[0] in r32 and check_immediate(program_line[1]):
        opcode=mov_not_fix["r32,imm32"]["opcode"]
        hex_val = hex(int(program_line[1]))[2:].upper().zfill(8)
        hex_val=''.join(list(reversed(list(map(lambda x,y:x+y, hex_val[0::2],hex_val[1::2])))))
        val0 = int(hex(int(r32[program_line[0]]))[2:],16)+ int(opcode,16)
        val0=hex(val0)[2:].upper().zfill(2)
        return val0+hex_val


def lst_text_table(text_symbol,program):
    lst_text=[[None for i in range(3)]for j in range((len(program)))]
    val1=0
    for i in range(len(program)):
        check_byte=''
        if len(program[i])>=3:
            lst_text[i][0]=(hex(val1)[2:]).zfill(8).upper()
            if program[i][0]=='mov':
                lst_text[i][1]=find_opcode_mov(program[i][1:])
            if program[i][0]=='add' or 'sub':
                lst_text[i][1]=find_opcode_mov(program[i][1:])
            if program[i][0]=='push':
                if check_memory(program[i][1]):
                    lst_text[i][1]='53'
            check_byte+=lst_text[i][1]
            val=list(filter(lambda x:x=='[',check_byte))
            if val==['[']:
                val1+=(int(len(lst_text[i][1]))/2)-1
            else:
                val1+=int(len(lst_text[i][1]))/2
            lst_text[i][2]=program[i][0]+' '+program[i][1]+','+program[i][2]
        else:
            lst_text[i][0]=0
            lst_text[i][1]=''
            lst_text[i][2]=program[i][0]
    return lst_text

def concat_lst_file(program,lst_data,lst_bss,lst_text):
    lst_file=[]
    lst_file.append(program[0])
    for i in range(len(lst_data)):
        lst_data[i][2]=program[i+1][0]
        lst_file.append(lst_data[i])
    lst_file.append(program[len(lst_data)+1])
    for i in range(len(lst_bss)):
        lst_bss[i][2]=program[len(lst_data)+i+2][0]
        lst_file.append(lst_bss[i])
    length_data_bss=len(lst_file)
    length_text=len(lst_text)
    other_data_length=max(length_text,length_data_bss)-min(length_text,length_data_bss)
    for i in range(4):
        lst_file.append(program[length_data_bss+i])
    length_upto_main=len(lst_file)
    for i in range(len(lst_text)):
        lst_file.append(lst_text[i])
    #max_first_line=[len(lst_file[i][0] for i in range(len(lst_file)))]
    #max_second_line=[len(lst_file[i][1] for i in range(len(lst_file)))]
    #max_third_line=[len(lst_file[i][2] for i in range(len(lst_file)))]
    return lst_file


#===========================================================================================================================

def filter_macro_first_last(file_data_macro1):
    filter_macro=[]
    for line in file_data_macro1:
        if line[0]=='%macro' or line[0]=='%endmacro':
            pass
        else:
            filter_macro.append(line)
    return filter_macro

def add_macro_to_asm(file_data_macro,program):
    for line in file_data_macro:
        program.append(line)


def function_parameter(function_call_reg,dict_parameter):
    for i in range(len(function_call_reg)):
        dict_parameter['%'+str(i+1)]=function_call_reg[i]

def replace_parameter_to_macro_file(program):
    for i in range(len(program)):
        if len(program[i])>2:
            if program[i][2] in dict_parameter:
                program[i][2]=dict_parameter[program[i][2]]




#=============================================================main===============================================================


file_data1=list(filter(lambda x:x!=[''],list(i.strip() for i in open('6202_Que1.asm'))))
file_data_asm=list(filter(lambda x:x!=[''],map(lambda x:re.split(' |,',x),file_data1)))
file_name=file_data_asm[0][0][9:-1]
file_name_asm=["%include"+'"'+file_name+'"']
program1=list(filter(lambda x:x!=file_name_asm,file_data_asm))
file_data_macro=list(filter(lambda x:x!=[''],(list(i.strip() for i in open(file_name)))))
file_data_macro=list(filter(lambda x:x!=[''],map(lambda x:re.split(' |,',x),file_data_macro)))
function_name=file_data_macro[0][1]
function_call_line=((list(filter(lambda x:x[0]==function_name,file_data_asm)))[0])[1:]
dict_parameter={}
function_parameter(function_call_line,dict_parameter)
#print dict_parameter
program1=list(it.takewhile(lambda x:x[0]!=function_name,program1))
list1=((filter(lambda x:x[0]==function_name,file_data_asm)))
program1.append(list1[0])
file_data_macro=filter_macro_first_last(file_data_macro)
add_macro_to_asm(file_data_macro,program1)
program_rem=list(filter(lambda x:x!=list1[0],(list(it.dropwhile(lambda x:x[0]!=function_name,file_data_asm)))))
add_macro_to_asm(program_rem,program1)
replace_parameter_to_macro_file(program1)
#pp.pprint(program)
#======================================================seperate section===========================================
file_data=[[x] for x in file_data1]
#pp.pprint(file_data)
file_data_main=list(filter(lambda x:x!=[''],file_data))
#pp.pprint(file_data[1:])
seperate_data_main=seperate_data_section(file_data_main[1:])
#pp.pprint(seperate_data_main)
seperate_bss_main=seperate_bss_section(file_data_main)
#pp.pprint(seperate_bss_main)
seperate_text_main=list(it.dropwhile(lambda x:x!=['section', '.text'],program1))
#pp.pprint(seperate_text_main)
program_main=seperate_data_main+seperate_bss_main+seperate_text_main
#print program_main
#======================================================literal table=================================================
literal_table_main=text_literal_table(seperate_text_main)
print '\n\n\t\t\tLITERAL TABLE\n'
#pp.pprint(literal_table_main)
for i in literal_table_main:
    print i
#======================================================symbol table======================================================


symbol_data_section_main=search_data_section(seperate_data_main[1:])
#print symbol_data_section_main
symbol_bss_section_main=search_bss_section(seperate_bss_main[1:])
#print symbol_bss_section_main
symbol_text_section_main=search_text_section(seperate_text_main[1:])
#pp.pprint(symbol_text_section_main)
symbol_data=symbol_data_section_main+symbol_bss_section_main+symbol_text_section_main
#symbol_data=concat_symbol_data(symbol_data)
#pp.pprint(symbol_data)
print '\n\n\t\t\tSYMBOL TABLE\n'
create_symbol_in_dictionary(symbol_data)
#==================================================intermediate code==============================
#pp.pprint(seperate_text_main)
intermediate_code=create_intermediate(seperate_text_main)
print '\n\n\t\t\tINTERMEDIATE CODE\n'
pp.pprint(intermediate_code)
#=======================================lst table===========================================
lst_data=lst_data_table(symbol_data_section_main,program_main)
#print lst_data
lst_bss=lst_bss_table(symbol_bss_section_main,symbol_data_section_main,program_main)
#print lst_bss
main_program=list(it.dropwhile(lambda x:x[0]!='main:',seperate_text_main))
#pp.pprint(main_program)
lst_text=lst_text_table(symbol_text_section_main,main_program[1:])
#pp.pprint(lst_text)
length_lst_data=len(lst_data)
length_lst_bss=len(lst_bss)
length_lst_text=len(lst_text)

lst_file_contents=lst_data+lst_bss+lst_text
#pp.pprint(lst_file_contents)
lst_file_data=concat_lst_file(file_data_main,lst_data,lst_bss,lst_text)
print '\n\n\t\t\tLST FILE\n'
pp.pprint(lst_file_data)
#write_in_file(lst_file_data)






