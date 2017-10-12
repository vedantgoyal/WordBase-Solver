import poc_grid 

WORDFILE = "assets_scrabble_words3.txt"
TOP = 0
BOTTOM = 1

class WordBase(poc_grid.Grid):
    
    def __init__(self,board,side):
        grid_height = len(board)
        grid_width = len(board[0])
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        self._board = board
        self._side=side
    
    def words_generate(self,start,depth):
        """
        Find words in the grid
        """
        def word_jinie(wordlist):
            word_lst = []
            for word in wordlist:
                for cell in self.eight_neighbors(word[-1][0],word[-1][1]):
                    if cell not in word:
                        word_lst.append(word+[(cell)])
            return word_lst
        
        mega_list = []
        for cell in self.eight_neighbors(start[0],start[1]):
            mega_list.append([start]+[cell])
            word_list = mega_list
        for jdx in range(depth-2):
            word_list = word_jinie(word_list)
            mega_list+=word_list
        return mega_list
         
    def load_words(self,filename):
        """
        Load word list from the file named filename.
    
        Returns a list of strings.
        """
        dictionary = open(filename,'r')
        return [line.strip() for line in dictionary.readlines()]
        
    def word_convert(self,word_list):
        words_gen = []
        for word in word_list:
            word_str=""
            for idx in word:
                word_str+=self._board[idx[0]][idx[1]]
            words_gen.append(word_str)
        return words_gen
    
    def run(self,start_point,depth,for_limit):
        """
        Run game.
        """
        words_long = self.load_words(WORDFILE)
        words=[]
        init_let = self._board[start_point[0]][start_point[1]]
        for wordie in words_long:
            if wordie[0]==init_let:
                words.append(wordie)
        word_indexs = self.words_generate(start_point,depth)
        word_filt = self.forward_filter(word_indexs,for_limit,start_point)
        poss_words = self.word_convert(word_filt)
        for each_word in poss_words:
            if each_word in words:
                print each_word

    def forward_filter(self,word_list,limit,start_point):
		"""
		Prune generated word list
		"""
        sort_list =[]
        for word in word_list:
            reachmax = max(word,key=lambda item:item[0])[0]
            reachmin = min(word,key=lambda item:item[0])[0]
            if self._side == TOP and reachmax>=(start_point[0]+limit):
                sort_list.append((word,reachmax))
            if self._side == BOTTOM and reachmin<=(start_point[0]-limit):
                sort_list.append((word,reachmin))            
        forward_sorted = sorted(sort_list, key=lambda tup: tup[1])
        final_list = []
        for word in forward_sorted:
            final_list.append(word[0])
        if self._side == TOP:
            return final_list
        if self._side == BOTTOM:
            return final_list[::-1]
        
      
def fast_grid(org_grid):
    proper_grid =[[] for dummy_idx in org_grid]
    count = 0
    for line in org_grid:
        for letter in line:
            proper_grid[count].append(str(letter))       
        count+=1
    return proper_grid

def print_grid(grid):
    ans = ""
    for row in range(len(grid)):
        ans += str(grid[row])
        ans += str(row)
        ans += "\n"
    ans+=str(["0","1","2","3","4","5","6","7","8","9"])
    return ans

#-----------------------------------#
###
def memory(choice,replacement=None,grid_change=False):
        grids = {
                'grid1' : (["tpsachgtoj","ratoytniao","ymerweauru","osabrdiptd","paneotpnvi","inighmgeae","logdaidwes","asuenwgnrv","ineyrsyhic","mlsetiplta","aedrsrfren","topuapoure","rlnktskgnp"],TOP),  
                'grid2' : (["arfedoapmi","enivtreshl","coatgimrst","rcebonvaeu","tnyspoeipd","meuadiscet","edrgeclral","ansrietimi","rtaksmyesf","agenithfen","deosarxcig","yrsleiteua","bouepsdnbc"],BOTTOM),  
                'grid3' : (["trodoypkrl","oecearepap","irehosnofi","lostlehrnu","tpmludmcli","sneslyoaek","tirksutrsh","kcoshyeatc","ywabeducea","erwjisdpnr","sniowuisef","odrsepstag","buntrareuc"],BOTTOM),
                'grid4' : (["bleneomrls","cautgmsuhc","tergnayioa","wudnotlonr","oamoeielep","rnrizsgrsu","sekadtodlm","alamlcsies","emismuntzm","rukdtigaon","tspnerloel","oauiasgmdg","coidcetnie"],BOTTOM)
                }
        if grid_change == True:
            grids[choice]=replacement
            return None
        return grids[choice]

def mem_display():
    print "grid1: ",memory("grid1")[0][0]
    print "grid2: ",memory("grid2")[0][0]
    print "grid3: ",memory("grid3")[0][0]
    print "grid4: ",memory("grid4")[0][0]        

####
def get_data():
    row = int(raw_input("Row: "))
    col = int(raw_input("Col: "))
    depth = int(raw_input("Max length: "))
    limit = int(raw_input("Min Reach: "))
    return row,col,depth,limit

####
def run_game(new_grid,data,side):
    Game = WordBase(new_grid,side)
    Game.run((data[0],data[1]),data[2],data[3])

###
def make_grid():
    print "Type 'done' when you are done!"
    new_grid = []
    row = "not_done"
    while row!="done":
        row = raw_input("Row: ")
        new_grid.append(row)
    new_grid.pop()
    satis = raw_input("Are you satisfied? (yes/no?)")
    if satis=="no":
        return None
    side = None
    while side!="top" and side!="bottom":
            side = raw_input("What is your side? (top/bottom?)")
            if side == "top":
                grid_info = (new_grid,TOP)
            if side == "bottom":
                grid_info = (new_grid,BOTTOM)
    mem_display()
    save_rq = raw_input("do you wish to save grid (yes/no?):")
    if save_rq == "yes":
        save_name = raw_input("Save as:(name)?")
        memory(save_name,grid_info,True)
    return grid_info

####
command = raw_input("load/new: ")
while command!="exit":
    if command == "again":
        print print_grid(new_grid)
        data = get_data()
        run_game(new_grid,data,side)
    if command == "new":
        grid_info = make_grid()
        while grid_info==None:
            grid_info = make_grid()
        side = grid_info[1]
        new_grid = fast_grid(grid_info[0])
        print print_grid(new_grid)        
        data = get_data()        
        run_game(new_grid,data,side)
    if command == "load":
        mem_display()
        choice = raw_input("grid1/grid2/grid3/grid4? ")
        grid_info = memory(choice)
        new_grid = fast_grid(grid_info[0])
        side = grid_info[1]
        print print_grid(new_grid)       
        data = get_data()
        run_game(new_grid,data,side)
    command = raw_input("again/new/load/exit? ")
    
    
