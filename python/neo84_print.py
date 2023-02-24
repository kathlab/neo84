def nprint(message, new_line='\n', add_pre_lf=False):
    if (add_pre_lf):
        print('')
        
    print('neo84 ::', message, end=new_line)

def sprint(message, new_line='\n'):
    print(message, end=new_line)