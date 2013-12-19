'''
把-1节点全部删掉,为聚类做准备
'''

def clean(filename):
    try:
        email = open(filename, 'rt')
    except:
        print('no such file')
    
    with open('cleaned_email_5.txt', 'wt') as ce:
        for line in email:
            fromNode, toNode = line.split() 
            if int(toNode) > 0:
                ce.write(fromNode + '\t' + toNode + '\n')
    
    email.close()


if __name__ == '__main__':
    clean(filename='new_Email-EuAll_5.txt')