import sys
from typing import Dict
from .getch import getch



class EditMenu:

    def __init__(self,source_dict:Dict)->None:
        self.source_dictionary = source_dict
    
        self.mod_source_dictionary = {}
        self.key = 0
        maxlen = 0
        for key in self.source_dictionary.keys():
            if len(key)>maxlen:
                maxlen = len(key)

        for key,value in self.source_dictionary.items():
            if len(key)< maxlen:
                key= key+" "*(maxlen-len(key))
            self.mod_source_dictionary[key]=value
            
        self.dict_list = [[key,value] for key,value in self.mod_source_dictionary.items()]
        self.current_row = len(self.dict_list) -1
        

    def detect_arrow_keys(self):
        getch()
        c=getch()
        if c=='A':
            return True
        elif c=='B':
            return False
        else:
            pass


    def move_cursor_in_row(self,previous_row):
        current_row_length = len(self.dict_list[self.current_row][0])+len(self.dict_list[self.current_row][1])+3
        previous_row_length = len(self.dict_list[previous_row][0])+len(self.dict_list[previous_row][1])+3
        if current_row_length>previous_row_length:
            difference  = current_row_length-previous_row_length
            sys.stdout.write(f"\033[{difference}C")
            sys.stdout.flush()
        elif current_row_length<previous_row_length:
            difference  = previous_row_length-current_row_length
            sys.stdout.write(f"\033[{difference}D")
            sys.stdout.flush()
        else:
            pass
    
    def menu(self)->Dict:
        for key,value in self.mod_source_dictionary.items():
            print(f"{key} : \033[90m{value}\033[0m")
        length = len(self.dict_list[len(self.dict_list)-1][0])+len(self.dict_list[len(self.dict_list)-1][1])+3
        sys.stdout.write(f"\033[{length}C")
        sys.stdout.flush()
        sys.stdout.write(f"\033[A")
        sys.stdout.flush()   
   
        while True:
            c = getch()
            if c=='\x1b':
                getch()
                arrow_letter = getch()
                if arrow_letter == 'A' and self.current_row>0:
                    sys.stdout.write("\033[A")
                    sys.stdout.flush()
                    self.current_row-=1
                    self.move_cursor_in_row(self.current_row+1)
                    continue
                elif arrow_letter =='B'and self.current_row<len(self.dict_list)-1:
                    sys.stdout.write("\033[B")
                    sys.stdout.flush()
                    self.current_row+=1
                    self.move_cursor_in_row(self.current_row-1)
                    continue
                else:
                    continue
            self.key =c

            if ord(self.key)==127 and len(self.dict_list[self.current_row][1])>0:
                sys.stdout.write('\033[D')
                sys.stdout.flush()
                sys.stdout.write('\033[0K')
                sys.stdout.flush()
                self.dict_list[self.current_row][1] = self.dict_list[self.current_row][1][:-1]
                
                


            elif self.key.isalnum() or self.key in [' ','_','.','-','@','!','#','$']:
                sys.stdout.write(c)
                sys.stdout.flush()
                self.dict_list[self.current_row][1] = self.dict_list[self.current_row][1]+self.key

            elif self.key=='\r':
                while self.current_row<len(self.dict_list)-1:
                    sys.stdout.write("\033[B")
                    sys.stdout.flush()
                    self.current_row+=1
                sys.stdout.write("\033[B\n")
                sys.stdout.flush()
                self.dict_list=[(key.strip(),value) for key,value in self.dict_list]
                return dict(self.dict_list)
            else:
                pass


