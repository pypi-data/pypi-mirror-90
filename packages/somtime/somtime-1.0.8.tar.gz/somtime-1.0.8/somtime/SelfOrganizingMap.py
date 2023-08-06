#python libraries needed in code
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import copy
from collections import defaultdict

class SelfOrganizingMap:
    def __init__(self, inputSize, variables, hiddenSize):
        ##############################
        # author: Ali Javed
        # October 14 2020
        # email: ajaved@uvm.edu
        #############################
        # Description: Class initilizer. This function creates an instance of neural network saving the parameters and setting random weights
        # inputsSize: number of input nodes needed i.e. 5.
        # variables: In case of multivariate time series data, the number of variables. For a list of featuers, this parameter will be 1.
        # hiddenSize: number of hidden layer nodes [2,3] will create a 2x3 node grid
        ########################################
        #set random see for reproducibility
        np.random.seed(0)
        # initilize variables
        self.hiddenSize = np.asarray(hiddenSize)
        self.inputSize = inputSize
        # always start learning rate at 0.9
        self.learningRateInitial = 0.9
        self.learningRate = 0.9
        self.neighborhoodSizeInitial = int(self.hiddenSize[0] / 2)
        self.neighborhoodSize = int(self.hiddenSize[0] / 2)
        self.Umatrix = np.zeros((self.hiddenSize[0],self.hiddenSize[1]))
        self.dim = variables
        # initilize weights between 0 and 1 for a 3d weights matrix
        self.weights_Kohonen = np.random.uniform(low=0, high=1,
                                                 size=(self.hiddenSize[0], self.hiddenSize[1], self.dim, self.inputSize))

        # grid layer activations to allow for finding winning node
        self.gridActivation = np.zeros((self.hiddenSize[0], self.hiddenSize[1]))

        # Kohonen/Output Layer winning node initlize to -1 (no node is minus 1, this is just a place holder)
        self.winnerNeuronIndex = -1



        # def oned_to_grid_inde(index):
        # function returns the index (in int) for each node in grid with the top left node being 0 and the bottom right node being i*j.

    #    return np.unravel_index(index, self.hiddenSize)
    # def grid_to_1d_index(i,j)
    #    return np.ravel_multi_index((i,j),dims = hiddenSize, mode  = 'raise')

    def update_parameters(self, iteration, epoch):
        #############################
        # Description: Update the neighborhood size and learning rate
        # iteration: number of current iteration
        # epoch: total epochs to run the SOM for
        ########################################
        self.neighborhoodSize = self.neighborhoodSizeInitial * (1 - (iteration / epoch))
        self.learningRate = self.learningRateInitial * (1 - (iteration / epoch))

    def find_neighbor_indices(self, i, j):
        # function finds the neighboring rows and columns to include
        # i : i-th index
        # j : j-th index
        # dist: how big the neighborhood should span
        #########################################################
        rows = []
        columns = []

        # python indexing starts with 0 so adjust here
        i = i + 1
        j = j + 1
        if i > self.hiddenSize[0] or i < 1 or j > self.hiddenSize[1] or j < 1:
            neighborhood = set()
            return neighborhood
            
            
        rows = np.arange(i - int(self.neighborhoodSize), i + int(self.neighborhoodSize) + 1)
        columns = np.arange(j - int(self.neighborhoodSize), j + int(self.neighborhoodSize) + 1)

        # get neighbor indexes as a combination of rows and columns
        neighborhood = set()
        for row in rows:
            for column in columns:
                #do not do wrap around neighborhood
                if row > self.hiddenSize[0] or row < 1 or column > self.hiddenSize[1] or column < 1:
                    continue
                
                row = row % self.hiddenSize[0]

                column = column % self.hiddenSize[1]

                if row == 0:
                    row = self.hiddenSize[0]
                if column == 0:
                    column = self.hiddenSize[1]

                # do not update actual row, because it is used in the loop
                row_temp = row - 1
                column_temp = column - 1

                neighborhood.add((row_temp, column_temp))

        return neighborhood

    def findWinningNode(self, x, windowSize):
        ## function to find winning node
        #: input observatiopn

        # format input for use in this function --- dtw distance
        # x = np.reshape(x[0], (1, 1, len(x[0])))


        ####################################
        # calculate distances (in Euclidean and DTW it is the minimum). Iterate over all nodes to find distance
        distances = np.zeros((self.hiddenSize[0], self.hiddenSize[1]))
        distances = distances + float('inf')
        for i in range(0, self.hiddenSize[0]):
            for j in range(0, self.hiddenSize[1]):
                # get weights associated to i-th and j-th node
                weights = self.weights_Kohonen[i, j, :,:]
                # make sure correct shape
                weights = np.reshape(weights, (1, np.shape(weights)[0], np.shape(weights)[1]))

                # format inputs for dynamic time warping

                # use dynamic time warping as distance measure which has a window size parameter
                
                d1 = np.reshape(x,(1,np.shape(x)[1],np.shape(x)[2]))
                d2 = np.reshape(weights, (1, np.shape(weights)[1], np.shape(weights)[2]))
                distance = self.dtw_d(d1, d2, windowSize)
                if distance != distance:
                    print('DTW error: Nan Value')
                distances[i, j] = distance



        # minimum value is winner
        winnerNeuronIndex = np.argmin(distances)

        return winnerNeuronIndex

    def propogateForward(self, x, windowSize):
        ############
        # Description: Function forward propogates from input to grid
        # x: single input
        # windowSize: window size for dynamic time warping

        ##############################
        # input to Kohonen
        ##############################


        # make sure x is in correct shape for matrix multiplication
        x = np.reshape(x, (1, np.shape(x)[0], np.shape(x)[1]))

        self.winnerNeuronIndex = self.findWinningNode(x, windowSize)

    def update_weights_Kohonen(self, x):
        ############
        # Description: Function updates the Kohonen layer (SOM layer) after one forward pass (i.e., forwardPropogate)
        # x: single input

        # make sure x is in correct shape
        ##############
        x = np.reshape(x, (1, np.shape(x)[0], np.shape(x)[1]))

        # convert the single winning index into grid location (x, and y cordinate)
        two_dIndex = np.unravel_index(self.winnerNeuronIndex, self.hiddenSize)

        neighborhood = self.find_neighbor_indices(two_dIndex[0], two_dIndex[1])

        # implement update formula to update all neighborhood
        for neighbors in neighborhood:
            i = neighbors[0]
            j = neighbors[1]

            # calculate the update
            loss = 0
            for m in range(0,np.shape(x)[1]):
                update = self.learningRate * (x[0,m,:] - self.weights_Kohonen[i, j, m,:])

                # update the weights
                self.weights_Kohonen[i, j, m,:] = self.weights_Kohonen[i, j, m,:] + update
                loss+= sum(abs(update))
        return loss

    def iterate(self, inputs, epochs, path = '',windowSize = 0, targets = [], labels = [],legend_dict = {}, showPlot = 'False'):
        ############
        # Description: Function iterates to organize the Kohonen layer

        # inputs: all inputs
        # epochs: epochs to iterate for
        # path: Path to save SOM plots
        # windowSize: windowSize to be used by DTW (for project), not usefull in assignment and set to 0.
        # targets: keys or ids for each observation
        # labels: labels, or ground truth.
        #returns
        #all_data: list of dictionary objects with 4 keys, 'target','x','y', and 'labels'
        # x: x coordinate on SOM
        # y: y cordinate on SOM
        # target: keys or name of observation if provided.
        # label: label (ground truth) of observation if provided.
        ##############

        # reinitilize weights based on inputs

        # initilize weights between 0 and 1 for a 3d weights matrix
        self.weights_Kohonen = np.random.uniform(low=0, high=1,
                                                 size=(self.hiddenSize[0], self.hiddenSize[1], self.dim,self.inputSize))

        # formula for weights initilization
        for i in range(0, np.shape(inputs)[1]):
            for j in range(0, np.shape(inputs)[2]):
                firstPart = (np.mean(np.asarray(inputs)[:,i, j]) + np.random.uniform(-0.1, 0.1))
                secondPart = (np.mean(np.asarray(inputs)[:,i, j]) * np.random.uniform(low=0, high=1, size=(self.hiddenSize[0], self.hiddenSize[1])))
                weights = firstPart * secondPart
                self.weights_Kohonen[:, :, i, j] = weights


        #######################
        # for epochs
        weight_change_magnitude = []
        for epoch in range(0, epochs):
            # for each input
            epoch_loss = 0
            for i in range(0, len(inputs)):
                # propogate forward
                self.propogateForward(inputs[i], windowSize)

                # update Kohonen
                loss = self.update_weights_Kohonen(inputs[i])
                epoch_loss += loss
            if epoch % 20 == 0:
                print('Epoch : ' + str(epoch) + ' complete.')
                print('Neighborhood Size : '+str(self.neighborhoodSize))
                print('Learning Rate : '+str(self.learningRate))
                print('**************************************')
                if len(path)>0:
                    self.plotMap(inputs, epoch, showPlot, windowSize,path,targets,labels = labels,legend_dict = legend_dict )

            self.update_parameters(epoch, epochs)
            if self.neighborhoodSize < 1:
                self.neighborhoodSize = 1
            if self.learningRate < 0.2:
                self.learningRate = 0.2
            
            weight_change_magnitude.append(epoch_loss)
        print('Epoch : ' + str(epoch + 1) + ' complete.')
        print('Neighborhood Size : '+str(self.neighborhoodSize))
        print('Learning Rate : '+str(self.learningRate))
        print('**************************************')
        
        #get Umatrix
        self.Umatrix = self.createUmatrix(windowSize)
        
        if len(path)>0:
            all_data = self.plotMap(inputs, epoch, showPlot, windowSize,path,targets,labels = labels,Umatrix = self.Umatrix,legend_dict  = legend_dict ,write = False) #,
        
            self.plotChange(weight_change_magnitude,showPlot, path)
        
        
        return all_data
        
    def createUmatrix(self,windowSize):
        #############################
        # Description: create the umatrix
        # windowSize: window size for dynamic time warping. Umatrix function currentl always uses Euclidean distance to avoid theoritical issues.
        ########################################
        #set neighborhood size to 1 and reset it after the function
        neighborHood_temp = copy.deepcopy(self.neighborhoodSize)
        self.neighborhoodSize = 1
        
        Umatrix = np.zeros((self.hiddenSize[0],self.hiddenSize[1]))
        # Perform 2D convolution with input data and kernel  to get sum of neighboring nodes
        for i in range(0,self.hiddenSize[0]):
            for j in range(0,self.hiddenSize[1]):
                #find all the neighbors for node at i,j
                neighbors = self.find_neighbor_indices(i, j)
                #remove self
                neighbors.remove((i, j))
                #get weights for node at i,j
                weights =  self.weights_Kohonen[i,j,:]
                weights =  np.reshape(weights, (1,np.shape(weights)[0],np.shape(weights)[1]))
                #for all neighbors
                for neighbor in neighbors:
                    #get x,y (i,j) coordinate for neighbor
                    
                    x = neighbor[0]
                    y = neighbor[1]

                    #get neighbor weights
                    neighborWeights = self.weights_Kohonen[x,y,:]
                    neighborWeights = np.reshape(neighborWeights, (1, np.shape(neighborWeights)[0],np.shape(neighborWeights)[1]))

                    # use dynamic time warping as distance measure which has a window size parameter
                    #always use Euc distance for Umatrix
                    
                    distance = self.dtw_d(weights, neighborWeights,0)
                    Umatrix[i,j] += distance
                Umatrix[i,j] = Umatrix[i,j] / len(neighbors)

        #reset neighborhoodSize
        self.neighborhoodSize = copy.deepcopy(neighborHood_temp)
        
        return Umatrix
                    
                    
                
        

    def plotChange(self, weight_change_magnitude,showPlot ,path):
        plt.figure()
        plt.plot(np.arange(0,len(weight_change_magnitude)),weight_change_magnitude)
        plt.xlabel('Epochs',fontsize = 22)
        plt.ylabel('Weight change magnitude',fontsize = 22)
        plt.ylim(0,max(weight_change_magnitude))
        plt.xlim(0,len(weight_change_magnitude))
        plt.savefig(path+'_weight_change.png',bbox_inches = 'tight')
        if showPlot == 'True':
            plt.show()
        else:
            plt.close()
    

    def plotMap(self, inputs, epoch, showPlot,windowSize, path = 'plot_epoch', targets = [],Umatrix = [], labels= [], legend_dict = {}, write = False):
    
        if len(legend_dict.keys())==0:
            setOfLabels= set(labels)
            for l in setOfLabels:
                legend_dict[l] = l
    
        #colors to label points
        colors = ['#9e0142','#d53e4f','#f46d43','#fdae61','#fee08b','#ffffbf','#e6f598','#abdda4','#66c2a5','#3288bd','#5e4fa2','#f768a1','#c7e9c0','#74c476','#238b45','#fec44f']
        #colors = ['#d7191c','#abdda4','#2b83ba']
        #for legend
        colors_used = set()
        # plot observations with labels
        plt.figure(figsize = (6,6))
        
        #plot Umatrix first so other stuff is over it
        if len(Umatrix)> 0:
            #normalize U matrix
            
            #ignore the zero padding for minimum

            min_v = Umatrix.min()
            max_v = Umatrix.max()
            Umatrix = (Umatrix - min_v) / (max_v - min_v)
            #update values less than 0 to zero
            Umatrix[Umatrix<0] = 0
            Umatrix = Umatrix * 255
            plt.imshow(Umatrix.transpose(), cmap='Greys',alpha=1)

            
            
        plotted = set()
        #write to CSV
        all_data = []
        node_to_scatterSize = defaultdict(lambda: 30)
        for i in range(0, len(inputs)):
            input = inputs[i]
            input = np.reshape(input, (1, np.shape(input)[0],np.shape(input)[1]))
            winnderNode = self.findWinningNode(input, windowSize)

            # convert to x - y coordinate
            coord = np.unravel_index(winnderNode, self.hiddenSize)

            #save to dict for writing to csv
            d = {}
            d['x'] = coord[0]
            d['y'] = coord[1]
            if len(targets)> 0:
                d['target'] = targets[i]
            if len(labels) >0:
                d['labels'] = labels[i]
            all_data.append(d)
            
            
            if coord in plotted:
                #just add some noise so duck and goose can show seperately. They are exactly the same as per data
                #shift = random.uniform(1, 4)
                #shift = 0
                x = coord[0]
                y = coord[1] #+ shift
                node_to_scatterSize[winnderNode] += 30
                #print('scatter size increased.')
                #print(node_to_scatterSize[winnderNode])
            else:
                plotted.add(coord)
                x = coord[0]
                y = coord[1]
            
            #scatter plot at same location but annotation differently
            #plt.scatter(coord[0], coord[1], s=30, color = '#2ca25f')
            if len(labels)>0:
                color = colors[labels[i]]
            else:
                color ='#2ca25f'
            if color in colors_used:
                plt.scatter(x, y, s=node_to_scatterSize[winnderNode], color = color)
            else:
                colors_used.add(color)
                if len(labels)>0:
                    plt.scatter(x, y, s=node_to_scatterSize[winnderNode], color = color,label = legend_dict[labels[i]])
                else:
                    plt.scatter(x, y, s=node_to_scatterSize[winnderNode], color = color)
            #if len(targets)> 0:
            #    plt.annotate(targets[i], (x, y), fontsize=22)



                
        
            
            
        
        plt.xlim(0 - 5, self.hiddenSize[0] + 5)
        plt.ylim(0 - 5, self.hiddenSize[1] + 5)
        plt.xlabel('Nodes', fontsize=22)
        plt.ylabel('Nodes', fontsize=22)
        plt.xticks([])
        plt.yticks([])
        plt.title('Kohonen Self-Organizing Map', fontsize=22)
        if len(labels)>0:
            plt.legend(fontsize = 18,bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.savefig(path+'_'+str(epoch)+'.png',bbox_inches = 'tight')
        if showPlot == 'True':
            plt.show()
        else:
            plt.close()


        return all_data

    
    def getWeights(self):
        return self.weights_Kohonen

    def getActivations(self):
        return self.gridActivation

    def getUmatrix(self):
        return self.Umatrix
        


    def sq_euc(self,s1, s2):
    #author: Ali Javed
    #email: ajaved@uvm.edu
    #Version history:
    #Version 1 . basis implementation of dynaimc time warping dependant.
    #Version 2 (7 Nov 2019). changed variable names to be more representative and added comments.

    #Inputs
    #s1: signal 1, size 1 * m * n. where m is the number of variables, n is the timesteps.
    #s2: signal 2, size 1 * m * n. where m is the number of variables, n is the timesteps.


    #OUTPUT
    #dist: Squared euclidean distance
        
        dist = ((s1 - s2) ** 2)
        return dist.flatten().sum()




    def dtw_d(self,s1, s2, w):
    #author: Ali Javed
    #email: ajaved@uvm.edu
    #Version 1 . basis implementation of dynaimc time warping dependant.
    #Version 2 (7 Nov 2019). changed variable names to be more representative and added comments.

    #INPUTS:
    #s1: signal 1, size 1 * m * n. where m is the number of variables, n is the timesteps.
    #s2: signal 2, size 1 * m * n. where m is the number of variables, n is the timesteps.
    #w: window parameter, percent of size and is between0 and 1. 0 is
    #euclidean distance while 1 is maximum window size.
    #
    #OUTPUTS:
    #dist: resulting distance


        s1 = np.asarray(s1)
        s2 = np.asarray(s2)
        s1_shape = np.shape(s1)
        s2_shape = np.shape(s2)
        
        if w<0 or w>1:
            print("Error: W should be between 0 and 1")
            return False
        if s1_shape[0] >1 or s2_shape[0] >1:
            print("Error: Please check input dimensions")
            return False
        if s1_shape[1] != s2_shape[1]:
            print("Error: Please check input dimensions. Number of variables not consistent.")
            return False
        if s1_shape[2] != s2_shape[2]:
            print("Warning: Length of time series not equal")
            
        #if window size is zero, it is plain euclidean distance
        if w ==0:
            dist = np.sqrt(self.sq_euc(s1, s2))
            return dist


        #get absolute window size
        w = int(np.ceil(w * s1_shape[2]))

        #adapt window size

        w=int(max(w, abs(s1_shape[2]- s2_shape[2])));
            
            
        #initilize
        DTW = {}
        for i in range(-1, s1_shape[2]):
            for j in range(-1, s2_shape[2]):
                DTW[(i, j)] = float('inf')
        DTW[(-1, -1)] = 0

        
        for i in range(s1_shape[2]):
            for j in range(max(0, i - w), min(s2_shape[2], i + w)):
                #squared euc distance
                dist = self.sq_euc(s1[0,:,i], s2[0,:,j])
                #find optimal path
                DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

        dist = np.sqrt(DTW[s1_shape[2] - 1, s2_shape[2] - 1])
        
        
        return dist














