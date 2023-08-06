import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
    """
        
    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size
        mean = self.calculate_mean()
        stdev = self.calculate_stdev()
        
        Distribution.__init__(self, mean, stdev)
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """                
        n = self.n
        p = self.p
        mean = n * p
        self.mean = mean
        
        return mean

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        n = self.n
        p = self.p
        stdev = math.sqrt(n*p*(1-p))
        self.stdev = stdev
        
        return stdev
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """                
        n = len(self.data)
        p = sum(self.data) / n
        self.n = n
        self.p = p
        self.mean = n * p
        self.stdev = math.sqrt(n*p*(1-p))
        
        return p, n
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        total_1 = sum(self.data)
        total_0 = self.n - total_1
        
        plt.bar(x=[0, 1], y=[total_0, total_1])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        n = self.n
        p = self.p
        
        binomial_coefficient = math.factorial(n) / (math.factorial(k)*math.factorial(n-k))
        probability = binomial_coefficient * (p**k) * ((1-p)**(n-k))
                             
        return probability

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """        
        x = [k for k in range(0, self.n+1)] # List of values of k
        y = [self.pdf(k) for k in x] # List of PDF of k
        
        plt.bar(x=x, y=y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y
        
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        # Accept only binomial distributions with the same value of p
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        n_total = self.n + other.n
        result = Binomial(prob=self.p, size=n_total)
        
        return result
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """

        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
