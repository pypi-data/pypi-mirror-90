import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.display import display


def unlimit_display_option(option, *args):
    """
    Wrapper for display function. It displays a DataFrame temporally
    setting an option to infinite.

    Parameters
    ----------
    option : str,
        indicates the option to be set to infinite.
    args : positional arguments,
        used as arguments of the `display` function.
    """
    current_option_value = pd.get_option(option)
    pd.set_option(option, None)
    display(*args)
    pd.set_option(option, current_option_value)


def cdisplay(*args):
    """
    Wrapper for display function. It displays  all columns of DataFrame
    objects present in `*args`
    """
    unlimit_display_option('display.max_columns', *args)


def rdisplay(*args):
    """
    Wrapper for display function. It displays  all columns of DataFrame
    objects present in `*args`
    """
    unlimit_display_option('display.max_rows', *args)

    
def percentage_count_plot(plot_srs, labels):
    """
    Draws barplot with percentages annotations calculated from
    `plot_srs`.

    Parameters
    ----------
    plot_srs : pd.Series,
        contains heighs of bars to be drawn. Percentages are calculated
        from it.
    labels : iterable
        contains the labels to be used as ticklabels on the x axis.
    """
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.bar(x=labels, height=plot_srs, 
            color=sns.color_palette(n_colors=len(plot_srs)))

    plot_srs_pct = plot_srs / plot_srs.sum()

    # Add this loop to add the annotations
    for i, (p, l) in enumerate(zip(ax.patches, labels)):
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        ax.annotate('{:.1%}'.format(plot_srs_pct.iloc[i]), 
                    (x + width / 2, y + height + 0.01), 
                    ha='center', va='bottom')
        p.set_label(l)
    plt.legend(bbox_to_anchor=(1., 1))
    
    return fig, ax