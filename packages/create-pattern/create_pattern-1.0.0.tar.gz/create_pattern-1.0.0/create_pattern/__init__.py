def word(letters,mask):
    m123='a'
    if mask==letters:
        m123=''
    letter12 = letters
    letter12 = letter12.upper()
    letter12 = list(letter12)

    print_SS = [[" " for i in range(5)] for j in range(7)]

    for row in range(7):
        for col in range(1):
            if col==1:
                print_SS[row][col]=' '


    #-----------------------------------------------------
    #-----------------------------------------------------
    def A():
        print_A=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if ((col==0 or col==4) and row!=0) or ((row==0 or row==3) and (col>0 and col<4)):
                    print_A[row][col]=mask

        for j in range(5):
                print(print_A[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

    #-----------------------------------------------------

    def B():
        print_B=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==0) or (col==4 and (row!=3 and row!=0 and row!=6)) or((row==0 or row==3 or row==6) and (col>0 and col<4)):
                    print_B[row][col]=mask

        for j in range(5):
            print(print_B[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 


    #-----------------------------------------------------

    def C():
        print_C=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==0) or ((row==0 or row==6) and (col>0)):
                    print_C[row][col]=mask
        for j in range(5):
            print(print_C[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

    #-----------------------------------------------------
    def D():
            
        print_D=[[" " for i in range(5)] for j in range(7)]  

        for row in range(7):
            for col in range(5):
                if (col==0) or (col==4 and (row!=0 and row!=6)) or ((row==0 or row==6) and (col>0 and col<4)):
                    print_D[row][col]=mask
        for j in range(5):
            print(print_D[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 


    #-----------------------------------------------------
    def E():
            
        print_E=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or ((row==0 or row==3 or row==6) and (col>0)):
                    print_E[row][col]=mask

        for j in range(5):
            print(print_E[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 



#-----------------------------------------------------
    def F():
            
        print_F=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==0) or ((row==0 or row==3) and col>0):
                    print_F[row][col]=mask
        for j in range(5):
            print(print_F[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def G():
            
        print_G=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or (col==4 and (row!=1 and row!=2)) or ((row==0 or row==6) and (col>0 and col<4)) or (row==3 and (col==3 or col==5)):
                    print_G[row][col]=mask


        for j in range(5):
            print(print_G[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 



#-----------------------------------------------------
    def H():
        print_H=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or col==4 or (row==3 and (col>0 and col<4)):
                    print_H[row][col]=mask


        for j in range(5):
                print(print_H[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def I():
            
        print_I=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==2 or ((row==0 or row==6) and col!=2):
                    print_I[row][col]=mask

        for j in range(5):
            print(print_I[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def J():
            
        print_J=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==2 or (row==0 and col!=2) or (row==6 and col<2):
                    print_J[row][col]=mask


        for j in range(5):
                print(print_J[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def K():

        print_K=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or (row+col==4 and row<4) or (col==row-2 and row>3):
                    print_K[row][col]=mask




        for j in range(5):
                print(print_K[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def L():
            
        print_L=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or (row==6 and col>0):
                    print_L[row][col]=mask

        for j in range(5):
            print(print_L[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def M():
            
        print_M=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==0 or col==4) or (row+col==4 and row<3) or (col-row==0 and row<3):
                    print_M[row][col]=mask


        for j in range(5):
                print(print_M[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def N():
            
        print_N=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or col==4 or (col-row==-1 and row<6):
                        print_N[row][col]=mask
                else:
                    print_N[row][col]=' '
    

            
                    

        for j in range(5):
                print(print_N[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def O():
            
        print_O=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if ((col==0 or col==4) and (row!=0 and row!=6)) or ((row==0 or row==6) and (col>0 and col<4)):
                    print_O[row][col]=mask


        for j in range(5):
                print(print_O[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def P():
            
        print_P=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or (col==4 and (row==1 or row==2)) or ((row==0 or row==3) and (col>0 and col<4)):
                    print_P[row][col]=mask

        for j in range(5):
                print(print_P[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def Q():
            
        print_Q=[[" " for i in range(5)] for j in range(8)]

        for row in range(7):
            for col in range(5):
                if ((col==0 or col==4) and (row>0 and row<6)) or ((row==0 or row==6) and (col>0 and col<4)):
                    print_Q[row][col]=mask


        for j in range(5):
                print(print_Q[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def R():
            
        print_R=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==0 or (col==4 and(row!=0 and row!=3)) or (row==0 or row==3) and(col>0 and col<4):
                    print_R[row][col]=mask

        for j in range(5):
            print(print_R[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def S():
            
        print_S=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if ((row==0 or row==3 or row==6) and (col>0 and col<4)) or (col==0 and (row>0 and row<3)) or (col==4 and (row>3 and row<6)):
                    print_S[row][col]=mask


        for j in range(5):
                print(print_S[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def T():
            
        print_T=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if col==2 or (row==0 and col!=2):
                    print_T[row][col]=mask

        for j in range(5):
                print(print_T[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def U():
            
        print_U=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if ((col==0 or col==4) and row!=6) or (row==6 and (col>0 and col<4)):
                    print_U[row][col]=mask

        for j in range(5):
                print(print_U[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def V():

        print_V=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if ((col==2 or col==4)and row<5) or (row==6 and col==3) or (row==5 and (col==2 or col==4)):
                    print_V[row][col]=mask

            


        for j in range(5):
                print(print_V[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def W():

        print_W=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==0 or col==4) or (row+col==5 and row>2) or (row-col==1 and row>2):
                    print_W[row][col]=mask


        for j in range(5):
                print(print_W[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def X():
            
        print_X=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if row+col==6 or row-col==2:
                    print_X[row][col]=mask

        for j in range(5):
                print(print_X[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def Y():
            
        print_Y=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (col==2 and row>1) or (col==row and col<2) or (row==0 and col==4) or (row==1 and col==3):
                    print_Y[row][col]=mask

        for j in range(5):
            print(print_Y[i][j],end="")
            print(end=' ')
        for j in range(1):
            print(print_SS[i][j],end=" ") 

#-----------------------------------------------------
    def Z():
            
        print_Z=[[" " for i in range(5)] for j in range(7)]

        for row in range(7):
            for col in range(5):
                if (row==0 or row==5) or (row+col==5):
                    print_Z[row][col]=mask

        for j in range(5):
                print(print_Z[i][j],end="")
                print(end=' ')
        for j in range(1):
                print(print_SS[i][j],end=" ") 


    #-----------------------------------------------------
    for i in range(7):

        for j in range(len(letter12)):
            j = letter12[j]
            if m123=='':
                mask=j

            if j=='A':
                A()
            
            elif j=='B':
                B()
            
            elif j=='C':
                C()

            elif j=='D':
                D()

            elif j=='E':
                E()

            elif j=='F':
                F()

            elif j=='G':
                G()

            elif j=='H':
                H()
            
            elif j=='I':
                I()

            elif j=='J':
                J()

            elif j=='K':
                K()

            elif j=='L':
                L()

            elif j=='M':
                M()

            elif j=='N':
                N()
            
            elif j=='O':
                O()

            elif j=='P':
                P()

            elif j=='Q':
                Q()

            elif j=='R':
                R()

            elif j=='S':
                S()

            elif j=='T':
                T()
            
            elif j=='U':
                U()

            elif j=='V':
                V()

            elif j=='W':
                W()

            elif j=='X':
                X()

            elif j=='Y':
                Y()

            elif j=='Z':
                Z()
            
            
        print()

    #------------------------------------------------------


def heart(mask):
    for row in range(6):
        for col in range(7):
            if (row==0 and col%3!=0) or (row==1 and col%3==0) or (row-col==2) or (row+col==8):
                print(mask,end=' ')
            else:
                print(end=' ')
        print()

#heart('*')











