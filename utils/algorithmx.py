class Data:
    
    def __init__(self, head=None, left=None, 
                 right=None, up=None, down=None, row_name=None):
        
        self.head = head # column header
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        
        self.row_name = row_name
        
class Header(Data):
    
    def __init__(self, head=None, left=None, right=None, 
                 up=None, down=None, size=None, name=None):
        
        super().__init__(head, left, right, up, down)
        self.size = size
        self.name = name
        
class Matrix:
    
    def __init__(self, mat, column_names, row_names=None):
        
        num_rows = len(mat)
        num_columns = len(mat[0])
        
        self.root = Header(name="root")
        self.root.left = self.root
        self.root.right = self.root
        
        self.columns = {name:None
                        for name in column_names}
        
        if row_names is None:
            row_names = [i for i in range(num_rows)] 
        
        for i, name in enumerate(column_names):
            
            new_column = Header(left=self.root.left,
                                right=self.root,
                                size=0, name=name)
            
            new_column.up = new_column
            new_column.down = new_column
            
            self.root.left.right = new_column
            self.root.left = new_column
            
            self.columns[name] = (i, new_column)
            
        for i in range(num_rows):
            
            row_head = Data()
            row_head.left = row_head
            row_head.right = row_head
            
            for j in range(num_columns):
                
                if mat[i][j] == 1:
                    
                    name = column_names[j]
                    column_head = self.columns[name][1]
                    column_head.size += 1
                    
                    new_data = Data(head=column_head,
                                    left=row_head.left,
                                    right=row_head,
                                    up=column_head.up,
                                    down=column_head,
                                    row_name = row_names[i])
                    
                    column_head.up.down = new_data
                    column_head.up = new_data
                    
                    row_head.left.right = new_data
                    row_head.left = new_data
                    
            row_head.left.right = row_head.right
            row_head.right.left = row_head.left
            
    def cover(self, name):
        
        # Removes column_head from the header list and removes 
        # all the rows in column_head's list from other column lists
    
        column_head = self.columns[name][1]
        column_head.right.left = column_head.left
        column_head.left.right = column_head.right
        
        i = column_head.down
        
        while not i is column_head:
            j = i.right
            while not j is i:
                j.down.up = j.up
                j.up.down = j.down
                j.head.size -= 1
                
                j = j.right
                
            i = i.down
                
    def uncover(self, name):
        
        # the opposite of cover
        
        column_head = self.columns[name][1]
        
        i = column_head.up
        
        while not i is column_head:
            j = i.left
            while not j is i:
                j.head.size += 1
                j.down.up = j
                j.up.down = j
                
                j = j.left
                
            i = i.up
        
        column_head.right.left = column_head
        column_head.left.right = column_head
        

def search_util(k, mat, sol, sol_array):
    
    if mat.root is mat.root.right:
        sol_array.append(sol.copy())
        return
    
    column_head = mat.root.right
    
    # heuristic
    c = mat.root.right
    s = c.size
    while not c is mat.root:
        if c.size<s:
            column_head = c
            s = c.size
        c = c.right
        
    mat.cover(column_head.name)
    
    r = column_head.down
    while not r is column_head:
        sol.append(r)
        j = r.right
        while not j is r:
            mat.cover(j.head.name)
            j = j.right
        
        search_util(k+1, mat, sol, sol_array)        
        r = sol.pop()
        column_head = r.head
        
        j = r.left
        while not j is r:
            mat.uncover(j.head.name)
            j = j.left
        
        r = r.down
    
    mat.uncover(column_head.name)
    return
    
def search(A, column_names):
    
    mat = Matrix(A, column_names)
    sol = []
    sol_array = []
    
    search_util(0,mat,sol,sol_array)