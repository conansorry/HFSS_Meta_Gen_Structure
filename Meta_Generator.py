import numpy
import os
import matplotlib.pyplot as plt


class Meta_Surf:


    def __init__(self, _n: int, _dim: float, _t: float ):

        self.n = _n
        self.dim = _dim
        self.t = _t

        self.a = numpy.zeros((2 * _n, 2 * _n))
        self.pix_l = _dim / (2.0 * _n)

        self.xy_wt = 0.0
        for i in range(_n):
            for j in range(_n):
                self.xy_wt = self.xy_wt + self.xy_wt_1( i, j)
        self.xy_wt =  _n*_n*1.0/self.xy_wt
        #
        # def fun(i, j):
        #     return self.xy_wt * (1.0-(0.5*i/_n)*(0.5*i/_n))*(1.0-(0.5*j/_n)*(0.5*j/_n))
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # x = y = numpy.arange(-_n, _n, 1.0)
        # X, Y = numpy.meshgrid(x, y)
        # zs = numpy.array(fun(numpy.ravel(X), numpy.ravel(Y)))
        # Z = zs.reshape(X.shape)
        #
        # ax.plot_surface(X, Y, Z)
        #
        # ax.set_xlabel('X Label')
        # ax.set_ylabel('Y Label')
        # ax.set_zlabel('Z Label')
        #
        # plt.show()
        # for i in range(_n):
        #     for j in range(_n):
        #         data.append([i,j,self.xy_wt * (1.0-(0.5*i/_n))*(1.0-(0.5*j/_n))])
        #         data.append([i+_n,j,self.xy_wt * (1.0-(0.5*i/_n))*(1.0-(0.5*j/_n))])
        #         data.append([i, j+_n, self.xy_wt * (1.0 - (0.5 * i / _n)) * (1.0 - (0.5 * j / _n))])
        #         data.append([i+_n, j+_n, self.xy_wt * (1.0 - (0.5 * i / _n)) * (1.0 - (0.5 * j / _n))])
        # print(len(data), len(data[0]))
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # # print(data[0,0], data)
        # ax.plot_surface(data[0], data[1], data[2])
        #
        # plt.show()

    def xy_wt_1(self, i, j):
        edge_p = 0.3
        var = 1.0 - edge_p
        xy_wt_1 = (1.0 - (var * i / self.n) * (var * i / self.n)) * (1.0 - (var * j / self.n) * (var * j / self.n))
        return xy_wt_1

    def rand_normal(self):
        _n = self.n
        for i in range(_n):
            for j in range(i+1):
                b = numpy.random.randint(0, 2)
                self.a[i, j] = b
                self.a[j, i] = b
                self.a[j, 2 * _n - 1 - i] = b
                self.a[i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - j, 2 * _n - 1 - i] = b
                self.a[2 * _n - 1 - j, i] = b
                self.a[2 * _n - 1 - i, j] = b

    def rand_modi(self, _thresh_hold):
        _n = self.n
        for i in range(_n):
            for j in range(i + 1):
                c = numpy.random.random()
                if c <_thresh_hold:
                    b=0
                else:
                    b=1
                self.a[i, j] = b
                self.a[j, i] = b
                self.a[j, 2 * _n - 1 - i] = b
                self.a[i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - j, 2 * _n - 1 - i] = b
                self.a[2 * _n - 1 - j, i] = b
                self.a[2 * _n - 1 - i, j] = b

    def rand_xy(self, _thresh_hold):
        _n = self.n
        t = 0
        for i in range(_n):
            for j in range(i + 1):
                c = numpy.random.random()
                d = self.xy_wt_1(_n-i, _n-j) * self.xy_wt

                if c*d >(1.0-_thresh_hold):
                    b=0
                    t = t + 1
                else:
                    b=1
                self.a[i, j] = b
                self.a[j, i] = b
                self.a[j, 2 * _n - 1 - i] = b
                self.a[i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - i, 2 * _n - 1 - j] = b
                self.a[2 * _n - 1 - j, 2 * _n - 1 - i] = b
                self.a[2 * _n - 1 - j, i] = b
                self.a[2 * _n - 1 - i, j] = b
        # print(2*t/(_n*_n))
        self.a[0, :] = 1.0
        self.a[:, 0] = 1.0
        self.a[:, 2*_n-1] = 1.0
        self.a[2*_n-1, :] = 1.0

    def continu(self):
        _n = self.n
        for i in range(1, 2 * _n - 1):
            for j in range(1, 2 * _n - 1):
                if (self.a[i - 1, j] == 0 and self.a[i, j - 1] == 0
                        and self.a[i, j + 1] == 0 and self.a[i + 1, j] == 0):
                    self.a[i, j] = 0

        for i in range(2*_n-1):
            for j in range(2*_n-1):
                if( self.a[i,j]==0 and self.a[i+1,j+1] == 0
                        and self.a[i,j+1] !=0 and self.a[i+1,j]!=0):
                    self.a[i, j + 1] = 0.5
                    self.a[i + 1, j] = 0.5

                if (self.a[i, j] != 0 and self.a[i + 1, j + 1] != 0
                        and self.a[i, j + 1] == 0 and self.a[i + 1, j] == 0):
                    self.a[i, j ] = 0.5
                    self.a[i + 1, j+ 1] = 0.5

    def remove_single(self):
        _n = self.n
        for i in range(1,2*_n-1):
            for j in range(1,2*_n-1):
                if( self.a[i - 1,j] == 1 and self.a[i,j - 1 ] == 1
                        and self.a[i,j + 1] ==1 and self.a[i+1,j]==1 ):
                    self.a[i, j] = 1





    def save( self, _file_name ):
        fig, ax = plt.subplots()
        ax.imshow( self.a, cmap=plt.cm.gray, interpolation='nearest',origin='upper')
        my_path = os.path.abspath("../Fig")
        my_file = "Fig_"+_file_name
        plt.savefig("./Fig/Fig_"+ _file_name )
        # os.path.join(my_path, my_file)
        my_path = os.path.abspath("../Mat")
        my_file = "Mat_" + _file_name +".txt"
        numpy.savetxt( "./Mat/Mat_"+ _file_name +".txt", self.a, fmt="%5.2f ",delimiter="," )


if __name__ == '__main__':

    for i in range(4):
        a = Meta_Surf(10)
        a.save(  str(i) )
