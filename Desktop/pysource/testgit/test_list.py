import pandas as pd
import socket, struct

list1 = [0,1,2,3,4]
list2 = ['a','b','c','d','e']
list3 = []
list3.append(list1)
list3.append(list2)

#pred_df = pd.DataFrame(data=list(pred_proba), columns=['normal','botnet'])
df = pd.DataFrame(columns=['idx','char'])
#df['idx'] = list1
#df['char'] = list2
df['idx'].loc[0] = 1
df['char'].loc[0] = 'a' 
num = socket.inet_ntoa(struct.pack('!L', 181305857))
print(str(num))




#df.to_csv('testlist.csv')