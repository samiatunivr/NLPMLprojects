__author__ = 'samipc'

from numpy import loadtxt


def linearRegression(x_samples, y_labels):

    length = len(x_samples)
    sum_x = sum(x_samples)
    sum_y = sum(y_labels)


    sum_x_squared = sum(map(lambda a: a * a, x_samples))
    sum_of_products = sum([x_samples[i] * y_labels[i] for i in range(length)])

    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
    b = (sum_y - a * sum_x) / length
    return a, b

# lets work on some one typical example example used of linear regression(our data file has two columns: column 1 represent the
# population of a city and column two represents a profit of a shop in the city) so we our goal is to find the relationship between these
# vairabiles in order to find out which city we will be sitting our business. So our objective function is is given as h(x) = lamda_t*x;
# the lamada is the parameter of our model, and we seek to minimize the cost fuction which
#can be done using different algorithms but commonly we use gredient descent algorithm.

# here is just a simple linear regression applying the function in wikipedia (works with two variables but if we want to work with multiple variabiles
# we need to do these steps:
# substact the mean of each feature from the entire data sets X= is dataset, m_i = mean(X(:,i)) i a samples,
# divid the feature values by the std deviation to understand how these features are deviated. X(:,i)-m_i/s_i, we will have a (normalized features)



#Load the dataset
toy_data_business = loadtxt('data.txt', delimiter=',')

x = toy_data_business[:, 0]
y = toy_data_business[:, 1]
print linearRegression(x, y)  # https://en.wikipedia.org/wiki/Linear_regression

output = (1.1930336441895988, -3.8957808783119017)
