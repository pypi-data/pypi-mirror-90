class hide_n_seek:
    def __init__(self,data_file_name_with_ext,password):
        self.file = data_file_name_with_ext
        self.sep = b'|'+bytes(password.encode())+b'|'
        
    def self_read(self):
        with open(self.file,'rb') as rb:
            return rb.read()
        
    def read_file(self,filein):
        with open(filein,'rb') as rb:
            return rb.read()
        
    def file_writer(self,data,method):
        with open(self.file,method) as ra:
            ra.write(data)
            
    def add_file(self,filein):
        self.file_writer(self.read_file(filein),'ab')
        self.file_writer(self.sep,'ab')
        self.file_writer(bytes(filein.split('\\')[-1].encode()),'ab')
        self.file_writer(self.sep,'ab')
        print('[+]Done[+]')
        
    def files_in_data(self,want_print=True):
        r_data = self.self_read().split(self.sep)
        dec = []
        sec = []
        ret=True
        for i in range((len(r_data))-1):
            if i%2 !=0:
                dec.append(i)
                sec.append(r_data[i])
                if want_print is True:
                    print(i,'-->',r_data[i])
                    ret = False
        if ret:
            return dec,sec
        
    def extract_file(self,index,file_name=None):
        if file_name is None:
            file_name=self.files_in_data(want_print=False)[1][index//2]
        r_data = self.self_read().split(self.sep)
        w_data = r_data[index-1]
        with open(file_name,'wb') as f:
            f.write(w_data)
        print(file_name,' ✓')
        
    def delete_file(self,index):
        r_data = self.self_read().split(self.sep)
        indexo = self.files_in_data(want_print=False)[0]
        indexo.remove(index)
        self.file_writer(b'','wb')
        for i in indexo:
            self.file_writer(r_data[i-1],'ab')
            self.file_writer(self.sep,'ab')
            self.file_writer(r_data[i],'ab')
            self.file_writer(self.sep,'ab')
        print(index,' ✖')
    def extract_all(self):
        try:
            for i in self.files_in_data(want_print=False)[0]:
                self.extract_file(i)
        except Exception as e:
            return e
    def swap(self,x,y):
        li = self.self_read().split(self.sep)
        li[x-1],li[x],li[y-1],li[y]=li[y-1],li[y],li[x-1],li[x]
        self.file_writer(b'','wb')
        for i in li:
            self.file_writer(i,'ab')
            self.file_writer(self.sep,'ab')
        print(x,y,' are Swapped.')
    def change_icon(self,index=None,icon=None):
        if index is not None:
            self.swap(1,index)
        if icon is not None:
            self.add_file(icon)
            self.swap(1,self.files_in_data(want_print=False)[0][-1])
        self.remove_trash()

    def remove_trash(self):
        trash=self.files_in_data(want_print=False)[1]
        trash_index=[]
        for i in range(len(trash)):
            if trash[i] == b'':
                trash_index.append(i)
        trash_index.reverse()
        for i in trash_index:
            self.delete_file(((i*2)+1))
