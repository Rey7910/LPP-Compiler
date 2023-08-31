import re

EOF = False

class Lexer():
    
    regex_dict={'escriba':r'\bescriba\b(?![\w_])'}
    
    def regex_match(self,code):
        print("a")
    
    def analize(self,code):
        
        line_size=len(code)
        position=0
        
        while(line_size>0):
            
            i=0
            while(code[i]==' '):
                i+=1;
                position+=1;
            
            code = code[i:]
            
            
            if re.match(self.regex_dict['escriba'], code, re.IGNORECASE) != None:

                print("Found position: ",position+1)
                end_index = re.match(self.regex_dict['escriba'], code, re.IGNORECASE).end()
                position+=end_index
            
            #print("Analyzer in position: ",position)
        
            code = code[end_index:]
            #print("Code in iteration: ",code)
            line_size=len(code)
    
    
    
    def report_token(token,lexem,line,column):
        print("xd")
    
    
        


try:
    line=1
    Lpp_lexer = Lexer()
    while True:
        current_line = input()
        #print(entrada)
        Lpp_lexer.analize(current_line)
        line+=1
        
except EOFError:
    EOF=True

