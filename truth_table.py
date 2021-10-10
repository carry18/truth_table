import re
import os

def sys_check(origin=""):
    """Check whether this is the right input"""
    chara = []
    tar = ("&", "/", ">", "<", "^")
    chara.append(origin.count("("))
    chara.append(origin.count(")"))
    # violate input requirement
    violate = re.compile(r'[^A-Za-z&/~>=()^]')

    # bracket error
    bracket = re.compile(r'\)\(')  # )(

    # grammar error
    ope = re.compile(r'''[&/>=^]{2,}| # operator multiple
    \w{2,}|                         # proposition multiple
    [&/~>\^]\)|                     # operator)
    \([&/>\^]|                      # (operator
    \)[A-Za-z]|                     # )proposition
    [A-Za-z]\(                      # proposition(
    ''', re.VERBOSE)

    if not origin:
        print("Nothing")
        return False
    elif violate.search(origin):
        print("Illegal input")
        return False
    elif chara[0] != chara[1] or bracket.search(origin):
        print("Bracket error")
        return False
    elif ope.search(origin):
        print("Operator error1")
        return False
    elif origin.startswith(tar) or origin.endswith(tar + ('~',)):
        print("Operator error2")
        return False
    else:
        return True


def cum(char1,char2):
    if int(char1)+int(char2)!=2:
        return '0'
    else:
        return '1'

def may(char1,char2):
    if int(char1)+int(char2)!=0:
        return '1'
    else:
        return '0'

def get(char1,char2):
    if char1 == '0' and char2 == '1':
        return '0'
    else:
        return '1'

def equal(char1,char2):
    if char1!=char2:
        return '0'
    else:
        return '1'

def antimay(char1,char2):
    if char1 != char2:
        return '1'
    else:
        return '0'

def no(char1):
    if char1 == '0':
        return '1'
    else:
        return '0'

