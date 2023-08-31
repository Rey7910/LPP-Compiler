import re

EOF = False

class Lexer():
    
    
    regex_dict={
    'arreglo':r'\barreglo\b(?![\w_])',
    'booleano':r'\bbooleano\b(?![\w_])',
    'cadena':r'\bcadena\b(?![\w_])',
    'caracter':r'\bcaracter\b(?![\w_])',
    'caso':r'\bcaso\b(?![\w_])',
    'de':r'\bde\b(?![\w_])',
    'div':r'\bdiv\b(?![\w_])',
    'entero':r'\bentero\b(?![\w_])',
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
    
    def match_keywords(self,code,line,end_index,position):
            
        for key in self.regex_dict:
            
            if re.match(self.regex_dict[key], code, re.IGNORECASE) != None:

                self.report_token(key,key,line,position+1,True)
                end_index = re.match(self.regex_dict[key], code, re.IGNORECASE).end()
                position+=end_index
                break
        
        return end_index
            
    

    def analize(self,code,line):
        end_index=0
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
            
            end_index = self.match_keywords(code,line,end_index,position) #could be commented
            position+=end_index
            
            code = code[end_index:]
            line_size=len(code)
            
    def report_token(self,token,lexem,line,position,key_word):
        
        if(key_word):
            print("<{},{},{}>".format(token,line,position))
        else:
            print("<{},{},{},{}>".format(token,lexem,line,position))
    
    
        


try:
    line=1
    Lpp_lexer = Lexer()
    while True:
        current_line = input()
        Lpp_lexer.analize(current_line,line)
        line+=1
        
except EOFError:
    EOF=True

