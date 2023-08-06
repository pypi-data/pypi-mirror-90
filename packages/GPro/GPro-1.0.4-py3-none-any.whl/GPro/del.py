from GPro.kernels import Matern
from GPro.posterior import Laplace
from GPro.acquisitions import UCB
from GPro.optimization import ProbitBayesianOptimization
from scipy.stats import multivariate_normal
import numpy as np
from sklearn import datasets
import matplotlib.cm as cm
import matplotlib.pyplot as plt

#
# # function optimization example.
# def random_sample(n, d, bounds, random_state=None):
#     # Uniform sampling given bounds.
#     if random_state is None:
#      random_state = np.random.randint(1e6)
#     random_state = np.random.RandomState(random_state)
#     sample = random_state.uniform(bounds[:, 0], bounds[:, 1],
#                               size=(n, d))
#     return sample
#
#
# def sample_normal_params(n, d, bounds, scale_sigma=1, random_state=None):
#     # Sample parameters of a multivariate normal distribution
#     # sample centroids.
#     mu = random_sample(n=n, d=d, bounds=np.array(list(bounds.values())),
#                     random_state=random_state)
#     # sample covariance matrices.
#     sigma = datasets.make_spd_matrix(d, random_state) * scale_sigma
#     theta = {'mu': mu, 'sigma': sigma}
#     return theta
#
#
# d = 2
# bounds = {'x' + str(i): (0, 10) for i in range(0, d)}
# theta = sample_normal_params(n=1, d=d, bounds=bounds, scale_sigma=10, random_state=12)
# f = lambda x: multivariate_normal.pdf(x, mean=theta['mu'][0], cov=theta['sigma'])
# # X, M, init
# X = random_sample(n=2, d=d, bounds=np.array(list(bounds.values())), random_state=2020)
# X = np.asarray(X, dtype='float64')
# M = sorted(range(len(f(X))), key=lambda k: f(X)[k], reverse=True)
# M = np.asarray([M], dtype='int16')
# GP_params = {'kernel': Matern(length_scale=1, nu=2.5),
#       'post_approx': Laplace(s_eval=1e-5, max_iter=1000,
#                              eta=0.01, tol=1e-3),
#       'acquisition': UCB(kappa=2.576),
#       'alpha': 1e-5,
#       'random_state': 2020}
# gpr_opt = ProbitBayesianOptimization(X, M, GP_params)
# function_opt = gpr_opt.function_optimization(f=f, bounds=bounds, max_iter=d*10,
#                                       n_init=1000, n_solve=1)
#
# optimal_values, X_post, M_post, f_post = function_opt
# print('optimal values: ', optimal_values)
#
# # rmse
# print('rmse: ', .5 * sum(np.sqrt((optimal_values - theta['mu'][0]) ** 2)))
# # 2d plot
# if d == 2:
#     resolution = 10
#     x_min, x_max = bounds['x0'][0], bounds['x0'][1]
#     y_min, y_max = bounds['x1'][0], bounds['x1'][1]
#     x = np.linspace(x_min, x_max, resolution)
#     y = np.linspace(y_min, y_max, resolution)
#     X, Y = np.meshgrid(x, y)
#     grid = np.empty((resolution ** 2, 2))
#     grid[:, 0] = X.flat
#     grid[:, 1] = Y.flat
#     Z = f(grid)
#     plt.imshow(Z.reshape(-1, resolution), interpolation="bicubic",
#            origin="lower", cmap=cm.rainbow, extent=[x_min, x_max, y_min, y_max])
#     plt.scatter(optimal_values[0], optimal_values[1], color='black', s=10)
#     plt.title('Target function')
#     plt.colorbar()
#     plt.show()

# 3D example. Initialization.
X = np.random.sample(size=(2, 3)) * 10
M = np.array([0, 1]).reshape(-1, 2)


GP_params = {'kernel': Matern(length_scale=1, nu=2.5),
      'post_approx': Laplace(s_eval=1e-5, max_iter=1000,
                             eta=0.01, tol=1e-3),
      'acquisition': UCB(kappa=2.576),
      'alpha': 1e-5,
      'random_state': 2020}

gpr_opt = ProbitBayesianOptimization(X, M, GP_params)

bounds = {'x0': (0, 10), 'x1': (0, 10), 'x2': (0, 10)}

console_opt = gpr_opt.interactive_optimization(bounds=bounds, n_init=100, n_solve=10)