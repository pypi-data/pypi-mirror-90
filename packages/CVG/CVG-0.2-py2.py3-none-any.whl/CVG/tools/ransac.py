import numpy
import scipy # use numpy if scipy unavailable
import scipy.linalg # use numpy if scipy unavailable
import math
import numpy as np
import copy

# todo 使用RANSAC算法来筛选特征点
from CVG.geometry.glabal_homography import GloablHomography

class RANSAC:
    def __init__(self, p=0.995, epsilon=0.5, threshold=10, src_point=None, dst_point=None):
        self.p = p
        self.epsilon = epsilon
        self.threshold = threshold
        self.src_point = src_point
        self.dst_point = dst_point
        self.N = self.calculate_N()

    # 计算一共需要进行多少轮的计算
    def calculate_N(self):
        return int(math.log(1 - self.p) / math.log(1 - math.pow((1 - self.epsilon), 6) + 1e-8))

    # todo 进行ransac计算
    def ransac(self):
        src_point = copy.deepcopy(self.src_point)
        dst_point = copy.deepcopy(self.dst_point)

        src_for_err = copy.deepcopy(src_point)
        dst_point_err = copy.deepcopy(dst_point)

        # todo 最终的选出的特征点的个数
        final_num = 0
        gh = GloablHomography()
        for i in range(min(self.N, 2000)):
            # todo 选取其中的四个点
            chose_point = np.arange(len(src_point))
            np.random.shuffle(chose_point)

            new_src_array = src_point[chose_point[:6], :]
            new_dst_array = dst_point[chose_point[:6], :]

            # # todo 判断其是否共线
            # xy1 = new_src_array[0, :] - new_src_array[1, :]
            # k1 = xy1[1] / xy1[0]
            #
            # xy2 = new_src_array[2, :] - new_src_array[3, :]
            # k2 = xy2[1] / xy2[0]
            # print(k1,k2)
            # if abs(k1 - k2) < 2:
            #     continue

            cal_src = copy.deepcopy(new_src_array)
            cal_dst = copy.deepcopy(new_dst_array)
            h = gh.get_global_homo(cal_src, cal_dst)

            target = np.zeros_like(src_for_err)
            error = np.zeros_like(src_for_err)
            for j in range(src_point.shape[0]):
                target[j] = self.my_transform(src_for_err[j], h)
                error[j] = target[j] - dst_point_err[j]
            err = np.sqrt(error[:, 0] ** 2 + error[:, 1] ** 2)
            point_ok = np.where(err < self.threshold)
            if point_ok[0].shape[0] > final_num:
                final_num = point_ok[0].shape[0]
                # todo 更新循环次数,如果全都是外点的话（包括自身的4个点），
                self.epsilon = 1. - final_num / len(self.src_point)
                self.calculate_N()
                final_src_point = self.src_point[point_ok[0], :]
                final_dst_point = self.dst_point[point_ok[0], :]

        return final_num, final_src_point, final_dst_point

    def my_transform(self, point, H):
        point = np.array([point[0], point[1], 1], dtype=np.float)
        result = H.dot(point)
        result = result / result[2]
        return result[:2]

def ransac(data,model,n,k,t,d,debug=False,return_all=False):
    """fit model parameters to data using the RANSAC algorithm
    
This implementation written from pseudocode found at
http://en.wikipedia.org/w/index.php?title=RANSAC&oldid=116358182

{{{
Given:
    data - a set of observed data points
    model - a model that can be fitted to data points
    n - the minimum number of data values required to fit the model
    k - the maximum number of iterations allowed in the algorithm
    t - a threshold value for determining when a data point fits a model
    d - the number of close data values required to assert that a model fits well to data
Return:
    bestfit - model parameters which best fit the data (or nil if no good model is found)
iterations = 0
bestfit = nil
besterr = something really large
while iterations < k {
    maybeinliers = n randomly selected values from data
    maybemodel = model parameters fitted to maybeinliers
    alsoinliers = empty set
    for every point in data not in maybeinliers {
        if point fits maybemodel with an error smaller than t
             add point to alsoinliers
    }
    if the number of elements in alsoinliers is > d {
        % this implies that we may have found a good model
        % now test how good it is
        bettermodel = model parameters fitted to all points in maybeinliers and alsoinliers
        thiserr = a measure of how well model fits these points
        if thiserr < besterr {
            bestfit = bettermodel
            besterr = thiserr
        }
    }
    increment iterations
}
return bestfit
}}}
"""
    iterations = 0
    bestfit = None
    besterr = numpy.inf
    best_inlier_idxs = None
    while iterations < k:
        maybe_idxs, test_idxs = random_partition(n,data.shape[0])
        maybeinliers = data[maybe_idxs,:]
        test_points = data[test_idxs]
        maybemodel = model.fit(maybeinliers)
        test_err = model.get_error( test_points, maybemodel)
        also_idxs = test_idxs[test_err < t] # select indices of rows with accepted points
        alsoinliers = data[also_idxs,:]
        if debug:
            print('test_err.min()',test_err.min())
            print('test_err.max()',test_err.max()) 
            print( 'numpy.mean(test_err)',numpy.mean(test_err))
            print('iteration %d:len(alsoinliers) = %d'%(
                iterations,len(alsoinliers)))
        if len(alsoinliers) > d:
            betterdata = numpy.concatenate( (maybeinliers, alsoinliers) )
            bettermodel = model.fit(betterdata)
            better_errs = model.get_error( betterdata, bettermodel)
            thiserr = numpy.mean( better_errs )
            if thiserr < besterr:
                bestfit = bettermodel
                besterr = thiserr
                best_inlier_idxs = numpy.concatenate( (maybe_idxs, also_idxs) )
        iterations+=1
    if bestfit is None:
        raise ValueError("did not meet fit acceptance criteria")
    if return_all:
        return bestfit, {'inliers':best_inlier_idxs}
    else:
        return bestfit

