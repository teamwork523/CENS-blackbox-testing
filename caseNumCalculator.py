#!/usr/bin/python

# inputs are two list of number of cases for each argument
# output are:
# 1. total number of valid case
# 2. total number of cases with one invalid argument
# 3. total number of cases with two invalid arguments
# 4. total number of cases

def main(valid_list, invalid_list):
    valid_case = 0
    invalid_one = 0
    invalid_two = 0
    total_case = 0
    
    # valid case
    temp = 1
    for a in valid_list:
        temp = temp * a
    valid_case = valid_case+temp
    
    # invalid case with one invalid argument
    index1 = 0
    for b in invalid_list:
        pop_out = valid_list.pop(index1)
        temp = b
        for c in valid_list:
            temp = temp * c
        invalid_one = invalid_one + temp
        valid_list.insert(index1, pop_out)
        index1 = index1 + 1
    
    # invalid case with two invalid arguments
    index1 = 0
    for d in invalid_list:
        invalid_list.pop(index1)
        pop_out1 = valid_list.pop(index1)
        index2 = index1
        for e in invalid_list[index1:]:
            pop_out2 = valid_list.pop(index2)
            temp = d*e
            for f in valid_list:
                temp = temp * f
            invalid_two = invalid_two + temp
            valid_list.insert(index2, pop_out2)
            index2= index2 + 1
        valid_list.insert(index1, pop_out1)
        invalid_list.insert(index1, d)
        index1 = index1 + 1
        
    # Summary
    print 'Summary Section:'
    print 'Valid cases: {0}'.format(valid_case)
    print 'Invalid cases with one invalid arg: {0}'.format(invalid_one)
    print 'Invalid cases with two invalid args: {0}'.format(invalid_two)
    print 'Total number of cases: {0}'.format(valid_case + invalid_one + invalid_two)
    
if __name__ == "__main__":
    # number of cases per each valid argument
    valid = [1,3,2]
    # number of cases per each invalid argument
    invalid = [4,3,6]
    main(valid, invalid)
    
    
    
