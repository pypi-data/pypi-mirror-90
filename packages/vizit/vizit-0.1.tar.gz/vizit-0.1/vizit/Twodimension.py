import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from .Generalviz import Visualization

class CatCat(Visualization):
    
    """ Class for creating a visualization with two categorical variables.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variables to visualize
        var1 (string): first variable to visualize
        var2 (string): second variable to visualize
    """
    
    def __init__(self, title, data, var1, var2):
        
        Visualization.__init__(self, title, data)
        self.var1 = var1
        self.var2 = var2
        
    def __repr__(self):
        
        """Function to output the characteristics of the CatCat instance.
        
        Args:
            None
            
        Returns:
            string: characteristics of the CatCat instance
        """
        
        return 'Visualization Type: Two-Dimensional Categorical & Categorical\nTitle: {}\nVariable 1: {}\nVariable 2: {}'.format(self.title, self.var1, self.var2)
    
    def switch_var(self):
        
        """Function to change which variable is var1 and which is var2.
        
        Args:
            None
            
        Returns:
            None
        """
        
        new_var1 = self.var2
        new_var2 = self.var1
        self.var1 = new_var1
        self.var2 = new_var2
    
    def plot_clustered_bar(self, rotate=False, normalize=False, **kwargs):
        
        """Function to plot a clustered bar chart with counts or proportions, with the unique values of var1 as labels on the specified axis and unique values of var2 as different colored bars.
        
        Args:
            rotate (bool): if True, the labels are plotted on the y-axis and the counts or proportions on the x-axis
            normalize (bool): whether to plot proportions instead of counts
            **kwargs: other keyword arguments to add to seaborn.countplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.countplot(data=self.data, y=self.var1, hue=self.var2, **kwargs)
            # get the count values of the x-axis tick marks
            count_locs, _ = plt.xticks()
            if normalize:
                # divide the counts values of the x-axis tick marks by the number of records in the dataset to get proportions
                labels = ['{:.2f}'.format(i) for i in (count_locs/self.data.shape[0])]
                plt.xticks(count_locs, labels)
        else:
            sb.countplot(data=self.data, x=self.var1, hue=self.var2, **kwargs)
            # get the count values of the y-axis tick marks
            count_locs, _ = plt.yticks()
            if normalize:
                # divide the counts values of the x-axis tick marks by the number of records in the dataset to get proportions
                labels = ['{:.2f}'.format(i) for i in (count_locs/self.data.shape[0])]
                plt.yticks(count_locs, labels)
        plt.title(self.title)
        plt.show()
    
    def plot_heatmap(self, annot=True, fmt='.0f', cmap='inferno_r', cbar_kws={'label': 'count'}, **kwargs):
        
        """Function to plot a heatmap with an option for labels for the counts between the unique values of var1 and the unique values of var2.
        
        Args:
            annot (bool): whether to add labels
            fmt (string): format specifier to define how to format the labels
            cmap (string): color palette used
            cbar_kws (dict): keyword arguments for the colorbar, including the label
            **kwargs: other keyword arguments to add to seaborn.heatmap
            
        Returns:
            None
        """
        
        # format counts between var1 and var2 so they can be used in seaborn.heatmap
        count = self.data.groupby([self.var1, self.var2]).size()
        count = count.reset_index(name='count').pivot(index=self.var2, columns=self.var1, values='count')
        sb.heatmap(count, annot=annot, fmt=fmt, cmap=cmap, cbar_kws=cbar_kws, **kwargs)
        plt.title(self.title)
        plt.show()
        
    def plot_stacked_bar(self, var1_order=None, var2_order=None, rotate=False, normalize=False, **kwargs):
        
        """Function to plot a stacked bar chart with counts or proportions, with the unique values of var1 as labels on the specified axis and the unique values of var2 as different colored bars.
        
        Args:
            var1_order (list or array): order to plot the labels for var1 on the specified axis
            var2_order (list or array): order to stack the bars for var2 from bottom to top
            rotate (bool): if True, the labels are plotted on the y-axis and the counts or proportions on the x-axis
            normalize (bool): whether to plot proportions instead of counts
            **kwargs: other keyword arguments to add to matplotlib.pyplot.bar
            
        Returns:
            None
        """
        
        # retrieve unique values for var1 and var2 if no orders provided
        if var1_order is None:
            var1_order = self.data[self.var1].unique()
        if var2_order is None:
            var2_order = self.data[self.var2].unique()
        var1_counts = self.data[self.var1].value_counts()
        baselines = np.zeros(len(var1_order))
        # create list to append artists for bars that can be used to create the legend
        artists = []
        for i in range(len(var2_order)):
                category = var2_order[i]
                # find the count of var1 for each value of var2; if there is no count of var1 for that value of var2, use 0
                var1_category = self.data[self.data[self.var2] == category][self.var1].value_counts().reindex(self.data[self.var1].unique(), fill_value=0)
                if normalize:
                    var1_category = var1_category/var1_counts
                if rotate:
                    # build bars left to right
                    bars = plt.barh(y=np.arange(len(var1_order)), width=var1_category[var1_order], left=baselines, **kwargs)
                    plt.yticks(np.arange(len(var1_order)), var1_order)
                else:
                    # build bars bottom to top
                    bars = plt.bar(x=np.arange(len(var1_order)), height=var1_category[var1_order], bottom=baselines, **kwargs)
                    plt.xticks(np.arange(len(var1_order)), var1_order)
                artists.append(bars)
                baselines += var1_category[var1_order]
        plt.legend(reversed(artists), reversed(var2_order), bbox_to_anchor=[1, 0.5])
        plt.title(self.title)
        plt.show()
    
    def plot(self, kind='clustered_bar'):
        
        """Function to plot a visualization with two categorical variables.
        
        Args:
            kind (string): type of visualization to plot
            
        Returns:
            None
        """
        
        try:
            if kind == 'clustered_bar':
                self.plot_clustered_bar()
            elif kind == 'heatmap':
                self.plot_heatmap()
            elif kind == 'stacked_bar':
                self.plot_stacked_bar()
        except:
            raise ValueError("Valid values for the kind parameter include 'clustered_bar', 'heatmap', and 'stacked_bar'")

class CatNum(Visualization):
    
    """ Class for creating a visualization with one categorical variable and one numerical variable.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variables to visualize
        cat_var (string): categorical variable to visualize
        num_var (string): numerical variable to visualize
    """
    
    def __init__(self, title, data, cat_var, num_var):
        
        Visualization.__init__(self, title, data)
        self.cat_var = cat_var
        self.num_var = num_var
        
    def __repr__(self):
        
        """Function to output the characteristics of the CatNum instance.
        
        Args:
            None
            
        Returns:
            string: characteristics of the CatNum instance
        """
        
        return 'Visualization Type: Two-Dimensional Categorical & Numerical\nTitle: {}\nCategorical Variable: {}\nNumerical Variable: {}'.format(self.title, self.cat_var, self.num_var)
    
    def create_bin_size(self, bin_size, scale='linear'):
        
        """Function to create bins for num_var that will be used in visualizations, using the specified bin size.
        
        Args:
            bin_size (float): if scale is 'linear', this is the value that is added between each bin; if scale is 'log', this is the value that is multiplied between each bin
            scale (string): type of scale applied to the bins
            
        Returns:
            bins (array): bin boundaries
        """
        
        try:
            if scale == 'linear':
                bins = np.arange(self.data[self.num_var].min(), self.data[self.num_var].max()+bin_size, bin_size)
            elif scale == 'log':
                bins = 10**np.arange(np.log10(self.data[self.num_var].min()), np.log10(self.data[self.num_var].max())+np.log10(bin_size), np.log10(bin_size))
            return bins
        except:
            raise ValueError("Valid values for the scale parameter include 'linear' and 'log'")
    
    def plot_violin(self, scale='linear', rotate=False, color=sb.color_palette()[0], **kwargs):
        
        """Function to plot a violin chart with the unique values of the cat_var as labels on one axis and the distribution of the num_var on the other axis.
        
        Args:
            scale (string): type of scale applied to the distribution of num_var
            rotate (bool): if True, the labels for cat_var are plotted on the y-axis and the distribution for num_var on the x-axis
            color (tuple or string): RGB tuple or string that defines the color of the violins
            **kwargs: other keyword arguments to add to seaborn.violinplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.violinplot(data=self.data, x=self.num_var, y=self.cat_var, color=color, **kwargs)
            plt.xscale(scale)
        else:
            sb.violinplot(data=self.data, x=self.cat_var, y=self.num_var, color=color, **kwargs)
            plt.yscale(scale)
        plt.title(self.title)
        plt.show()
        
    def plot_box(self, scale='linear', rotate=False, color=sb.color_palette()[0], **kwargs):
        
        """Function to plot a box chart with the unique values of the cat_var as labels on one axis and the distribution of the num_var on the other axis.
        
        Args:
            scale (string): type of scale applied to the distribution of num_var
            rotate (bool): if True, the labels for cat_var are plotted on the y-axis and the distribution for num_var on the x-axis
            color (tuple or string): RGB tuple or string that defines the color of the boxes
            **kwargs: other keyword arguments to add to seaborn.boxplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.boxplot(data=self.data, x=self.num_var, y=self.cat_var, color=color, **kwargs)
            plt.xscale(scale)
        else:
            sb.boxplot(data=self.data, x=self.cat_var, y=self.num_var, color=color, **kwargs)
            plt.yscale(scale)
        plt.title(self.title)
        plt.show()
        
    def plot_facet(self, bins=10, scale='linear', normalize=False, height=0.9, col_wrap=3, **kwargs):
        
        """Function to plot a histogram of the distribution of num_var for each unique value in cat_var.
        
        Args:
            bins (int or array): if int, the number of bins for the specified variable; if array, the bin boundaries
            scale (string): type of scale applied to the x-axis
            normalize (bool): whether to plot proportions within each unique value of cat_var instead of counts
            height (float): fraction of the figure height to plot, leaving space for the title
            col_wrap (int): number of columns with histograms
            **kwargs: other keyword arguments to add to seaborn.displot
            
        Returns:
            None
        """
        
        # create bins if a logarithmic scale is used and bin boundaries are not specified
        if scale == 'log' and type(bins) == int:
            bins = np.logspace(np.log10(self.data[self.num_var].min()), np.log10(self.data[self.num_var].max()), bins+1)
        if normalize:
            g = sb.displot(data=self.data, x=self.num_var, col=self.cat_var, bins=bins, col_wrap=col_wrap, stat='probability', common_norm=False, **kwargs)
        else:
            g = sb.displot(data=self.data, x=self.num_var, col=self.cat_var, bins=bins, col_wrap=col_wrap, **kwargs)
        plt.xscale(scale)
        g.set_titles('{col_name}')
        # create room at the top of the visualization for the title
        plt.subplots_adjust(top=height)
        plt.suptitle(self.title)
        plt.show()
    
    def plot_bar(self, rotate=False, color=sb.color_palette()[0], ci=None, **kwargs):
        
        """Function to plot a bar chart for each unique value of cat_var with an estimate of central tendency for num_var as the height, with the default being the mean.
        
        Args:
            rotate (bool): if True, the labels for cat_var are plotted on the y-axis and the estimate of central tendency for num_var on the x-axis
            color (tuple or string): RGB tuple or string that defines the color of the bars
            ci (float or string): size of confidence intervals to plot above and below the bars
            **kwargs: other keyword arguments to add to seaborn.barplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.barplot(data=self.data, x=self.num_var, y=self.cat_var, color=color, ci=ci, **kwargs)
        else:
            sb.barplot(data=self.data, x=self.cat_var, y=self.num_var, color=color, ci=ci, **kwargs)
        plt.title(self.title)
        plt.show()
        
    def plot_point(self, rotate=False, color=sb.color_palette()[0], ci='sd', linestyles='', **kwargs):
        
        """Function to plot points for each unique value of cat_var at an estimate of central tendency for num_var, with confidence intervals above and below.
        
        Args:
            rotate (bool): if True, the labels for cat_var are plotted on the y-axis and the estimate of central tendency for num_var on the x-axis
            color (tuple or string): RGB tuple or string that defines the color of the points and confidence intervals
            ci (float or string): size of confidence intervals to plot above and below the bars
            linestyles (string): style of the line to connect the points
            **kwargs: other keyword arguments to add to seaborn.pointplot
            
        Returns:
            None
        """
        
        if rotate:
            sb.pointplot(data=self.data, x=self.num_var, y=self.cat_var, color=color, ci=ci, linestyles=linestyles, **kwargs)
        else:
            sb.pointplot(data=self.data, x=self.cat_var, y=self.num_var, color=color, ci=ci, linestyles=linestyles, **kwargs)
        plt.title(self.title)
        plt.show()
        
    def plot(self, kind='violin'):
        
        """Function to plot a visualization with one categorical variable and one numerical variable.
        
        Args:
            kind (string): type of visualization to plot
            
        Returns:
            None
        """
        
        try:
            if kind == 'violin':
                self.plot_violin()
            elif kind == 'box':
                self.plot_box()
            elif kind == 'facet':
                self.plot_facet()
            elif kind == 'bar':
                self.plot_bar()
            elif kind == 'point':
                self.plot_point()
        except:
            raise ValueError("Valid values for the kind parameter include 'violin', 'box', 'facet', 'bar', and 'point'")
        