def random_partition(n,n_data):
    """return n random rows of data (and also the other len(data)-n rows)"""
    all_idxs = numpy.arange( n_data )
    numpy.random.shuffle(all_idxs)
    idxs1 = all_idxs[:n]
    idxs2 = all_idxs[n:]
    return idxs1, idxs2

class LinearLeastSquaresModel:
    """linear system solved using linear least squares

    This class serves as an example that fulfills the model interface
    needed by the ransac() function.
    
    """
    def __init__(self,input_columns,output_columns,debug=False):
        self.input_columns = input_columns
        self.output_columns = output_columns
        self.debug = debug
    def fit(self, data):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        x,resids,rank,s = numpy.linalg.lstsq(A,B)
        return x
    def get_error( self, data, model):
        A = numpy.vstack([data[:,i] for i in self.input_columns]).T
        B = numpy.vstack([data[:,i] for i in self.output_columns]).T
        B_fit = scipy.dot(A,model)
        err_per_point = numpy.sum((B-B_fit)**2,axis=1) # sum squared error per row
        return err_per_point
        
def test():
    # generate perfect input data

    n_samples = 500
    n_inputs = 1
    n_outputs = 1
    A_exact = 20*numpy.random.random((n_samples,n_inputs) )
    perfect_fit = 60*numpy.random.normal(size=(n_inputs,n_outputs) ) # the model
    B_exact = scipy.dot(A_exact,perfect_fit)
    assert B_exact.shape == (n_samples,n_outputs)

    # add a little gaussian noise (linear least squares alone should handle this well)
    A_noisy = A_exact + numpy.random.normal(size=A_exact.shape )
    B_noisy = B_exact + numpy.random.normal(size=B_exact.shape )

    if 1:
        # add some outliers
        n_outliers = 100
        all_idxs = numpy.arange( A_noisy.shape[0] )
        numpy.random.shuffle(all_idxs)
        outlier_idxs = all_idxs[:n_outliers]
        non_outlier_idxs = all_idxs[n_outliers:]
        A_noisy[outlier_idxs] =  20*numpy.random.random((n_outliers,n_inputs) )
        B_noisy[outlier_idxs] = 50*numpy.random.normal(size=(n_outliers,n_outputs) )

    # setup model

    all_data = numpy.hstack( (A_noisy,B_noisy) )
    input_columns = range(n_inputs) # the first columns of the array
    output_columns = [n_inputs+i for i in range(n_outputs)] # the last columns of the array
    debug = True
    model = LinearLeastSquaresModel(input_columns,output_columns,debug=debug)
    
    linear_fit,resids,rank,s = numpy.linalg.lstsq(all_data[:,input_columns],all_data[:,output_columns])

    # run RANSAC algorithm
    ransac_fit, ransac_data = ransac(all_data,model,
                                     5, 5000, 7e4, 50, # misc. parameters
                                     debug=debug,return_all=True)
    if 1:
        import pylab

        sort_idxs = numpy.argsort(A_exact[:,0])
        A_col0_sorted = A_exact[sort_idxs] # maintain as rank-2 array

        if 1:
            pylab.plot( A_noisy[:,0], B_noisy[:,0], 'k.', label='data' )
            pylab.plot( A_noisy[ransac_data['inliers'],0], B_noisy[ransac_data['inliers'],0], 'bx', label='RANSAC data' )
        else:
            pylab.plot( A_noisy[non_outlier_idxs,0], B_noisy[non_outlier_idxs,0], 'k.', label='noisy data' )
            pylab.plot( A_noisy[outlier_idxs,0], B_noisy[outlier_idxs,0], 'r.', label='outlier data' )
        pylab.plot( A_col0_sorted[:,0],
                    numpy.dot(A_col0_sorted,ransac_fit)[:,0],
                    label='RANSAC fit' )
        pylab.plot( A_col0_sorted[:,0],
                    numpy.dot(A_col0_sorted,perfect_fit)[:,0],
                    label='exact system' )
        pylab.plot( A_col0_sorted[:,0],
                    numpy.dot(A_col0_sorted,linear_fit)[:,0],
                    label='linear fit' )
        pylab.legend()
        pylab.show()

if __name__=='__main__':
    test()
    
