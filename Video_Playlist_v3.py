import cv2
import numpy as np
import os

class Node:          #  Node of a Video
    def __init__(self,sea,epi,ad):   # Implementation of 'Doubly Linked List'
        self.prev=None
        self.next=None
        self.season=sea
        self.episode=epi
        self.addr=ad

class Tree_Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class Tree:
    def __init__(self):
        self.root = None

    def insert(self,val):
        if self.root==None:
            self.root=Tree_Node(val)
        else:
            self._insert(self.root,val)
            
    def _insert(self,node,val):
        q = []
        q.append(node)
        while len(q):
            node = q.pop(0)
            if not node.left:
                node.left = Tree_Node(val)
                break
            else:
                if node.left.data==val:
                    break
                q.append(node.left)
            if not node.right:
                node.right = Tree_Node(val)
                break
            else:
                if node.right.data==val:
                    break
                q.append(node.right)

    def print_tree(self):
        self.display(self.root)

    def display(self,node):
        if node is None:
            return
        print(node.data.split(':')[0])
        self.display(node.left)
        self.display(node.right)


class Video:                      #   Video class holding essential node links
    def __init__(self):
        self.head=None
    
    def set_nodes(self):
        tree = Tree()
        sf=open(r"Admin\series_count.txt","r")
        series=sf.read()
        series=int(series)
        sf.close()
        if series==0:
            print('\nNo Seasons available to watch.\nCome back later...\n')
        else:
            print('\nSeasons already Present :-\n')
            for i in range(series):
                print('Series '+str(i+1))
            curr=input('\nSelect a Season to watch : ')
            txt='Admin/series_'+curr+'.txt'
            ef=open(txt,'r')
            name=ef.readline()
            episodes=ef.read()
            print(f'\nEpisodes in Series_{curr} - {name} \n')
            ef.close()
            episodes=episodes.split('\n')       # List Data_Structure Usage
            self.episodes=episodes[:-1]

            for i in self.episodes:             # Binary Tree Data_Structure Usage
                tree.insert(i)
            tree.print_tree()

            for i in range(len(self.episodes)): # Doubly LinkedList Data_Structure Usage
                if self.head==None:
                    temp = Node('S'+curr,self.episodes[i].split(':')[0],episodes[i].split(':')[1])
                    self.head=temp
                else:
                    this=self.head
                    temp = Node('S'+curr,episodes[i].split(':')[0],episodes[i].split(':')[1])
                    while this.next!=None:
                        this=this.next
                    this.next=temp
                    temp.prev=this
            self.play_vids()
                    
    def play_vids(self):
        node=self.head
        while True:
            clear()
            print(f"\nCurrently Playing {node.season} - {node.episode}...\n\nPress 'Q' to stop playing....\n")
            self.play_mp4('Videos/'+node.addr)
            if node.prev==None:
                move=int(input('\n1.Play Next\n2.Quit\n\nEnter your option : '))
                if move==1:
                    node=node.next
                elif move==2:
                    break
            elif node.next==None:
                move=int(input('1.Play Previous\n2.Quit\n\nEnter your option : '))
                if move==1:
                    node=node.prev
                elif move==2:
                    break
            else:
                move=int(input('1.Play Next\n2.Play Previous\n3.Quit\n\nEnter your option : '))
                if move==1:
                    node=node.next
                elif move==2:
                    node=node.prev
                elif move==3:
                    break
        
    def play_mp4(self,file):
        cap = cv2.VideoCapture(file)

        if (cap.isOpened()== False):
            print("\nError opening video file !\n") 

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

class Admin:   
    def __init__(self):
        self.logged=False
        self.series_count=0

    def login(self):
        adm_nm=input("\nEnter Admin Username : ")
        adm_ps=input("Enter Admin Password : ")
        f=open("Admin/admin_creds.txt","r")
        self.admn=f.readlines()
        f.close()                                     # TIME-COMPLEXITY CALCULATION for this function
        if self.admn[0][:-1]==adm_nm:                 #O(1)
            if self.admn[1]==adm_ps:                  #O(2)
                print("\nLogged in Successfully !")
                self.logged=True                      #O(3)
            else:
                print("\nIncorrect Password !")
                self.logged=False                     #O(4)
        else:
            print("\nIncorrect Username !\n")
            self.logged=False                         #O(5)

        # Time Complexity of login() Function is O(1) as it takes constant time...

    def change_pass(self):
        old_p=input("\nEnter Old Password : ")
        if old_p==self.admn[1]:
            new_p=input("\nEnter New Password : ")
            f=open("Admin/admin_creds.txt","w")
            f.write(self.admn[0])
            f.write(new_p)
            f.close()
        else:
            print("Incorrect Old Password !")

    def add_episodes(self):
        sf=open("Admin/series_count.txt","r")
        series=sf.read()
        self.series_count=int(series)+1
        sf.close()
        sf=open("Admin/series_count.txt","w")
        sf.write(str(self.series_count))
        sf.close()
        txt="Admin/series_"+str(self.series_count)+".txt"
        ef=open(txt,"w")
        name=input(f'\nEnter a name to Season-{self.series_count} Title : ')
        episode_count=int(input(f'\nEnter no.of episodes to add in Series {self.series_count} : '))
        ef.write(name+'\n')
        for i in range(episode_count):
            addr=input(f'\nEnter video-file name for E{i+1} : ')
            ef.write('e'+str(i+1)+':'+addr+'\n')
        ef.close()

    def del_episodes(self):
        sf=open(r"Admin\series_count.txt","r")
        series=sf.read()
        series=int(series)
        sf.close()
        if series==0:
            print('\nNo Seasons present.')
        else:
            print('\nSeasons already Present :-\n')
            for i in range(series):
                print('Series '+str(i+1))
            curr=input('\nEnter your number : ')
            txt='Admin/series_'+curr+'.txt'
            ef=open(txt,'r')
            name=ef.readline()
            episodes=ef.read()
            print(f'\nEpisodes in Series {curr} :-\n\n')
            ef.close()
            ef=open(txt,"w")
            episodes=episodes.split('\n')  # List Data_Structure Usage
            episodes=episodes[:-1]
            for i in episodes:
                print(i.split(':')[0])
            count=int(input("\nEnter no.of episodes to delete from back : "))
            episodes=episodes[:-count]
            ef.write(name+'\n')
            for i in episodes:
                ef.write(i+'\n')
            ef.close()
            
