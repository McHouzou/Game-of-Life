"""
Game of Life simulator class together with scripts producing equilibration time files and CoM
data. To run, please run 'Run_GoL.py'.
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update_array(lattice_sums, current_value):
    if current_value == 0: #if it's dead, check if it will be revived in next iteration.
        if lattice_sums == 3:
            return 1
        else:
            return 0

    else: #if it's alive, decide on wether to keep alive or kill in next iteration
        if (lattice_sums < 2) or (lattice_sums > 3):  #too isolated or too crowded
            return 0
        else:
            return 1

v_update = np.vectorize(update_array)  #Vectorize update function


class Game_of_life(object):

    def __init__(self, N, M, initial):
        """
        Initialise lattice for game of life. 'N' is size of lattice, 'initial' is the initial state.
        Choose 'initial' from:
            -"rand" = randomly generated
            -"blinker"
            -"gider"
            -"spaceship"

        Lattice has 1s for alive cells, 0s for dead cells
        """

        self.N = N
        self.M = M
        self.lattice = np.zeros((N,M))


        if isinstance(initial, np.ndarray): #If initial is an nd.array (i.e. explicitly given grid with initial condition)
            # initial has to be a square array
            if initial.shape[0] != initial.shape[1]:
                raise TypeError("The initial array has to be square (i.e. of dimensions (m,m))")

            m = initial.shape[0]
            # if the size of "initial" is smaller than self.lattice, place "initial" at the centre of the lattice
            if self.N > m:
                index_start_i = (self.N - m)//2
                index_start_j = (self.M - m)//2

            self.lattice[index_start_i:index_start_i+m, index_start_j:index_start_j+m] = initial


        elif initial == "rand":
            for i in range(N):
                for j in range(M):
                    r = rnd.random()
                    if r > 0.5: self.lattice[i][j] = 1

        elif initial == "blinker":
            center = np.array([2,2])
            #positions of alive cells
            positions = np.array([center+[1,0], center + [-1,0], center])

            for p in positions:
                self.lattice[p[0]][p[1]] = 1

        elif initial == "glider":
            #centers = np.array([[20,20], [21,21], [2,3]])
            centers = np.array([[3,3]])
            for c in centers:
                positions = np.array([c+[0,-1], c+[1,0], c+[-1,1], c+[0,1], c+[1,1]])
                for p in positions:
                    self.lattice[p[0]][p[1]] = 1

        elif initial == "spaceship":
            centers = np.array([[5,5]])
            for c in centers:
                positions = np.array([c, c+[0,-1], c+[0,-2], c+[0,-3], c+[-1,-4], c+[-3,-4], c+[-3,-1], c+[-2,0], c+[-1,0]])
                for p in positions:
                    self.lattice[p[0]][p[1]] = 1



    def update(self, nsteps = 1):
        """
        Simply update lattice according to rules.
        Complete nsteps - number of steps/updates
        """

        nn = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
        nn_sums = np.zeros((self.N, self.M)) #store new lattice after update
        for n in nn: #find nearest neighbours of each lattice point
            nn_sums += np.roll(np.roll(self.lattice, n[0], axis = 0), n[1], axis = 1)
        self.lattice = v_update(nn_sums, self.lattice)

        """
        #Old update function - iterates over array
        #nearest neighbours
        nn = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
        temporary = np.zeros((self.N, self.N)) #store new lattice after update
        for i in range(self.N):
            for j in range(self.N):
                cnt = 0
                for n in nn: #count allive neighbours
                    if self.lattice[(i+n[0])%self.N][(j+n[1])%self.N] == 1: cnt+=1

                if self.lattice[i][j] == 0: #if it's dead, check if it will be revived in next iteration.
                    if cnt == 3:
                        temporary[i][j] = 1
                    else:
                        temporary[i][j] = 0

                else: #if it's alive, decide on wether to keep alive or kill in next iteration
                    if (cnt < 2) or (cnt > 3):  #too isolated
                        temporary[i][j] = 0
                    else:
                        temporary[i][j] = 1

        self.lattice = temporary
        """

    def count_active(self):
        """
        Returns number of active sites
        """
        return self.lattice.sum(axis=1).sum(axis=0)


    def current_com(self):
        """
        Returns the centre of mass of the whole system. If whole grid is dead, returns central coordinates
        """
        total_mass = self.count_active()
        if total_mass != 0:
            CM = np.array([0.0,0.0])
            for i in range(self.N):
                for j in range(self.M):
                    CM += np.array([float(i),float(j)])*self.lattice[i][j]
            CM = CM/total_mass
        else:
            CM = [self.N/2, self.M/2]
        return CM


    def allsame(self, counter):
        """
        Check if all elements in a list are equal. Used in run_to_equilibrium
        """
        temp = counter[0]
        for c in counter[1:]:
            if c != temp:
                return False
        return True


    def run_timesteps(self, Dt):
        """
        It performs Dt updates of grid and then stops.
        """
        for i in range(Dt):
            self.update()


    def run_to_equilibrium(self):
        """
        Runs simulated lattice to 'equilibrium'.
        This is found by looking at the history of active counts. When these plateau
        (i.e. they remain constant for a particular amount of time-steps), then assume equilibrium
        has been reached. Subtract the number of steps you waited to confirm equilibrium was reached.

        Here, the time to wait was chosen as = self.N (e.g. 50),
        so that any travelling structures have time to colide with objects in their way.
        """
        t = 0
        cnt = np.zeros(self.N); cnt[0] = 1
        while (not self.allsame(cnt)) and (t<2000): #while the cnt array is still changing and t<5000, iterate
            cnt = np.roll(cnt, 1, axis=0)
            self.update() #roll update and count active cites. Update cnt
            cnt[0] = self.count_active()
            t+=1
            if t%self.N == 0:
                print(f"At time-step {t}, counter = {cnt[0]}")

        if t!= 2000:
            return t + 1 - self.N
        else:
            return None



    def centre_of_mass(self, npoints, structure):
        """
        Output position of centre of mass of glider every w steps to file.
        """
        w = 4
        filecom = open(f"CoM_{structure}", 'w')
        for n in range(w*npoints):
            self.update()
            if n%w == 0:
                xpos = 0
                ypos = 0
                cnt = 0
                for i in range(self.N):
                    for j in range(self.M):
                        val = self.lattice[i][j]
                        xpos += val*j
                        ypos += val*i
                        cnt += val
                filecom.write(f"{n} {xpos/cnt} {ypos/cnt}")
                filecom.write('\n')
                print(f"{xpos/cnt} {ypos/cnt}")



    #Animation related functions
    def update_anim(self, t):

        self.update()
        if t%10 == 0:
            print(f"{t} {self.count_active()}")
        #update what is to be plotted
        X, Y = np.meshgrid(range(self.M), range(self.N))
        self.mesh.set_array(self.lattice.ravel())
        return self.mesh,



    def run_animate(self, anim_interval):
        #Initiate plots
        size_x = 11
        size_y = 11*(self.N/self.M)
        fig = plt.figure(figsize=(size_x, size_y), dpi=80)
        X, Y = np.meshgrid(range(self.M), range(self.N))
        self.mesh = plt.pcolormesh(X, Y, self.lattice, cmap = plt.cm.binary, shading = 'auto', vmin=0, vmax=1)

        #Animate
        a = animation.FuncAnimation(fig, self.update_anim,  frames = 1000, interval = anim_interval, blit = True)
        writervideo = animation.FFMpegWriter(fps=40)
        plt.show() #To animate live only (no saving of animation), comment out lines 206-207, and uncomment this line
        #a.save("Game_of_life.mp4", writer=writervideo)
        #plt.close()



"""
file = open("Equilibrium_data", 'w')
cnt = 0
while cnt < 1000:
    G = Game_of_life(30, "rand")
    print(f"At simulation no. {cnt+1}" + '\n')
    Eq_steps = G.run_to_equilibrium()
    if Eq_steps:
        print(f"Found equilibrium at time-step {Eq_steps}" + '\n' + '\n')
        file.write(f"{Eq_steps}" + '\n')
        cnt+=1
    else:
        print("Discarding and ignoring")
file.close()
"""


"""
structure = "spaceship"
G = Game_of_life(50, structure)
G.centre_of_mass(100, structure)
"""