class NumNum(Visualization):
    
    """ Class for creating a visualization with two numerical variables.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variables to visualize
        var1 (string): first variable to visualize
        var2 (string): second variable to visualize
    """
    
    def __init__(self, title, data, var1, var2):
        
        Visualization.__init__(self, title, data)
        self.var1 = var1
        self.var2 = var2
        
    def __repr__(self):
        
        """Function to output the characteristics of the NumNum instance.
        
        Args:
            None
            
        Returns:
            string: characteristics of the NumNum instance
        """
        
        return 'Visualization Type: Two-Dimensional Numerical & Numerical\nTitle: {}\nVariable 1: {}\nVariable 2: {}'.format(self.title, self.var1, self.var2)
    
    def switch_var(self):
        
        """Function to change which variable is var1 and which is var2.
        
        Args:
            None
            
        Returns:
            None
        """
        
        new_var1 = self.var2
        new_var2 = self.var1
        self.var1 = new_var1
        self.var2 = new_var2
        
    def create_bins_size(self, bins_size, scales=['linear', 'linear']):
        
        """Function to create bins for both numerical variables that will be used in visualizations, using the specified bin sizes.
        
        Args:
            bins_size (list): list with two floats; for each, if scale is 'linear', this is the value that is added between each bin; if scale is 'log', this is the value that is multiplied between each bin
            scales (list): list with two strings; each is the type of scale applied to the bins
            
        Returns:
            bins_tuple (tuple): tuple containing bin boundaries for both numerical variables
        """
    
        bins_list = []
        try:
            for i in range(2):
                if scales[i] == 'linear':
                    bins = np.arange(self.data[self.var1].min(), self.data[self.var1].max()+bins_size[i], bins_size[i])
                elif scales[i] == 'log':
                    bins = 10**np.arange(np.log10(self.data[self.var1].min()), np.log10(self.data[self.var1].max())+np.log10(bins_size[i]), np.log10(bins_size[i]))
                bins_list.append(bins)
                bins_tuple = tuple(bins_list)
            return bins_tuple
        except:
            raise ValueError("Valid values for the scale parameter include 'linear' and 'log'")
    
    def plot_scatter(self, var1_scale='linear', var2_scale='linear', **kwargs):
        
        """Function to plot a scatter pot using both numerical variables.
        
        Args:
            var1_scale (string): type of scale applied to var1 on the x-axis
            var2_scale (string): type of scale applied to var2 on the y-axis
            **kwargs: other keyword arguments to add to seaborn.regplot
            
        Returns:
            None
        """
        
        sb.regplot(data=self.data, x=self.var1, y=self.var2, **kwargs)
        plt.xscale(var1_scale)
        plt.yscale(var2_scale)
        plt.title(self.title)
        plt.show()
        
    def plot_heatmap(self, bins=[10, 10], scales=['linear', 'linear'], cbar_label='count', cmin=0.5, cmap='inferno_r', **kwargs):
        
        """Function to plot a heatmap of the counts between bins for the two numerical variables.
        
        Args:
            bins (list): list in order of var1 and var2 with int or array; if int, the number of bins; if array, the bin boundaries
            scales (list): list in order of var1 and var2 with the type of scale applied to each variable
            cbar_label (string): label for the colorbar
            cmin (float): minimum number of counts for bins to have color
            cmap (string): color palette used
            **kwargs: other keyword arguments to add to matplotlib.pyplot.hist2d
            
        Returns:
            None
        """
        
        var_list = [self.var1, self.var2]
        for i in range(2):
            # create bins if a logarithmic scale is used and bin boundaries are not specified
            if scales[i] == 'log' and type(bins[i]) == int:
                bins[i] = np.logspace(np.log10(self.data[var_list[i]].min()), np.log10(self.data[var_list[i]].max()), bins[i]+1)
        plt.hist2d(data=self.data, x=self.var1, y=self.var2, bins=bins, cmin=cmin, cmap=cmap, **kwargs)
        plt.colorbar(label=cbar_label)
        plt.xscale(scales[0])
        plt.yscale(scales[1])
        plt.title(self.title)
        plt.show()
        
    def plot_bar(self, bins=10, scale='linear', **kwargs):
        
        """Function to plot a histogram of var1 with the heights being the mean of var2 in each bin.
        
        Args:
            bins (int or array): if int, the number of bins for the specified variable; if array, the bin boundaries
            scale (string): type of scale applied to the x-axis
            **kwargs: other keyword arguments to add to matplotlib.pyplot.hist
            
        Returns:
            None
        """
        
        # create bins if a logarithmic scale is used and bin boundaries are not specified
        if scale == 'log' and type(bins) == int:
            bins = np.logspace(np.log10(self.data[self.var1].min()), np.log10(self.data[self.var1].max()*1.001), bins+1)
        # divide the records in the dataset into the specified bins
        bins_group = pd.cut(self.data[self.var1], bins, right=False, include_lowest=True, labels=False).astype(int)
        count_per_bin = self.data.groupby([bins_group]).size()
        # divide the values of var2 by the counts in each bin to get the means
        bin_weights = self.data[self.var2]/count_per_bin[bins_group].values
        plt.hist(data=self.data, x=self.var1, bins=bins, weights=bin_weights, **kwargs)
        plt.xscale(scale)
        plt.title(self.title)
        plt.show()
        
    def plot_point(self, bins=10, scale='linear', stdev=True, **kwargs):
        
        """Function to plot the mean of var2 as a point for each bin of var1, with the standard deviation above and below.
        
        Args:
            bins (int or array): if int, the number of bins for the specified variable; if array, the bin boundaries
            scale (string): type of scale applied to the x-axis
            stdev (bool): whether to plot the standard deviation above and below
            **kwargs: other keyword arguments to add to matplotlib.pyplot.errorbar
            
        Returns:
            None
        """
        
        # create bins if bin boundaries are not specified
        if scale == 'linear' and type(bins) == int:
            bins = np.linspace(self.data[self.var1].min(), self.data[self.var1].max()*1.001, bins+1)
        elif scale == 'log' and type(bins) == int:
            bins = np.logspace(np.log10(self.data[self.var1].min()), np.log10(self.data[self.var1].max()*1.001), bins+1)
        bins_center = (bins[:-1]+bins[1:])/2
        # divide the records in the dataset into the specified bins
        bins_group = pd.cut(self.data[self.var1], bins, include_lowest=True)
        # calculate the mean and standard deviation of var2 in each bin
        bins_mean = self.data.groupby([bins_group])[self.var2].mean()
        bins_std = self.data.groupby([bins_group])[self.var2].std()
        if stdev:
            plt.errorbar(x=bins_center, y=bins_mean, yerr=bins_std, **kwargs)
        else:
            plt.errorbar(x=bins_center, y=bins_mean, **kwargs)
        plt.xscale(scale)
        plt.title(self.title)
        plt.show()
        
    def plot(self, kind='scatter'):
        
        """Function to plot a visualization with two numerical variables.
        
        Args:
            kind (string): type of visualization to plot
            
        Returns:
            None
        """
        
        try:
            if kind == 'scatter':
                self.plot_scatter()
            elif kind == 'heatmap':
                self.plot_heatmap()
            elif kind == 'bar':
                self.plot_bar()
            elif kind == 'point':
                self.plot_point()
        except:
            raise ValueError("Valid values for the kind parameter include 'scatter', 'heatmap', 'bar', and 'point'")