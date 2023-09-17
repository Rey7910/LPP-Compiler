'''
Analizador sintáctico - Lenguaje de Programación LPP
Reinaldo Toledo Leguizamón
Monitoría de Lenguajes de programación
2023-2

'''

import re

EOF = False

class Token():
    
    
    def __init__(self,token,lexem,line,position):
        self.token = token
        self.lexem = lexem
        self.line = line
        self.position = position

class Parser():
    
    prediction_set = set([])
    stack =[]
    LLkTokenContainer=[]
    LL1=True
    error=False
    pars_counter=0
    exp_arith=False
    finishCatchUp=False
    
    EXP_set = set(['tkn_integer','tkn_real','tkn_char','tkn_str','verdadero','falso',
    'id','tkn_opening_bra','tkn_closing_bra','tkn_plus','tkn_div',
    'tkn_times','tkn_minus','tkn_power','div','mod', "tkn_opening_par","tkn_closing_par"])
    
    grammar = {
        'P':[
            ['R','V','F_P','M']
            ],
        'R':[
            ['registro','id','V','fin','registro'],
            ['empty']
            ],
        'V':[
            ['V_1','V'],
            ['empty']
            ],
        'V_1':[
            ['arreglo','tkn_opening_bra','PA','tkn_closing_bra','de','T','id'],
            ['T','id']
            ],
        'PA':[
            ['tkn_integer','PAm'],
            ],
        'PAm':[
            ['tkn_comma','tkn_integer','PAm'],
            ['empty']
            ],
        'T':[
            ['entero'],
            ['real'],
            ['booleano'],
            ['cadena','tkn_opening_bra','tkn_integer','tkn_closing_bra'],
            ['caracter'],
            ['id'],
            ],
        'F_P':[
            ['F','F_P'],
            ['PR','F_P'],
            ['empty']
            ],
        'F':[
            ['funcion','id','PAR','tkn_colon','T','V','inicio','S','retorne','EXP','fin']
            ],
        'PAR':[
            ['tkn_opening_par','V_1','PAR_1','tkn_closing_par'],
            ['empty']
            ],
        'PR':[
            ['procedimiento','id','PARp','V','inicio','S','fin']
            ],
        
        'PARp':[
            ['tkn_opening_par','PARp_1','tkn_closing_par'],
            ['empty']
            ],
        'PARp_1':[
                ['var','V_1','PARp_2'],
                ['V_1','PARp_2']
            ],
        'PARp_2':[
                ['tkn_comma','PARp_1'],
                ['empty']
            ],
        
        'M': [
            ['inicio','S','fin']
            ],
        
        'S':[
             ['L','S'],
             ['CO','S'],
             ['A','S'],
             ['E','S'],
             ['CA','S'],
             ['CAL','S'],
             ['empty'],
            ],
        
        'L':[
                ['mientras','EXP_C','haga','S','fin','mientras'],
                ['repita','S','hasta','EXP_C'],
                ['para','A','hasta','EXP','haga','S','fin','para'],
            ],
        'CO':[
                ['si','EXP_C','entonces','S','CO_1','fin','si']
            ],
        'CO_1':[
                ['sino','si','EXP_C','entonces','S','CO_1','fin', 'si'],
                ['sino','S'],
                ['empty']
            ],
            
        'A':[
                ['id','AC','tkn_assign','EXP'],
        
            ],
        'AC':[
                ['tkn_period','id','AC'],
                ['tkn_opening_bra','EXP','AC_1','tkn_closing_bra'],
                ['empty']
            ],
        
        'AC_1':[
                ['tkn_comma','EXP','AC_1'],
                ['empty']
            ],
        'E':[
                ['escriba','EXP','E_exp'],
                ['lea','id','AC']
            ],
        'E_exp':[
                ['tkn_comma','EXP','E_exp'],
                ['empty']
            ],
        
        'CAL':[
                ['llamar','CAL_ex'],
            ],
        
        'CAL_ex':[
                ['nueva_linea'],
                ['id','ARGS']
            ],
            
        'ARGS':[
                ['tkn_opening_par','EXP','AC_1','tkn_closing_par'],
            ],
        
        'CA':[
                ['caso','id','AC','CA_SEC','tkn_colon','S','CA_OP','fin','caso']
            ],
        
        'CA_OP':[
                ['CA_SEC','tkn_colon','S','CA_OP'],
                ['sino','tkn_colon','S'],
                ['empty']
            ],
            
        'CA_SEC':[
                
                ['VAL','CA_SEC_1']
            ],
        'CA_SEC_1':[
                ['tkn_comma','VAL','CA_SEC_1'],
                ['empty']
            ],
        'VAL':[
                
                ['tkn_integer'],
                ['tkn_real'],
                ['tkn_char'],
                ['tkn_str'],
                ['verdadero'],
                ['falso']
                
            ],
        
        'EXP':[
                ['Te','OP_E'],
                ['tkn_opening_par','EXP','tkn_closing_par'],
            ],
        
        
        
        'OP_E':[
                ['OP_A','EXP'],
                ['empty']
            ],
        
        'Te':[
                ['tkn_minus','Te'],
                ['VAL'],
                ['id','Te_id'],
            ],
        
        'Te_id':[
                
                ['ARGS'],
                ['AC']
            ],
        
        'OP_A':[
                ['tkn_minus'],
                ['tkn_plus'],
                ['tkn_times'],
                ['tkn_power'],
                ['tkn_div'],
                ['div'],
                ['mod']
            ],
        'EXP_C':[
                ['tkn_opening_par','EXP_C','tkn_closing_par','EXP_C_1'],
                ['EXP','OP_R','EXP'],
            ],
        
        'EXP_C_1':[
                ['OP_L','tkn_opening_par','EXP','OP_R','EXP','tkn_closing_par','EXP_C_1'],
                ['empty']
            ],
        'OP_R':[
            ['tkn_equal'],
            ['tkn_less'],
            ['tkn_greater'],
            ['tkn_leq'],
            ['tkn_geq'],
            ['tkn_neq']
        ],
        'OP_L':[
          ['o'],
          ['y']
        ],
        
        
    }
    
    
    
    
    def catchUpLL1(self):
        
        rule_applied=True
        self.finishCatchUp=True
        
        for i in range(len(self.LLkTokenContainer)):
            
            #print("---------------------- Next Token --------------------------")
            #self.showTokenInfo(self.LLkTokenContainer[i])
            #print("Prediction set before the match algorithm",self.prediction_set)
            match=False
            #print("Stack before the match algorithm: ",self.stack)
            
            #print("---------------------- Starting match process----------------------")
            
            while(match==False and self.LL1==True):
                
                if(len(self.stack) < 1):
                    error=True
                    self.reportError(i)
                    break
          
                current_element = self.stack.pop()
                
                
                if(current_element[0].isupper()):
                    
                    current_no_terminal = current_element
                    
                    if(rule_applied==True):
                        
                        if(self.exp_arith==True):
                            rule=self.grammar['EXP_C'][1]
                            self.exp_arith==False
                            rule_applied=False
                        else:
                            rule=self.grammar['EXP_C'][0]
                            rule_applied=False
                    
                    else:
        
                        rule = self.lookForMatchRule(current_no_terminal,self.LLkTokenContainer[i])
                        
                    #print("Rule that must be applied",rule)
                        
                    #print("Updated prediction set: ",self.prediction_set)
                    
                    if(rule=='error'):
                        #print("Error sintáctico")
                        self.error=True
                        self.reportError(token)
                        break
                    else:
                        for j in reversed(rule):
                            
                            if j!="empty":
                                self.stack.append(j)
                        
                        #print("Updated stack: ",self.stack)
                    
                    
                        
                else:
                    
                    self.prediction_set.add(current_element)
                    #print("Symbol parsed")
                    #print(i)
                    #print(self.LLkTokenContainer[i])
                    
                    if(current_element==self.LLkTokenContainer[i].token):
                        match=True
                        #print("*************************** Token matched successfully *******************")
                        self.prediction_set.clear()
                        break
                    else:
                        self.error = True
                        self.reportError(token)
                        break
        
        self.LLkTokenContainer.clear()
            
            
            
            
            
            
    
    
    
    def analize(self,token):
        #print("*************************** Next Token *******************")
        #self.showTokenInfo(token)
        #print("Prediction set before the match algorithm",self.prediction_set)
        match=False
        #print("Stack before the match algorithm: ",self.stack)
        
        #print("******************** Starting match process *******************")
        
        
        if(self.LL1==False):
            
            if(token.token=="tkn_opening_par"):
                self.pars_counter+=1
                self.LLkTokenContainer.append(token)
            
            elif(token.token=="tkn_closing_par"):
                self.pars_counter-=1
                self.LLkTokenContainer.append(token)
                
                if(self.pars_counter==0):
                    self.LL1=True
                    #print("Pars from arithmetic rule")
                    self.exp_arith=True
                    self.catchUpLL1()
                    '''
                    for i in self.LLkTokenContainer:
                        print(i.token,end=",")
                    print() '''
                    
            
            elif token.token in self.EXP_set:
                self.LLkTokenContainer.append(token)
            
            else:
                self.LL1=True
                #print("Pars from conditional rule")
                self.LLkTokenContainer.append(token)
                #print(self.pars_counter)
                
                '''
                for i in self.LLkTokenContainer:
                    print(i.token,end=",")
                print() '''
                
                self.catchUpLL1()
                
            
                
            
        
        
        while(match==False and self.LL1==True and self.finishCatchUp==False):
          
            if(len(self.stack) < 1):
                error=True
                self.reportError(token)
                break
            
            current_element = self.stack.pop()
            
            
            
            
            if(current_element[0].isupper()):
                
                current_no_terminal = current_element
                
                if(current_no_terminal=='EXP_C' and token.token == "tkn_opening_par"):
                    #print("Switch to LL(K)")
                    self.stack.append(current_element)
                    self.pars_counter+=1
                    self.LL1=False
                    self.LLkTokenContainer.append(token)
                    break
            
                #print("Current no terminal rules:",self.grammar[current_no_terminal])
                
                rule = self.lookForMatchRule(current_no_terminal,token)
                
                #print("Rule that must be applied",rule)
                
                #print("Updated prediction set: ",self.prediction_set)
                
                if(rule=='error'):
                    #print("Error sintáctico")
                    self.error=True
                    self.reportError(token)
                    break
                else:
                    for i in reversed(rule):
                        
                        if i!="empty":
                            self.stack.append(i)
                    
                    #print("Updated stack: ",self.stack)
                
                
                    
            else:
                
                self.prediction_set.add(current_element)
                
                if(current_element==token.token):
                    match=True
                    #print("*************************** Token matched successfully *******************")
                    self.prediction_set.clear()
                    break
                else:
                    self.error = True
                    self.reportError(token)
                    break
                
        
        
        self.finishCatchUp=False
    
    
    def lookForMatchRule(self,current_no_terminal,token):
        
        match = 'error'
        
        for i in self.grammar[current_no_terminal]:
            
            if(i[0][0].isupper()):
                possible = self.lookForMatchRule(i[0],token)
                
                #print("Possible match across another rule: "+i[0],possible)
                
                if(possible!='error'):
                    match = i
                    return match
                    break
                
            elif(i[0]=="empty"):
                #current_element=self.stack.pop()
                return i
                break
            
            elif(i[0]==token.token):
                return i
                break
                
            else:
                self.prediction_set.add(i[0])
                
            
        
        if(match == 'error'):
            return match
            
        
    
    def showTokenInfo(self,token):
        print("<"+str(token.token)+","+str(token.lexem)+","+str(token.line)+","+str(token.position)+">")
        
        
    def reportError(self,token):
        
        if token.lexem=='assign':
                token.lexem='<-'
                
        elif token.lexem == 'period':
            token.lexem ='.'
        
        elif token.lexem == 'comma':
            token.lexem=','
            
        elif token.lexem == 'colon':
            token.lexem=':'
        
        elif token.lexem == 'closing_bra':
            token.lexem=']'
        
        elif token.lexem == 'opening_bra':
            token.lexem='['
            
        elif token.lexem == 'closing_par':
            token.lexem=')'
            
        elif token.lexem == 'opening_par':
            token.lexem='('
            
        elif token.lexem == 'plus':
            token.lexem='+'
            
        elif token.lexem == 'minus':
            token.lexem='-'
            
        elif token.lexem == 'times':
            token.lexem='*'
            
        elif token.lexem == 'div':
            token.lexem='/'
            
        elif token.lexem == 'power':
            token.lexem='^'
            
        elif token.lexem == 'equal':
            token.lexem='='
            
        elif token.lexem == 'neq':
            token.lexem='<>'
            
        elif token.lexem == 'less':
            token.lexem='<'
            
        elif token.lexem == 'leq':
            token.lexem='<='
            
        elif token.lexem == 'greater':
            token.lexem='>'
            
        elif token.lexem == 'geq':
            token.lexem ='>='
        
        
        print("<{}:{}> Error sintactico: se encontro \"{}\"; se esperaba:".format(str(token.line),str(token.position),token.lexem),end="")
        
        
        report_prediction_set = list(self.prediction_set)
        
        
        for i in range(len(report_prediction_set)):
            if report_prediction_set[i]=='tkn_integer':
                report_prediction_set[i]='valor_entero'
                
            elif report_prediction_set[i]=='tkn_real':
                report_prediction_set[i]='valor_real'
                
            elif report_prediction_set[i]=='tkn_char':
                report_prediction_set[i]='caracter_simple'
                
            elif report_prediction_set[i]=='tkn_str':
                report_prediction_set[i]='cadena_de_caracteres'
        
        
        report_prediction_set.sort()
        
        
        for i in range(len(report_prediction_set)):
            
            if report_prediction_set[i]=='tkn_assign':
                report_prediction_set[i]='<-'
                
            elif report_prediction_set[i] == 'tkn_period':
                report_prediction_set[i]='.'
            
            elif report_prediction_set[i] == 'tkn_comma':
                report_prediction_set[i]=','
                
            elif report_prediction_set[i] == 'tkn_colon':
                report_prediction_set[i]=':'
            
            elif report_prediction_set[i] == 'tkn_closing_bra':
                report_prediction_set[i]=']'
            
            elif report_prediction_set[i] == 'tkn_opening_bra':
                report_prediction_set[i]='['
                
            elif report_prediction_set[i] == 'tkn_closing_par':
                report_prediction_set[i]=')'
                
            elif report_prediction_set[i] == 'tkn_opening_par':
                report_prediction_set[i]='('
                
            elif report_prediction_set[i] == 'tkn_plus':
                report_prediction_set[i]='+'
                
            elif report_prediction_set[i] == 'tkn_minus':
                report_prediction_set[i]='-'
                
            elif report_prediction_set[i] == 'tkn_times':
                report_prediction_set[i]='*'
                
            elif report_prediction_set[i] == 'tkn_div':
                report_prediction_set[i]='/'
                
            elif report_prediction_set[i] == 'tkn_power':
                report_prediction_set[i]='^'
                
            elif report_prediction_set[i] == 'tkn_equal':
                report_prediction_set[i]='='
                
            elif report_prediction_set[i] == 'tkn_neq':
                report_prediction_set[i]='<>'
                
            elif report_prediction_set[i] == 'tkn_less':
                report_prediction_set[i]='<'
                
            elif report_prediction_set[i] == 'tkn_leq':
                report_prediction_set[i]='<='
                
            elif report_prediction_set[i] == 'tkn_greater':
                report_prediction_set[i]='>'
                
            elif report_prediction_set[i] == 'tkn_geq':
                report_prediction_set[i]='>='
        
        if(len(report_prediction_set)==0):
            report_prediction_set.append('final de archivo')
        
        for i in range(len(report_prediction_set)):
            print(" \"{}\"".format(report_prediction_set[i]),end="")
            
            if(i!=len(report_prediction_set)-1):
                print(",",end="")
            else:
                print(".",end="")

