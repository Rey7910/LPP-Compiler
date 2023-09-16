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
    error=False
    
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
    }
    
    def analize(self,token):
        print("*************************** Next Token *******************")
        self.showTokenInfo(token)
        print("Prediction set before the match algorithm",self.prediction_set)
        match=False
        print("Stack before the match algorithm: ",self.stack)
        
        print("******************** Starting match process *******************")
        
        while(match==False):
          
            current_element = self.stack.pop()
            
            if(current_element[0].isupper()):
                
                current_no_terminal = current_element
            
                #print("Current no terminal rules:",self.grammar[current_no_terminal])
                
                rule = self.lookForMatchRule(current_no_terminal,token)
                    
                #print("Updated prediction set: ",self.prediction_set)
                
                if(rule=='error'):
                    #print("Error sintáctico")
                    self.error=True
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
                    print("*************************** Token matched successfully *******************")
                    self.prediction_set.clear()
                    break
                else:
                    self.error = True
                    break
    
    
    def lookForMatchRule(self,current_no_terminal,token):
        
        match = 'error'
        
        for i in self.grammar[current_no_terminal]:
            
            if(i[0][0].isupper()):
                possible = self.lookForMatchRule(i[0],token)
                
                #print("Possible match across another rule: ",possible)
                
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
        print("<"+token.token+","+token.lexem+","+str(token.line)+","+str(token.position)+">")


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
        
        id_match = r'[a-zA-Z_][\w_]*'
        
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
            print("Error sintáctico")
            print("Se esperaba: ",Lpp_lexer.parser.prediction_set)
        line+=1
        
except EOFError:
    EOF=True
    
    if(EOF==True and Lpp_lexer.block_comment==True):
        Lpp_lexer.report_error(Lpp_lexer.block_comment_line,Lpp_lexer.block_comment_position+1)
