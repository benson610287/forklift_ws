import os 
import os.path 

# UI���辣���銁��頝臬��
dir = './'  

# ��堒枂�𤌍��銝讠�����缷i���辣
def listUiFile(): 
	list = []
	files = os.listdir(dir)  
	for filename in files:  
		#print( dir + os.sep + f  )
		#print(filename)
		if os.path.splitext(filename)[1] == '.ui':
			list.append(filename)
	
	return list

# ��𠰴�𡒊�銝滾i�����辣�㺿��𣂼�𡒊�銝歉y�����辣���	
def transPyFile(filename): 
	return os.path.splitext(filename)[0] + '.py' 

# 隤輻鍂蝟餌�笔𦶢隞斗��ui頧㗇�𥟇�醩y
def runMain():
	list = listUiFile()
	for uifile in list :
		pyfile = transPyFile(uifile)
		cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile,uifile=uifile)  
		#print(cmd)
		os.system(cmd)

###### 蝔见�讐�銝餃�亙藁		
if __name__ == "__main__":  	
	runMain()