class Lexer():
    
    error=False
    block_comment=False
    block_comment_line=0
    block_comment_position=0
    
    regex_dict={
    'arreglo':r'\barreglo\b(?![\w_])',
    'booleano':r'\bbooleano\b(?![\w_])',
    'cadena':r'\bcadena\b(?![\w_])',
    'caracter':r'\bcaracter\b(?![\w_])',
    'caso':r'\bcaso\b(?![\w_])',
    'de':r'\bde\b(?![\w_])',
    'div':r'\bdiv\b(?![\w_])',
    'entero':r'\bentero\b(?![\w_])',
    'entonces':r'\bentonces\b(?![\w_])',
    'escriba':r'\bescriba\b(?![\w_])',
    'falso':r'\bfalso\b(?![\w_])',
    'fin':r'\bfin\b(?![\w_])',
    'funcion':r'\bfuncion\b(?![\w_])',
    'haga':r'\bhaga\b(?![\w_])',
    'hasta':r'\bhasta\b(?![\w_])',
    'inicio':r'\binicio\b(?![\w_])',
    'lea':r'\blea\b(?![\w_])',
    'llamar':r'\bllamar\b(?![\w_])',
    'mientras':r'\bmientras\b(?![\w_])',
    'mod':r'\bmod\b(?![\w_])',
    'nueva_linea':r'\bnueva_linea\b(?![\w_])',
    'o':r'\bo\b(?![\w_])',
    'para':r'\bpara\b(?![\w_])',
    'procedimiento':r'\bprocedimiento\b(?![\w_])',
    'real':r'\breal\b(?![\w_])',
    'registro':r'\bregistro\b(?![\w_])',
    'repita':r'\brepita\b(?![\w_])',
    'retorne':r'\bretorne\b(?![\w_])',
    'si':r'\bsi\b(?![\w_])',
    'sino':r'\bsino\b(?![\w_])',
    'var':r'\bvar\b(?![\w_])',
    'verdadero':r'\bverdadero\b(?![\w_])',
    'y':r'\by\b(?![\w_])',
    }
    
    
    symbols_regex_dict = {
        'assign':r'<-',
        'period':r'\.',
        'comma':r',',
        'colon':r':',
        'closing_bra':r'\]',
        'opening_bra':r'\[',
        'closing_par':r'\)',
        'opening_par':r'\(',
        'plus':r'\+',
        'minus':r'\-',
        'times':r'\*',
        'div':r'/',
        'power':r'\^',
        'equal':r'=',
        'neq':r'<>',
        'leq':r'<=',
        'geq':r'>=',
        'greater':r'>',
        'less':r'<',
    }
    
    def __init__(self,parser):
        
        self.parser = parser
    
    def match_symbol(self,code,line,end_index,position):
        
        found=False
        
        for key in self.symbols_regex_dict:
            
            #print("the code: ",code ,"; and the regex: ",self.symbols_regex_dict[key])
            #print(key,": ",re.match(self.symbols_regex_dict[key],code))
            
           
            if re.match(self.symbols_regex_dict[key], code) != None:

                self.report_token("tkn_"+key,key,line,position+1,True)
                end_index = re.match(self.symbols_regex_dict[key], code).end()
                position+=end_index
                found=True
                break
        
        if(found==False):
            self.report_error(line,position+1)
        
        return end_index
    
    def match_string(self,code,line,end_index,position):
        
        string_match = r'\"(.*?)\"'
        
        if re.match(string_match, code, re.IGNORECASE) != None:
            self.report_token('tkn_str',re.match(string_match, code).group().replace('\"',''),line,position+1,False)
            end_index = re.match(string_match, code).end()
            position+=end_index
        
        else:
            self.report_error(line,position+1)
        
        return end_index
        
    def match_number(self,code,line,end_index,position):
        
        real_match = r'[0-9]+\.[0-9]+'
        integer_match = r'[0-9]+'
        
        if re.match(real_match, code) != None:
            self.report_token('tkn_real',re.match(real_match, code).group(),line,position+1,False)
            end_index = re.match(real_match, code).end()
            position+=end_index
        
        elif re.match(integer_match, code) != None:
            self.report_token('tkn_integer',re.match(integer_match, code).group(),line,position+1,False)
            end_index = re.match(integer_match, code).end()
            position+=end_index
        
        return end_index
    
    def match_char(self,code,line,end_index,position):
        
        char_match = r'\'(.?)\''
        
        if re.match(char_match, code, re.IGNORECASE) != None:
            self.report_token('tkn_char',re.match(char_match, code).group().replace('\'',''),line,position+1,False)
            end_index = re.match(char_match, code).end()
            position+=end_index
        else:
            self.report_error(line,position+1)
        
        return end_index
        
    
    
    def match_id(self,code,line,end_index,position):
        
        # Match the id
        
        id_match = r'[a-zA-Z_][0-9a-zA-Z_]*'
        
        if re.match(id_match, code, re.IGNORECASE) != None:
            self.report_token('id',re.match(id_match, code, re.IGNORECASE).group().lower(),line,position+1,False)
            end_index = re.match(id_match, code, re.IGNORECASE).end()
            position+=end_index
        
        return end_index

    
    def match_keywords(self,code,line,end_index,position):
        
        # Match the key words 
        found=False
            
        for key in self.regex_dict:
            
            if re.match(self.regex_dict[key], code, re.IGNORECASE) != None:

                self.report_token(key,key,line,position+1,True)
                end_index = re.match(self.regex_dict[key], code, re.IGNORECASE).end()
                position+=end_index
                found=True
                break
        
        # Match the ids that start with any letter and those who were not recognized as key words
        if(found==False):
            end_index=self.match_id(code,line,end_index,position)
        
        return end_index
            
    

    def analize(self,code,line):
        end_index=0
        single_line_comment=False
        line_size=len(code)
        position=0
        end_of_line=False
        
        while(line_size>0):
            
            i=0
        
            while(code[i]==' '):
                
                i+=1;
                position+=1;
                if(i==len(code)):
                    break
            
            code = code[i:]
            
            if(len(code)==0):
                break
            
            # Matching comments of single line denoted by //
            if(len(code)>=2 and code[0]=='/'):
                if(code[1]=='/'):
                    break
                elif(code[1]=='*'):
                    # Match block comment
                    self.block_comment=True
                    self.block_comment_line=line
                    self.block_comment_position=position
                    code = code[2:]
                    position+=2
                    
            if(len(code)>=2 and code[0]=='*'):
                # Close block comment
                if(code[1]=='/'):
                    self.block_comment=False
                    self.block_comment_line=0
                    self.block_comment_position=0
                    code = code[2:]
                    position+=2
                    i=0
                    
                    if(len(code)>0):
                    #Recover the next char different to a blank space
                        while(code[i]==' '):
                            i+=1;
                            position+=1;
                            if(i==len(code)):
                                break
                        code = code[i:]
            
            if(len(code)==0):
                break
                    
            
            #print("Code by this iteration: ",code)
            if(self.block_comment==False):
                # Match the keywords 
                if(re.match(r'[a-zA-Z]',code[0],re.IGNORECASE)!=None):
                    end_index = self.match_keywords(code,line,end_index,position) #could be commented
                
                # Match the ids that start with _ 
                elif(code[0]=='_'):
                    end_index = self.match_id(code,line,end_index,position) #could be commented
                
                elif(code[0]=='\''):
                    end_index= self.match_char(code,line,end_index,position)
                
                elif(code[0]=='\"'):
                    end_index = self.match_string(code,line,end_index,position)
                    
                elif(re.match(r'[0-9]',code[0])!=None):
                    end_index= self.match_number(code,line,end_index,position)
                
                else:
                    end_index = self.match_symbol(code,line,end_index,position)
                
                position+=end_index
            
            else:
                end_index=1
                position+=1
            
            if(self.error==True):
                break
            
            if(self.parser.error == True):
                break
            
            code = code[end_index:]
            
            #print("Code by this iteration: ",code)
            
            line_size=len(code)
            
            if(len(code)==0):
                break
            
    def report_token(self,token,lexem,line,position,key_word):
        
        '''
        
        if(key_word):
            print("<{},{},{}>".format(token,line,position))
        else:
            print("<{},{},{},{}>".format(token,lexem,line,position)) '''
        
        current_token = Token(token,lexem,line,position)
        
        self.parser.analize(current_token)
    
    def report_error(self,line,position):
        self.error=True
        print(">>> Error lexico (linea: {}, posicion: {})".format(line,position))
        

try:
    line=1
    Lpp_parser = Parser()
    Lpp_parser.stack.append('P')
    Lpp_lexer = Lexer(Lpp_parser)
    while True:
        current_line = input()
        Lpp_lexer.analize(current_line,line)
        
        if(Lpp_lexer.error==True):
            break
        
        if(Lpp_lexer.parser.error==True):
            
            #print("Error sintáctico")
            #print("Se esperaba: ",Lpp_lexer.parser.prediction_set)
            break
        line+=1
        
except EOFError:
    EOF=True
    #print("Parser stack after EOF found: ",Lpp_lexer.parser.stack)
    if(EOF==True and Lpp_lexer.block_comment==True):
        Lpp_lexer.report_error(Lpp_lexer.block_comment_line,Lpp_lexer.block_comment_position+1)
    
    if(EOF==True and len(Lpp_lexer.parser.stack)>0):
        #print("Error sintáctico en final de archivo")
        
        EOF_tkn= Token('EOF','EOF',100,100)
        
        Lpp_lexer.parser.analize(EOF_tkn)