#loop control
while True:
    condition=input("Please enter 1 to start the program or 0 to close the program:")
    if condition == '0':
        quit()
    elif condition != '1':
        continue
    else:
        # input module
        value=0
        while not value:
            notes='''Rules to use this truth table
            1. Use "&" "/" "~" ">" "=" "^"to replace "∧" "∨" "¬" "→" "⇔"and "⊕"(xor) respectively;
            2. Make sure use the character in English form instead of Chinese version;
            3. Upper case will be recognized as lower case. Therefore the maximum proposition is 26;
            4. The higher level bracket should contain no more than 37 lower level bracket
                eg: (()()()) contains 3 inner lower level brackets
            '''
            print(notes)
            while True:
                switch=input("Please choose the mode you want to use(1 stands for infix; 0 stands for suffix; q stands for quit): ")
                if switch != '1' and switch != '0' and switch != 'q':
                    continue
                elif switch == 'q':
                    quit()
                else:
                    origin=input("Please enter formula to be calculated:")
                    break
            # count module
            origin=origin.lower()
            chara = []
            chara_print = []
            for i in range(97, 123, 1):
                if origin.count(chr(i)) != 0:
                    chara.append([i, origin.count(chr(i))])
                    chara_print.append(chr(i))
            flag = 0
            if switch == '1':
                if not sys_check(origin):
                    continue
                else:
                    # sub module
                    rep=re.compile('~~')
                    origin=rep.sub('',origin)
                    #print(origin)

                    # Bracket output module
                    left_bracket,right_bracket='(',')'
                    left_index,right_index=[],[]
                    ori_list=list(origin)
                    count=0
                    for i in range(len(ori_list)):
                        count+=1
                        if ori_list[count-1] ==left_bracket:
                            left_index.append(count-1)
                        elif ori_list[count-1]==right_bracket:
                            right_index.append(count-1)
                    #print(left_index,right_index)
                    if  left_index:
                        flag=2
                    else:
                        flag=1


                    # class module
                    if flag==2:
                        contain=[]
                        num=0
                        cls=1
                        for i in right_index:
                            num+=1
                            if num<2:
                                for j in reversed(left_index):
                                    if j<i:
                                        pair=[]
                                        pair.append(j)
                                        pair.append(i)
                                        pair.append(cls)
                                        pair.append(0)
                                        contain.append(pair)
                                        left_index.remove(j)
                                        break
                            else:
                                for j in reversed(left_index):
                                    if j<i:
                                        pair = []
                                        pair.append(j)
                                        pair.append(i)
                                        if j>contain[len(contain)-1][0]:
                                            pair.append(1)
                                            pair.append(0)
                                        else:
                                            for k in range(len(contain)):
                                                if j < contain[k][0]:
                                                    for s in range(k,len(contain)):
                                                        max=0
                                                        if contain[s][2]>max:
                                                            max=contain[s][2]
                                                    cls=max+1
                                                    count=len(contain)-k
                                                    pair.append(cls)
                                                    pair.append(count)
                                                    break
                                        left_index.remove(j)
                                        contain.append(pair)
                                        break
                        #print(contain)

                        #slicing module
                        slice=[]
                        for i in contain:
                            slice.append(origin[i[0]+1:i[1]])
                        #print(slice)

                        # anti-boland module
                        '''bracket portion'''
                        subt = []
                        for i in range(len(slice)):
                            if contain[i][2]==1:
                                swap=0
                                repl=slice[i]
                                for k in range(len(slice[i])):
                                    if swap != 0:
                                        swap-=1
                                        continue
                                    else:
                                        if slice[i][k].isalpha():
                                            swap=0
                                            continue
                                        else:
                                            o=k
                                            if k!=0 and slice[i][k+1] =='~':
                                                o=k+1
                                            temp=slice[i][o+1]
                                            repl=repl.replace(slice[i][o+1],slice[i][k])
                                            repl=list(repl)
                                            repl[k]=temp
                                            repl=''.join(repl)
                                            swap=1+o-k
                            else:
                                skip=0
                                ind,fin,fin_ch=list(range(contain[i][3])),[],[]
                                #print(ind)
                                for n in ind:
                                    if skip!=0:
                                        skip-=1
                                    else:
                                        fin.append(n)
                                        fin_ch.append(chr(n))
                                        if contain[i-n-1][3] == 0:
                                            continue
                                        else:
                                            skip=contain[i-n-1][3]
                                repl=slice[i]
                                for n in fin:
                                    repl = repl.replace(origin[contain[i-1-n][0]:contain[i-1-n][1]+1],chr(n))
                                    #print(repl)
                                swap=0
                                for m in range(len(repl)):
                                    #print(f'm={m}')
                                    #print(f'repl={repl}')
                                    repl = list(repl)
                                    if swap != 0:
                                        swap-=1
                                        continue
                                    else:
                                        if repl[m].isalpha() or repl[m] in fin_ch:
                                            swap=0
                                            continue
                                        else:
                                            o=m
                                            if m!=0 and repl[m+1] == '~':
                                                o=m+1
                                            #print(m,repl[m])
                                            temp = repl[o+1]
                                            #print(temp)
                                            repl[o+1] = repl[m]
                                            #print(repl)
                                            repl[m] = temp
                                            #print(repl)
                                            swap=1+o-m
                                repl = ''.join(repl)
                                for n in fin:
                                    #print(n,subt[i-1-n])
                                    repl = repl.replace(chr(n),subt[i-1-n])
                                    #print(repl)
                            subt.append(repl)
                            #print(subt)

                        '''conjunction portion'''
                        '''find useful bracket'''
                        con,con_ch = [],[]
                        skip=0
                        for s in reversed(range(len(subt))):
                            if skip != 0:
                                skip -= 1
                            else:
                                con.append(s)
                                con_ch.append(chr(s))
                                if contain[s][3] == 0:
                                    continue
                                else:
                                    skip = contain[s][3]
                        #print(con)

                        '''replace bracket with character'''
                        for p in con:
                            origin = origin.replace(origin[contain[p][0]:contain[p][1] + 1], chr(p))
                            #print(origin)

                        '''swap location between operator and proposition'''
                        for l in range(len(origin)):
                            origin=list(origin)
                            if swap != 0:
                                swap -=1
                                continue
                            else:
                                if origin[l].isalpha() or origin[l] in con_ch:
                                    swap = 0
                                    continue
                                else:
                                    o=l
                                    if l!=0 and origin[l+1]=='~':
                                        o=l+1
                                    temp = origin[o + 1]
                                    origin[o+1] = origin[l]
                                    origin[l] = temp
                                    swap = 1+o-l
                        origin = ''.join(origin)
                        for n in con:
                            #print(chr(n),subt[n])
                            origin = origin.replace(chr(n),subt[n])
                            #print(origin)
            try:
                # calculate module
                '''print portion'''
                if flag == 0:
                    ori_list = list(origin)
                print('  '.join(chara_print)+'  '+''.join(ori_list))
                operator = '&/~>=^'

                '''run portion'''
                for i in range(2**len(chara)):
                    bi=list(bin(i).replace('0b','').rjust(len(chara),'0'))
                    new=origin
                    for i in range(len(chara)):
                        confer=re.compile(chr(chara[i][0]))
                        new=confer.sub(bi[i],new)
                    #print(new)
                    if flag==1:
                        neg_zero,neg_one=re.compile(r'~0'),re.compile(r'~1')
                        new=neg_zero.sub('1',new)
                        new=neg_one.sub('0',new)
                        while len(new)!=1:
                            if new[1]=='&':
                                tak=cum(new[0],new[2])
                            elif new[1]=='/':
                                tak=may(new[0], new[2])
                            elif new[1]=='>':
                                tak=get(new[0], new[2])
                            elif new[1]=='=':
                                tak=equal(new[0],new[2])
                            else:
                                tak=antimay(new[0], new[2])
                            new=new.replace(new[0]+new[1]+new[2],tak)
                        #print(new)
                    else:
                        new=list(new)
                        while len(new)!=1:
                            for v in range(len(new)):
                                #print(new)
                                if new[v] in operator:
                                    resolution=2
                                    if  new[v] == operator[0]:
                                        res=cum(new[v-1],new[v-2])
                                    elif new[v] == operator[1]:
                                        res=may(new[v - 1], new[v - 2])
                                    elif new[v] == operator[3]:
                                        res=get(new[v - 1], new[v - 2])
                                    elif new[v] == operator[4]:
                                        res= equal(new[v - 1], new[v - 2])
                                    elif new[v] == operator[5]:
                                        res=antimay(new[v - 1], new[v - 2])
                                    else:
                                        resolution=1
                                        res=no(new[v-1])
                                    if resolution == 1:
                                        new.insert(v-1,res)
                                        del new[v]
                                        del new[v]
                                    else:
                                        new.insert(v-2,res)
                                        del new[v-1]
                                        del new[v-1]
                                        del new[v-1]
                                    break
                        #print(new)
                    space=' '*(len(ori_list)//2+2)
                    bi_print='  '.join(bi)
                    print(bi_print+space+new[0])
                os.system('pause')
            except ValueError:
                print('Please enter correctly!')
                os.system('pause')
                continue
