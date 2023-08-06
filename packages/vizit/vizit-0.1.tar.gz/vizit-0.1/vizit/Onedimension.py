import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from .Generalviz import Visualization

class Cat(Visualization):
    
    """ Class for creating a visualization with one categorical variable.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variable to visualize
        var (string): variable to visualize
        counts (Series): series containing the counts of each unique value in the specified variable
    """
    
    def __init__(self, title, data, var):
        
        Visualization.__init__(self, title, data)
        self.var = var
        self.counts = self.data[self.var].value_counts()
        
    def __repr__(self):
        
        """Function to output the characteristics of the Cat instance.
        
        Args:
            None
            
        Returns:
            string: characteristics of the Cat instance
        """
        
        return 'Visualization Type: One-Dimensional Categorical\nTitle: {}\nVariable: {}'.format(self.title, self.var)
        
    def plot_bar(self, rotate=False, normalize=False, color=sb.color_palette()[0], **kwargs):
        
        """Function to plot a bar chart with counts or proportions of each unique value in the specified variable.
        
        Args:
            rotate (bool): if True, the unique values are plotted on the y-axis and the counts or proportions on the x-axis
            normalize (bool): whether to plot proportions instead of counts
            color (tuple or string): RGB tuple or string that defines the color of the bars
            **kwargs: other keyword arguments to add to seaborn.countplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.countplot(data=self.data, y=self.var, color=color, **kwargs)
            # get the count values of the x-axis tick marks
            count_locs, _ = plt.xticks()
            if normalize:
                # divide the counts values of the x-axis tick marks by the number of records in the dataset to get proportions
                labels = ['{:.2f}'.format(i) for i in (count_locs/self.data.shape[0])]
                plt.xticks(count_locs, labels)
        else:
            sb.countplot(data=self.data, x=self.var, color=color, **kwargs)
            # get the count values of the y-axis tick marks
            count_locs, _ = plt.yticks()
            if normalize:
                # divide the counts values of the x-axis tick marks by the number of records in the dataset to get proportions
                labels = ['{:.2f}'.format(i) for i in (count_locs/self.data.shape[0])]
                plt.yticks(count_locs, labels)
        plt.title(self.title)
        plt.show()
    
    def plot_pie(self, labels=None, startangle=90, counterclock=False, **kwargs):
        
        """Function to plot a pie chart with the proportions of each unique value in the specified variable.
        
        Args:
            labels (list or array): labels to add to the wedges of the pie
            startangle (float): number of degrees to rotate the start of the pie counterclockwise from the x-axis
            counterclock (bool): whether the wedges are ordered in a counterclockwise direction
            **kwargs: other keyword arguments to add to matplotlib.pyplot.pie
            
        Returns:
            None
        """
        
        if labels is None:
            labels = self.counts.index
        plt.pie(self.counts, labels=labels, startangle=startangle, counterclock=counterclock, **kwargs)
        # make the pie chart show as a circle
        plt.axis('square')
        plt.title(self.title)
        plt.show()
    
    def plot_waffle(self):
        
        """Function to plot a waffle chart with each unique value in the specified variable getting a certain number of blocks out of 100, each representing 1% of the total counts.
        
        Args:
            None
            
        Returns:
            None
        """
        
        # calculate the proportion of each unique value and multiply by 100 to get the number of blocks assigned to each unique value
        proportions = self.counts/self.data.shape[0]*100
        # keep only whole numbers of blocks
        waffle_counts = np.floor(proportions).astype(int)
        # use the remainders sorted in descending order to assign the remaining blocks
        proportions_remainder = (proportions-waffle_counts).sort_values(ascending=False)
        remaining_blocks = 100-waffle_counts.sum()
        for category in proportions_remainder.index[:remaining_blocks]:
            waffle_counts[category] += 1
        previous_count = 0
        for i in range(waffle_counts.shape[0]):
            waffle_blocks = np.arange(previous_count, previous_count+waffle_counts[i])
            # build blocks from left to right, bottom to top
            x = waffle_blocks%10
            y = waffle_blocks//10
            plt.bar(x=x, height=0.8, width=0.8, bottom=y)
            previous_count += waffle_counts[i]
        plt.legend(waffle_counts.index, bbox_to_anchor=[1, 0.5], loc=6)
        # make the chart show as a square and remove the axes
        plt.axis('square')
        plt.axis('off')
        plt.title(self.title)
        plt.show()
    
    def plot(self, kind='bar'):
        
        """Function to plot a visualization with one categorical variable.
        
        Args:
            kind (string): type of visualization to plot
            
        Returns:
            None
        """
        
        try:
            if kind == 'bar':
                self.plot_bar()
            elif kind == 'pie':
                self.plot_pie()
            elif kind == 'waffle':
                self.plot_waffle()
        except:
            raise ValueError("Valid values for the kind parameter include 'bar', 'pie', and 'waffle'")

class Num(Visualization):
    
    """ Class for creating a visualization with one numerical variable.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variable to visualize
        var (string): variable to visualize
    """

    def __init__(self, title, data, var):
    
        Visualization.__init__(self, title, data)
        self.var = var
        
    def __repr__(self):
        
        """Function to output the characteristics of the Num instance.
        
        Args:
            None
            
        Returns:
            string: characteristics of the Num instance
        """
        
        return 'Visualization Type: One-Dimensional Numerical\nTitle: {}\nVariable: {}'.format(self.title, self.var)
    
    def create_bin_size(self, bin_size, scale='linear'):
        
        """Function to create bins for the specified variable that will be used in visualizations, using the specified bin size.
        
        Args:
            bin_size (float): if scale is 'linear', this is the value that is added between each bin; if scale is 'log', this is the value that is multiplied between each bin
            scale (string): type of scale applied to the bins
            
        Returns:
            bins (array): bin boundaries
        """
        
        try:
            if scale == 'linear':
                bins = np.arange(self.data[self.var].min(), self.data[self.var].max()+bin_size, bin_size)
            elif scale == 'log':
                bins = 10**np.arange(np.log10(self.data[self.var].min()), np.log10(self.data[self.var].max())+np.log10(bin_size), np.log10(bin_size))
            return bins
        except:
            raise ValueError("Valid values for the scale parameter include 'linear' and 'log'")
             
    def plot_hist(self, bins=10, scale='linear', **kwargs):
        
        """Function to plot a histogram of the specified variable.
        
        Args:
            bins (int or array): if int, the number of bins for the specified variable; if array, the bin boundaries
            scale (string): type of scale applied to the x-axis
            **kwargs: other keyword arguments to add to matplotlib.pyplot.hist
            
        Returns:
            None
        """
    
        # create bins if a logarithmic scale is used and bin boundaries are not specified
        if scale == 'log' and type(bins) == int:
            bins = np.logspace(np.log10(self.data[self.var].min()), np.log10(self.data[self.var].max()), bins+1)
        plt.hist(data=self.data, x=self.var, bins=bins, **kwargs)
        plt.xscale(scale)
        plt.title(self.title)
        plt.show()

    def plot(self, kind='hist'):
        
        """Function to plot a visualization with one numerical variable.
        
        Args:
            kind (string): type of visualization to plot
            
        Returns:
            None
        """
        
        try:
            if kind == 'hist':
                self.plot_hist()
        except:
            raise ValueError("Valid values for the kind parameter include 'hist'")