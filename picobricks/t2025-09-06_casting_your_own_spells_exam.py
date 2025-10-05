def add_two_numbers(a,b):
    sum = a + b
    return sum

# print(add_two_numbers(3,3))

def has_list_negative(array):
    for value in array:
        if value < 0:
            return True
        
    return False

print('has_list_negative first ', has_list_negative([9,8,6,5,7,100,0,2,1000,150,190,1098,1960,-10]))
print('has_list_negative second ', has_list_negative([1]))

def test_return(number):
    print(number)
    

test_return(10000000000000000)

                
              
                   
            
                
                