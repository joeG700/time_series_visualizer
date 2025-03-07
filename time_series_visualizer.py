import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#import data
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
#clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

#draw line plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    fig.savefig('line_plot.png')
    return fig

#draw bar plot
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month_name()
    
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().unstack()
    
    # Reorder months
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar.reindex(columns=months)
    
    fig = df_bar.plot(kind='bar', figsize=(12,6)).figure
    plt.legend(title='Months')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    fig.savefig('bar_plot.png')
    return fig

#draw a box plot
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig

if __name__ == "__main__":
    # Create and display the line plot
    line_fig = draw_line_plot()
    plt.close(line_fig)

    # Create and display the bar plot
    bar_fig = draw_bar_plot()
    plt.close(bar_fig)

    # Create and display the box plot
    box_fig = draw_box_plot()
    plt.close(box_fig)

    print("Plots have been saved as 'line_plot.png', 'bar_plot.png', and 'box_plot.png'")