class User:
    def __init__(self):
        self.logged=False
        self.user_id=0

    def new_user(self):
        f=open("Users/user_count.txt","r")
        count=f.read()
        self.user_id=int(count)+1
        f.close()
        f=open("Users/user_count.txt","w")
        f.write(str(self.user_id))
        f.close()
        txt='Users/user_'+str(self.user_id)+'.txt'
        f=open(txt,'w')
        f.write('username\n')
        f.write('password')
        f.close()
        print(f'\nAccount Created !\n\nUser_ID : {self.user_id}\nUsername : username\nPassword : password\n\nYou may change it anytime !')

    def login(self):
        self.user_id=int(input('\nEnter User_ID : '))
        f=open('Users/user_count.txt','r')
        count=f.read()
        count=int(count)
        if self.user_id>count:
            print('\nID does not exist !')
        else:
            f=open('Users/user_'+str(self.user_id)+'.txt','r')
            usr_nm=input("\nEnter Username : ")  # default - 'username'
            usr_ps=input("\nEnter Password : ")  # default - 'password'
            self.user=f.readlines()
            if self.user[0][:-1]==usr_nm:
                if self.user[1]==usr_ps:
                    print("\nLogged in Successfully !")
                    self.logged=True
                else:
                    print("\nIncorrect Password !")
            else:
                print("\nIncorrect Username !\n")
        f.close()
    
    def change_pass(self):
        old_p=input("\nEnter Old Password : ")
        if old_p==self.user[1]:
            new_p=input("\nEnter New Password : ")
            f=open("Users/user_"+str(self.user_id)+".txt","w")
            f.write(self.user[0])
            f.write(new_p)
            f.close()
        else:
            print("\nIncorrect Old Password !")

    def show_stats(self):
        f=open("Users/user_count.txt","r")
        count = int(f.read())-1
        if not count:
            print("\nYou are our only valuable subscriber so far !\n")
        else:
            print(f"\nYou and, {count} other people have subscribed to Netflix...!")

    def watch_episodes(self):
        Vid = Video()
        Vid.set_nodes()
        return

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


A = Admin()
U = User()
print("\n\t - WELCOME TO 'NETFLIX' SIMULATOR -\n\n")
while True:
    mode=int(input("\nLogin as ?\n1.Administrator\n2.User\n\nEnter your option : "))
    clear()
    if mode==1:  # Administrator
        while True:
            A.login()
            if A.logged:
                choice=int(input("\n1.Change Password\n2.Add Episodes\n3.Delete Episodes\n\nEnter your option : "))
                clear()
                if choice==1:
                    A.change_pass()
                elif choice==2:
                    A.add_episodes()
                elif choice==3:
                    A.del_episodes()
                else:
                    print('\nInvalid option !')
            opt=int(input("\nDo you want to continue ?\n1.Yes(Admin Login)\n2.No (Main Menu).\n\nEnter your option : "))
            clear()
            if opt==2:
                break
    elif mode==2:  # User
        while True:
            choice=int(input("\n1.New-User SignUp\n2.Old-User Login\n\nEnter your option : "))
            clear()
            if choice==1:
                U.new_user()
            elif choice==2:
                U.login()
                if U.logged:
                    while True:
                        choice=int(input("\n1.Change Password\n2.Watch Episodes\n3.Other Users' stats\n\nEnter your option : "))
                        clear()
                        if choice==1:
                            U.change_pass()
                        elif choice==2:
                            U.watch_episodes()
                        elif choice==3:
                            U.show_stats()
                        else:
                            print('\nInvalid Option !')
                        opt=int(input("\nDo you want to continue ?\n1.Yes(Old_User menu)\n2.No (User Login).\n\nEnter your option : "))
                        clear()
                        if opt==2:
                            break
            opt=int(input("\nDo you want to continue ?\n1.Yes(User Login)\n2.No (Main Menu).\n\nEnter your option : "))
            clear()
            if opt==2:
                break
    else:
        print("\nEnter a Valid option !\n")
    opt=int(input("\nDo you want to continue ?\n1.Yes(Main Menu)\n2.No (Exit).\n\nEnter your option : "))
    clear()
    if opt==2:
        break
print("\nCome back soon ! New and Exciting series' waiting for you !")