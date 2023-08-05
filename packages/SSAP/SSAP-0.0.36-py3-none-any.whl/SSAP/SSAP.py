# ***********************************************************************************
# Author:Tony
# Create time:2020.12.08
# The software is build 4 SSAP poc testing.
# ctrl+shift+'-'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# basic introduction
def info():
    print('Welcome to SSAP! SSAP→[Self Service Analytics Platform]. There are different analytics function modules to '
          'support you complete different data analytics scenarios. Please enjoy! Any question or support needed, '
          'please raise in Big Data Community(BDC).')


# documentation for all functions and commands:
def docs():

    # print abstract:
    print(
        "[1] ssap.info()\n"
        "[2] ssap.docs()\n"
        "[3] ssap.bsfcmap(df, speed_name, torque_name, bsfc_name, title, level)\n"
        "[4] ssap.dutycycle(df, speed_name, torque_name, stepx, stepy, bubblesize, title)\n"
        "[5] ssap.dutycycle3d(df,speed_name, torque_name, barnum, title)\n"
        "[6] ssap.boxplot01(df, parameter_name, title)\n"
        "[7] ssap.boxplot02(df, title)\n"
        "[8] ssap.boxplot03(df, category_x_name, value_y_name, title)\n"
        "[9] ssap.pdsclean(df)\n"
        "[10] ssap.cmd()\n"
        "[11] ssap.dfprofile(df)\n"
        "[12] ssap.hist01(df, parameter_name, bins, title)\n"
        "[13] ssap.hist02(df1, parameter_name1, df2, parameter_name2, bins, title)\n"
        "[14] ssap.hist03(df1, parameter_name1, bins, title)\n"
        "[15] ssap.hist04(df1, parameter_name1, df2, parameter_name2, bins, title)\n"
        "[16] ssap.line01(df, x_parameter, y_parameter, title)\n"
        "[17] ssap.line02(df, x_parameter, title)\n"
        "[18] ssap.line03(df, x_parameter, y_parameter, category_parameter, title)\n"
        "[19] ssap.bar01(df, parameter_x, title)\n"
        "[20] ssap.bar01h(df, parameter_x, title)\n"
        "[21] ssap.bar02(df, parameter_x, parameter_category, title)\n"
        "[22] ssap.bar03(df, parameter_x, parameter_y, method, title) | (method(sum/mean/median,max,min,var))\n"
        "[23] ssap.bar04(df, parameter_x, parameter_y, method, title) | method(std_err,ci)\n"
        "[24] ssap.pie(df, parameter, title)\n"
        "[25] ssap.scatter01(df, parameter_x, parameter_y, title)\n"
        "[26] ssap.scatter02(df, parameter_x, parameter_y, parameter_z, bubblesize, title)\n"
        "[27] ssap.scatter03(df, parameter_x, parameter_y, category, title)\n"
        "[28] ssap.map()\n"
        "[29] ssap.map01(df, province, parameter_x, method)\n"
        "[30] ssap.scatter04hist(df, parameter_x, parameter_y, bins, title)\n"
        "[31] ssap.colorlist()\n"
        "[32] ssap.colormap()\n"
        "[33] ssap.scatter05box(df, parameter_x, parameter_y, title)\n"
    )
    # explain details:
    # print(
    #     "--------------------------------------------------------------------\n"
    #     "[Details]:\n"
    #     "[1] ssap.info() - SSAP python package description;\n"
    #
    #     "[2] ssap.docs() - All function modules and commands in SSAP package;\n"
    #
    #     "[3] ssap.bsfcmap(speed,torque,bsfc,title,level) - ICE bsfcmap chart\n"
    #     "\t ● speed:engine speed\n"
    #     "\t ● torque:engine torque\n"
    #     "\t ● bsfc:engine bfsc\n"
    #     "\t ● title:create a name for your chart\n"
    #     "\t ● level: bsfcmap boundary level matrix, define graininess for your map.\n"
    #
    #     "[4] ssap.dutycycle(speed,torque,x1,x2,stepx,y1,y2,stepy,title) - ICE duty cycle chart\n"
    #     "\t ● speed:engine speed\n"
    #     "\t ● torque:engine torque\n"
    #     "\t ● x1:speed start point\n"
    #     "\t ● x2:speed end point\n"
    #     "\t ● stepx:speed gap distance\n"
    #     "\t ● y1:torque start point\n"
    #     "\t ● y2:torque end point\n"
    #     "\t ● stepy:torque gap distance\n"
    #     "\t ● title:create a name for your chart\n"
    #
    #     "[5] ..."
    # )


# ※※other common python commands:
def cmd():
    print(
        "[1] pd.concat([df1,df2]) | 'combine df'\n"
        "[2] list(df) | 'show all column name'\n"
        "[3] df.drop_duplicates() | 'remove duplicate rows'\n"
        "[4] df.drop(['B', 'C'], axis=1) | 'delete columns'\n"
        "[5] df1 = df.loc[df['parameter name']==xxx] | 'filter dataset with conditions'\n"
        "[6] df.dropna(axis=1) | 'remove nan'\n"
        "[7] df = df.rename(columns = {'engine serial number':'esn'}) | 'change column name'\n"
        "[8] df2.sort_values(by=['xxx'],inplace=True) | 'sort values'\n"
        "[9] set(df) | 'remove duplicate for one parameter'\n"
        "[10] df['new column'] = df['existing column'] + 100 | 'add a new column' \n"
        "[11] pip show (package name)\n"
    )


# bsfcmap | 20.dec.09
def bsfcmap(df, speed_name, torque_name, bsfc_name, title, level):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = np.array(df[speed_name])
    y = np.array(df[torque_name])
    z = np.array(df[bsfc_name])
    level = level
    title = title

    xi = np.linspace(min(x), max(x), 1000)
    yi = np.linspace(min(y), max(y), 1000)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # method: nearest / linear / cubic
    plt.figure(figsize=(12, 8))
    C = plt.contour(X, Y, Z, level, colors='black', alpha=0.5)
    plt.contourf(X, Y, Z, level, alpha=.75, cmap='plasma')
    plt.colorbar()
    plt.clabel(C, inline=True, fontsize=10, colors='black')
    plt.xlabel(speed_name)
    plt.ylabel(torque_name)
    plt.title(title)
    plt.show()


# dutycycle | 20.dec.10
def dutycycle(df, speed_name, torque_name, stepx, stepy, bubblesize, title):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = df[speed_name]
    y = df[torque_name]

    x1 = int((min(x) - 200) / 100) * 100
    x2 = int((max(x) + 200) / 100) * 100
    y1 = int((min(y) - 200) / 100) * 100
    y2 = int((max(y) + 200) / 100) * 100

    xedges = [*range(x1, x2, stepx)]
    yedges = [*range(y1, y2, stepy)]

    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    hist = hist_temp.T
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.set_xticks(xedges, minor=False)
    ax.set_yticks(yedges, minor=False)

    ax.grid(which='both', color='grey', linestyle='--', alpha=0.6)

    ax.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.5)
    ax.set_xlabel(speed_name)
    ax.set_ylabel(torque_name)
    ax.set_title(title)
    plt.show()


# dutycycle3d plot | 20.dec.14
def dutycycle3d(df,speed_name, torque_name, barnum, title):
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import pandas as pd
#     %matplotlib notebook

    # define inputs.
    df = df

    x = df[speed_name]
    y = df[torque_name]
    bins = barnum
    title = title

    # basic function.
    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=bins)

    hist1 = hist_temp.T

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Construct arrays for the anchor positions of all the bars. add_subplot(111) - standard format for 3d plotting. x,y,z axis
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos1 = 0

    # Construct arrays with bar dimension
    dx = int(2 / 3 * (max(x) - min(x)) / (bins))
    dy = int(2 / 3 * (max(y) - min(y)) / (bins))

    dz1 = hist1.ravel()
    # dz2 = hist2.ravel()

    ax.bar3d(xpos, ypos, zpos1, dx, dy, dz1, zsort='average', color='skyblue', edgecolor='black', linewidth=0.3,
             alpha=0.4)
    # ax.bar3d(xpos, ypos, zpos1, dx, dy, dz2, zsort='average', color='orange',alpha=0.5)
    ax.set_xlabel('Engine Speed(rpm)')
    ax.set_ylabel('Torque(N.m)')
    ax.set_title(title)
    plt.show()


# boxplot01 (single boxplot, 1 parameter, details info) | 20.dec.14
def boxplot01(df, parameter_name, title):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df

    # data = pd.read_csv('demo.csv')
    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    #     ax1.set_xlabel(parameter_name)
    labels = [parameter_name]

    par = df[parameter_name]

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)

    B = ax1.boxplot(par, labels=labels, flierprops=red_square)
    # B = B.set(color='blue')
    x = [item.get_ydata() for item in B['whiskers']]

    # box_bdr=[]
    x1 = x[0][1]
    x2 = x[0][0]
    x3 = round(np.median(par), 2)
    x4 = x[1][0]
    x5 = x[1][1]

    box_bdr = [x1, x2, x3, x4, x5]

    for i in range(len(box_bdr)):
        plt.axhline(y=box_bdr[i], ls='--', alpha=0.5, c='darkorange', lw=1)
        plt.text(0.51, box_bdr[i], str(round(box_bdr[i], 2)), size=9, c='darkorange')

    # show mean and variation
    mean = round(np.mean(par))
    std_error = round(np.std(par))
    plt.axhline(y=mean, ls='--', alpha=0.5, c='blue', lw=1)
    plt.text(1.1, mean, '→ (mean:' + str(mean) + ' | std-err:' + str(std_error) + ')', size=9, c='blue')
    ax1.set_xticklabels(labels,rotation=45,fontsize=9)

    plt.show()


# boxplot02 (differrent parameter, same category)
def boxplot02(df, title):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    group = []
    medians = []
    std_err = []

    df = df

    # get all columns names, medians, std_errs
    for i in df.iloc[:, :].columns:
        dfi = df[i]
        group.append(dfi)
        medians.append(np.mean(df[i]))
        std_err.append(np.std(df[i]))

    # start chart layout
    fig1, ax1 = plt.subplots()

    num_boxes = len(list(df))
    pos = np.arange(num_boxes) + 1
    word_colors = ['steelblue', 'darkorange']

    # 01-show medium value
    upper_labels = ['μ:' + str(np.round(s, 1)) for s in medians]

    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        #     k = tick % 2
        ax1.text(pos[tick], .96, upper_labels[tick],
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center', size='small',
                 weight='semibold', color=word_colors[0])

    # 02-show standard error value
    upper_labels = ['σ:' + str(np.round(s, 1)) for s in std_err]

    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        #     k = tick % 2
        ax1.text(pos[tick], .93, upper_labels[tick],
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center', size='small',
                 weight='semibold', color=word_colors[1])

    # 03-change abnormal format
    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)
    bx = ax1.boxplot(group, flierprops=red_square, patch_artist=True)

    # 04-change boxplot colors:
    for patch in bx['boxes']:
        patch.set_facecolor('lightgrey')

    # 05-chart title
    ax1.set_title(title)

    # 06-change x ticks
    xticks = list(df)
    ax1.set_xticklabels(xticks, rotation=45, fontsize=8)

    # 07-add grid lines
    ax1.yaxis.grid(True)

    plt.show()


# boxplot03 (same parameter, different gategory)
def boxplot03(df, category_x_name, value_y_name, title):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    df = df

    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    group = []

    cat = list(set(df[category_x_name]))
    for i in cat:
        dfi = df.loc[df[category_x_name] == i]
        group.append(dfi[value_y_name])

    fig1, ax1 = plt.subplots()
    ax1.yaxis.grid(True)

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)
    bx = ax1.boxplot(group, flierprops=red_square, patch_artist=True)

    for patch in bx['boxes']:
        patch.set_facecolor('lightgrey')

    ax1.set_xticklabels(cat, rotation=45, fontsize=9, fontproperties=font)
    ax1.set_ylabel(value_y_name)
    plt.title(title)
    plt.show()


# pds dataset cleaning:
def pdsclean(df):
    # 1，turn '\N' into 'NaN';
    # 2.delete whole column with 'NaN';
    # 3.front fill & back fill;
    # 4.remove duplicate rows
    # (Format writing:  df=pdsclean(df))

    df = df

    # [step1]:turn \N into '' (empty value)
    for i in df.iloc[:, :].columns:
        df.loc[df[i] == '\\N', i] = 'NaN'

    # [step2]delete the whole column if any column still has na value.
    df.dropna(axis=1, how='all', inplace=True)

    # [step3]:fill empty value
    df = df.mask(df == 'NaN', None).ffill(axis=0)

    # [step4]:remove duplicate rows
    df = df.drop_duplicates()

    return df


# pandas profiling
def dfprofile(df):
    from pandas_profiling import ProfileReport
    import webbrowser

    df = df
    profile = ProfileReport(df, title='SSAP - Dataset Profile Report', html={'style': {'full_width': True}})

    profile.to_file("profile_file.html")
    url = 'profile_file.html'
    webbrowser.open(url, new=2)

    return profile


# histogram01 (simple histogram)
def hist01(df, parameter_name, bins, title):
    import matplotlib.pyplot as plt

    df = df
    x = df[parameter_name]
    bins = bins

    plt.grid(linestyle='--',lw=0.5)

    plt.hist(x, bins=bins, facecolor='steelblue', edgecolor='black', lw=0.5)
    plt.title(title)
    plt.xlabel(parameter_name)
    plt.ylabel('Counts')
    plt.show()


# histogram02 (two parameter overlap histogram)
def hist02(df1, parameter_name1, df2, parameter_name2, bins, title):
    import matplotlib.pyplot as plt
    import numpy as np

    df1 = df1
    x1 = df1[parameter_name1]

    df2 = df2
    x2 = df2[parameter_name2]

    bins = bins

    min_p = min(min(x1), min(x2))
    max_p = max(max(x1), max(x2))

    bins = np.linspace(min_p, max_p, bins + 1)

    plt.grid(linestyle='--', lw=0.5)

    plt.hist(x1, bins=bins, facecolor='purple', edgecolor='black', lw=0.5, alpha=0.7,
             label='(sample-1):' + parameter_name1)
    plt.hist(x2, bins=bins, facecolor='orange', edgecolor='black', lw=0.5, alpha=0.7,
             label='(sample-2):' + parameter_name2)

    plt.title(title)

    plt.xlabel(parameter_name1)
    plt.ylabel('Counts')
    plt.legend(loc='upper left')
    plt.show()


# histogram03 (histogram with normalized curve. mean + std_err)
def hist03(df1, parameter_name1, bins, title):
    import matplotlib.pyplot as plt
    from scipy import stats
    import numpy as np

    df1 = df1
    x1 = df1[parameter_name1]
    bins = bins

    plt.grid(linestyle='--',lw=0.5)

    # inputs for normality curve.
    lnspc1 = np.linspace(min(x1), max(x1), len(x1))
    m1, s1 = stats.norm.fit(x1)
    pdf_g1 = stats.norm.pdf(lnspc1, m1, s1)

    # hist and normality curve visuals
    plt.hist(x1, bins=bins, facecolor='steelblue', edgecolor='black', density=True, lw=0.5, alpha=0.7,
             label=parameter_name1)
    plt.plot(lnspc1, pdf_g1, label="μ1=" + str(round(m1, 2)) + ', σ1=' + str(round(s1, 2)), ls='--', color='steelblue',
             lw=1.5)

    plt.title(title)

    plt.xlabel(parameter_name1)
    plt.ylabel('Probability Density')
    plt.legend(loc='upper left')
    plt.show()


# histogram04 (two parameter overlap histogram with normalized curve. mean + std_err)
def hist04(df1, parameter_name1, df2, parameter_name2, bins, title):
    import matplotlib.pyplot as plt
    from scipy import stats
    import numpy as np

    df1 = df1
    x1 = df1[parameter_name1]
    df2 = df2
    x2 = df2[parameter_name2]
    bins = bins

    min_p = min(min(x1), min(x2))
    max_p = max(max(x1), max(x2))

    bins_new = np.linspace(min_p, max_p, bins + 1)
    plt.grid(linestyle='--',lw=0.5)

    # inputs for normality curve.
    lnspc1 = np.linspace(min(x1), max(x1), len(x1))
    m1, s1 = stats.norm.fit(x1)
    pdf_g1 = stats.norm.pdf(lnspc1, m1, s1)

    lnspc2 = np.linspace(min(x2), max(x2), len(x2))
    m2, s2 = stats.norm.fit(x2)
    pdf_g2 = stats.norm.pdf(lnspc2, m2, s2)

    # hist and normality curve visuals
    plt.hist(x1, bins=bins_new, facecolor='purple', edgecolor='black', density=True, lw=0.5, alpha=0.7,
             label='[sample-1]:' + parameter_name1)
    plt.hist(x2, bins=bins_new, facecolor='orange', edgecolor='black', density=True, lw=0.5, alpha=0.7,
             label='[sample-2]:' + parameter_name2)
    plt.plot(lnspc1, pdf_g1, label="μ1=" + str(round(m1, 2)) + ', σ1=' + str(round(s1, 2)), ls='--', color='purple',
             lw=1.5)
    plt.plot(lnspc2, pdf_g2, label="μ2=" + str(round(m2, 2)) + ', σ2=' + str(round(s2, 2)), ls='--', color='orange',
             lw=1.5)

    plt.title(title)

    plt.xlabel(parameter_name1)
    plt.ylabel('Probability Density')
    plt.legend(loc='upper left')
    plt.show()


# line chart01-(single line chart)
def line01(df, x_parameter, y_parameter, title):
    df2 = df
    df2.sort_values(by=[x_parameter], inplace=True)

    plt.grid(linestyle='--', lw=0.5)
    x1 = df2[x_parameter]
    y1 = df2[y_parameter]

    plt.plot(x1, y1, 'o--', color='steelblue', alpha=0.8, linewidth=2, ms=6, mfc='white', mew=1, mec='black')

    plt.title(title)
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.show()


# line chart02-(multiple line chart - many parameters. dataset contain 1 x-axis value, rest columns are numbers)
def line02(df, x_parameter, title):
    df2 = df
    df2.sort_values(by=[x_parameter], inplace=True)
    x = df2[x_parameter]

    df2 = df2.drop([x_parameter], axis=1)
    plt.grid(linestyle='--', lw=0.5)

    labels = list(df2)

    colorindex = ['steelblue', 'darkorange', 'purple', 'grey', 'blue', 'seagreen', 'magenta']
    k = 0

    # loop numercial columns
    for i in df2.iloc[:, :].columns:
        yi = df[i]
        plt.plot(x, yi, 'o--', color=colorindex[k], alpha=0.8,
                 linewidth=2, ms=6, mfc='white', mew=1, mec=colorindex[k], label=labels[k])
        k += 1

    plt.title(title)
    plt.xlabel(x_parameter)
    plt.legend(loc='upper left')
    plt.show()


# line chart03-(mutiple line chart - one x, one y. labeled by categories.)
def line03(df, x_parameter, y_parameter, category_parameter, title):
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    df2 = df[[x_parameter, y_parameter, category_parameter]]

    title = title
    labels = list(set(df2[category_parameter]))
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    colorindex = ['steelblue', 'darkorange', 'purple', 'grey', 'blue', 'seagreen',
                  'magenta', 'brown', 'yellow']
    k = 0
    plt.grid(linestyle='--', lw=0.5)

    for i in labels:
        dfi = df2.loc[df2[category_parameter] == i]
        dfi.sort_values(by=[x_parameter], inplace=True)

        xi = dfi[x_parameter]
        yi = dfi[y_parameter]

        plt.plot(xi, yi, 'o--', color=colorindex[k], alpha=0.8,
                 linewidth=2, ms=6, mfc='white', mew=1, mec=colorindex[k],
                 label=labels[k])
        k = k + 1

    plt.title(title)
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.legend(loc='upper left', prop=font)
    plt.show()


# bar01 - single category(string). Vertical bar. y=count.
def bar01(df, parameter_x, title):  # single category
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.font_manager as fm

    df = df
    title = title
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    df[parameter_x].astype(str)
    label = list(set(df[parameter_x]))
    y = []

    plt.grid(linestyle='--', lw=0.5)

    x_pos = [i for i, _ in enumerate(label)]
    #     print(x_pos)

    for i in label:
        ypos = df[parameter_x].tolist().count(i)
        y.append(ypos)

    plt.bar(x_pos, y, color='steelblue', edgecolor='black', lw=1, alpha=0.9)
    plt.xlabel(parameter_x)
    plt.ylabel('Counts')
    plt.xticks(x_pos, label, rotation=45, fontproperties=font)
    plt.title(title)
    plt.show()


# bar01h - single category(string). Horizontal bar. y=count.
def bar01h(df, parameter_x, title):  # single category
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.font_manager as fm

    df = df
    title = title
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    df[parameter_x].astype(str)
    label = list(set(df[parameter_x]))
    y = []

    plt.grid(linestyle='--', lw=0.5)

    x_pos = [i for i, _ in enumerate(label)]
    #     print(x_pos)

    for i in label:
        ypos = df[parameter_x].tolist().count(i)
        y.append(ypos)

    plt.barh(x_pos, y, color='steelblue', edgecolor='black', lw=1, alpha=0.9)
    plt.ylabel(parameter_x)
    plt.xlabel('Counts')
    plt.yticks(x_pos, label, fontproperties=font)
    plt.title(title)
    plt.show()


# bar02 - two category(string). y=count.
def bar02(df, parameter_x, parameter_category, title):  # two categories. y=count.
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.font_manager as fm

    global list  # "list is local variable / list is not callable etc issues."

    df = df
    title = title
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')
    df2 = df[[parameter_x, parameter_category]]

    labelx = list(set(df2[parameter_x]))
    labelc = list(set(df2[parameter_category]))
    #     print(labelc)

    ind = np.array(len(labelx))
    y = []
    valuepool = []

    for i in labelx:
        for j in range(len(labelc)):
            z = []
        for k in labelc:
            zpos = df[parameter_category].loc[df[parameter_x] == i].tolist().count(k)
            z.append(zpos)
        valuepool.append(z)

    source = valuepool

    step = 1
    n = len(labelc)
    k = 1
    #     print(source)
    for i in range(len(source[0])):
        #         test={}
        listx = []
        for j in range(len(source)):
            val = source[j][i]
            listx.append(val)
        #         test["col{0}".format(i)] = listx
        #         rst = pd.DataFrame(test)
        #         s = rst.iloc[:,0]
        #         s.tolist()

        #         print(len(s))
        #         print(listx)

        N = len(labelx)
        ind = np.arange(N)
        width = 0.85 / n
        plt.bar(ind + (k - 1) * width, listx, width, label=labelc[i], edgecolor='black')
        k += 1
    #         print(k)

    plt.grid(linestyle='--', lw=0.5)

    plt.xticks(ind + (n - 1) * width / 2, (labelx), rotation=45, fontproperties=font)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_category)
    plt.title(title)

    plt.legend(loc='upper left', prop=font)
    plt.show()


# bar03 - one category, one numerical. y=numbers. simple functions method(sum/mean/median,max,min,var)
def bar03(df, parameter_x, parameter_y, method, title):  # single category
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.font_manager as fm

    df = df
    title = title
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    df[parameter_x].astype(str)
    label = list(set(df[parameter_x]))
    y = []

    method = method
    plt.grid(linestyle='--', lw=0.5,axis='y')

    x_pos = [i for i, _ in enumerate(label)]
    #         print(x_pos)

    for i in label:
        temp = df[parameter_y].loc[df[parameter_x] == i]
        #         print(temp)
        #         print(temp.tolist())
        temp = temp.tolist()

        # define method:
        if method == 'sum':
            ypos = np.sum(temp)
        elif method == 'mean':
            ypos = np.mean(temp)
        elif method == 'max':
            ypos = np.max(temp)
        elif method == 'min':
            ypos = np.min(temp)
        elif method == 'median':
            ypos = np.median(temp)
        elif method == 'var':
            ypos = np.var(temp)

        y.append(ypos)
    #         print(y)

    plt.bar(x_pos, y, color='skyblue', edgecolor='black', label=parameter_y + ' (' + method + ')', lw=0.9, alpha=1)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y + ' (' + method + ')')
    plt.legend(loc='upper left')
    plt.xticks(x_pos, label, rotation=45, fontproperties=font)
    plt.title(title)
    plt.show()


# bar04 - one category, one numerical, y=numbers. error bar function (method(std_err,ci). Var, CI 95% confidential interval)
def bar04(df, parameter_x, parameter_y, method, title):  # single category
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.font_manager as fm
    import scipy.stats as st

    df = df
    title = title
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    df[parameter_x].astype(str)
    label = list(set(df[parameter_x]))
    y_mean = []
    y_err = []

    method = method
    plt.grid(linestyle='--', lw=0.5, axis='y')

    x_pos = [i for i, _ in enumerate(label)]
    #         print(x_pos)

    for i in label:
        temp = df[parameter_y].loc[df[parameter_x] == i]
        #         print(temp)
        #         print(temp.tolist())
        temp = temp.tolist()
        y_mean_temp = np.mean(temp)

        if method == 'std_err':
            y_err_temp = np.std(temp)
            labelx = parameter_y + ' (std_err)'


        elif method == 'ci':
            a = st.norm.interval(alpha=0.95, loc=np.mean(temp), scale=st.sem(temp))
            y_err_temp = a[1] - a[0]

            labelx = parameter_y + ' (95% CI)'

        y_mean.append(y_mean_temp)
        y_err.append(y_err_temp)
    #         print(y)

    plt.bar(x_pos, y_mean, color='skyblue', edgecolor='black', yerr=y_err, capsize=7, label=labelx, lw=0.9, alpha=1)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y + ' (' + method + ')')
    plt.legend(loc='upper left')
    plt.xticks(x_pos, label, rotation=45, fontproperties=font)
    plt.title(title)
    plt.show()


# pie chart - one category parameter.
def pie(df, parameter, title):
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    from matplotlib import cm
    import numpy as np

    df1 = df
    title = title
    labelx = list(set(df1[parameter]))
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    y = []
    for i in labelx:
        y_temp = df1[parameter].tolist().count(i)
        y.append(y_temp)

    fig1, ax1 = plt.subplots()

    colormap = plt.cm.Blues
    numberOfSlices = len(labelx)
    sliceColors = colormap(np.linspace(0., 1., numberOfSlices))

    wedgeprops = {"linewidth": 2, 'width': 1, "edgecolor": "white"}  # Width = 1
    textprops = {"fontproperties": font, 'fontsize': 12}
    colors = ["c", 'b', 'r', 'y', 'g']

    ax1.pie(y,
            labels=labelx,
            autopct='%1.2f%%',
            pctdistance=0.7,
            shadow=True,
            radius=1.2,
            counterclock=True,
            startangle=90,
            wedgeprops=wedgeprops,
            textprops=textprops,
            colors=sliceColors,
            )

    ax1.axis('equal')
    plt.title(title, )
    plt.show()


# scatter chart 01 - basics
def scatter01(df, parameter_x, parameter_y, title):
    df = df
    x = df[parameter_x].tolist()
    y = df[parameter_y].tolist()
    fig, ax = plt.subplots()
    scatter = ax.scatter(x=x, y=y, edgecolor='black', lw=0.5, alpha=0.7, facecolor='orange')
    plt.grid(linestyle='--', lw=0.5)

    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    plt.title(title)
    plt.show()


# scatter chart 02 - basic bubble plot
def scatter02(df, parameter_x, parameter_y, parameter_z, bubblesize, title):
    df = df
    x = df[parameter_x].tolist()
    y = df[parameter_y].tolist()
    s = (df[parameter_z] / bubblesize).tolist()
    #     s1 = s/100

    fig, ax = plt.subplots()
    scatter = ax.scatter(x=x, y=y, s=s, edgecolor='black', lw=0.5, alpha=0.8, facecolor='orange')
    plt.grid(linestyle='--', lw=0.5)

    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # size elements
    handles, labels = scatter.legend_elements(prop="sizes", alpha=0.5)
    legend2 = ax.legend(handles, labels, loc="lower right", title='size * ' + str(bubblesize), )

    # plt.legend()
    plt.title(title)
    plt.show()


# scatter chart 03 - scatter plot + color(category)
def scatter03(df, parameter_x, parameter_y, category, title):
    import matplotlib.font_manager as fm
    import matplotlib.pyplot as plt

    df = df
    font = fm.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

    catlist = list(set(df[category]))

    fig, ax = plt.subplots()
    plt.grid(linestyle='--', lw=0.5)
    k = 0

    colormap = plt.cm.plasma
    numberOfSlices = len(catlist)
    sliceColors = colormap(np.linspace(0., 1., numberOfSlices))

    for i in catlist:
        x = df[parameter_x].loc[df[category] == i].tolist()
        y = df[parameter_y].loc[df[category] == i].tolist()
        scatter = ax.scatter(x=x, y=y, c=sliceColors[k], label=i, edgecolor='black', lw=0.5, alpha=0.7,
                             facecolor='orange')
        k += 1

    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # size elements
    handles, labels = scatter.legend_elements(prop="sizes", alpha=0.5)
    legend2 = ax.legend(handles, labels, loc="lower right", title='size')

    plt.legend(prop=font)
    plt.title(title)
    plt.show()


# empty map:
def map():
    import folium
    import webbrowser

    m = folium.Map(location=[39.9, 116.4])
    m.save('ssap_map.html')
    url = 'ssap_map.html'
    webbrowser.open(url, new=2)
    return m


# map with value method(max,min,mean,median,sum,std_err)
def map01(df, province, parameter_x, method):
    import matplotlib.pyplot as plt
    import numpy as np
    import folium
    import pandas as pd
    import webbrowser

    # References:
    # https://gitee.com/riverscn/china-geojson/blob/master/china.json
    # https://geojson.io/#map=3/31.73/104.24
    # https://python-visualization.github.io/folium/modules.html#module-folium.map

    df = df
    df1 = df[[province, parameter_x]]

    category = list(set(df1[province]))
    value = []

    for i in category:
        temp = df[parameter_x].loc[df[province] == i]
        temp = temp.tolist()

        if method == 'sum':
            temp1 = np.sum(temp)
        elif method == 'median':
            temp1 = np.median(temp)
        elif method == 'std':
            temp1 = np.std(temp)
        elif method == 'max':
            temp1 = np.max(temp)
        elif method == 'min':
            temp1 = np.min(temp)
        else:
            temp1 = np.var(temp)

        value.append(temp1)

    dfnew = pd.DataFrame(
        {
            'province': category,
            'value': value,
        }
    )

    print(dfnew)

    pdsmap = folium.Map(location=[35, 120], zoom_start=4)
    pdsmap.choropleth(
        geo_data=open('china.json', encoding='utf-8-sig').read(),
        data=dfnew,
        columns=['province', 'value'],
        key_on='feature.properties.name',
        fill_color='Greens',
        nan_fill_color='lightgrey',
        fill_opacity=0.8,
        nan_fill_opacity=0.1,
        line_color='grey',
        line_opacity=0.2,
        legend_name='[PDS_Map] distribution for: ' + parameter_x + ' (' + method + ')',
        highlight=True,
    )

    pdsmap.save('PDS_Map.html')
    url = 'PDS_Map.html'
    webbrowser.open(url, new=2)
    # display(pdsmap)


# scatter plot + hist plot on top/right.
def scatter04hist(df, parameter_x, parameter_y, bins, title):
    import matplotlib.pyplot as plt

    df = df
    x = df[parameter_x]
    y = df[parameter_y]
    title = title

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    # scatter plot
    ax_scatter = plt.axes(rect_scatter)
    plt.grid(linestyle='--', lw=0.5)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # top hist
    ax_histx = plt.axes(rect_histx)
    plt.grid(linestyle='--', lw=0.5, axis='y')
    ax_histx.tick_params(direction='in', labelbottom=False)
    plt.xlabel(parameter_x)
    plt.ylabel('Counts')
    plt.title(title)

    # right hist
    ax_histy = plt.axes(rect_histy)
    plt.grid(linestyle='--', lw=0.5, axis='x')
    ax_histy.tick_params(direction='in', labelleft=False)
    plt.xlabel('Counts')
    plt.ylabel(parameter_y)

    # the scatter plot:
    ax_scatter.scatter(x, y, edgecolor='black', lw=0.5, alpha=0.7, facecolor='darkorange')

    bins = bins

    # now determine nice limits by hand:
    ax_histx.hist(x, bins=bins, edgecolor='black', facecolor='darkorange', alpha=0.7)
    ax_histy.hist(y, bins=bins, orientation='horizontal', edgecolor='black', facecolor='darkorange', alpha=0.7)

    ax_histx.set_xlim(ax_scatter.get_xlim())
    #     ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()


# show colormap detail:
def colormap():
    import numpy as np
    import matplotlib.pyplot as plt


    cmaps = [('Perceptually Uniform Sequential', [
                'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
             ('Sequential', [
                'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
             ('Sequential (2)', [
                'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
                'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
                'hot', 'afmhot', 'gist_heat', 'copper']),
             ('Diverging', [
                'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
             ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
             ('Qualitative', [
                'Pastel1', 'Pastel2', 'Paired', 'Accent',
                'Dark2', 'Set1', 'Set2', 'Set3',
                'tab10', 'tab20', 'tab20b', 'tab20c']),
             ('Miscellaneous', [
                'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))


    def plot_color_gradients(cmap_category, cmap_list):
        # Create figure and adjust figure height to number of colormaps
        nrows = len(cmap_list)
        figh = 0.35 + 0.15 + (nrows + (nrows-1)*0.1)*0.22
        fig, axes = plt.subplots(nrows=nrows, figsize=(6.4, figh))
        fig.subplots_adjust(top=1-.35/figh, bottom=.15/figh, left=0.2, right=0.99)

        axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

        for ax, name in zip(axes, cmap_list):
            ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
            ax.text(-.01, .5, name, va='center', ha='right', fontsize=10,
                    transform=ax.transAxes)

        # Turn off *all* ticks & spines, not just the ones with colormaps.
        for ax in axes:
            ax.set_axis_off()


    for cmap_category, cmap_list in cmaps:
        plot_color_gradients(cmap_category, cmap_list)

    plt.show()


# show colorbar detail:
def colorlist():

    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors


    def plot_colortable(colors, title, sort_colors=True, emptycols=0):

        cell_width = 212
        cell_height = 22
        swatch_width = 48
        margin = 12
        topmargin = 40

        # Sort colors by hue, saturation, value and name.
        if sort_colors is True:
            by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                             name)
                            for name, color in colors.items())
            names = [name for hsv, name in by_hsv]
        else:
            names = list(colors)

        n = len(names)
        ncols = 4 - emptycols
        nrows = n // ncols + int(n % ncols > 0)

        width = cell_width * 4 + 2 * margin
        height = cell_height * nrows + margin + topmargin
        dpi = 72

        fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
        fig.subplots_adjust(margin/width, margin/height,
                            (width-margin)/width, (height-topmargin)/height)
        ax.set_xlim(0, cell_width * 4)
        ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.set_axis_off()
        ax.set_title(title, fontsize=24, loc="left", pad=10)

        for i, name in enumerate(names):
            row = i % nrows
            col = i // nrows
            y = row * cell_height

            swatch_start_x = cell_width * col
            swatch_end_x = cell_width * col + swatch_width
            text_pos_x = cell_width * col + swatch_width + 7

            ax.text(text_pos_x, y, name, fontsize=14,
                    horizontalalignment='left',
                    verticalalignment='center')

            ax.hlines(y, swatch_start_x, swatch_end_x,
                      color=colors[name], linewidth=18)

        return fig

    plot_colortable(mcolors.BASE_COLORS, "Base Colors",
                    sort_colors=False, emptycols=1)
    plot_colortable(mcolors.TABLEAU_COLORS, "Tableau Palette",
                    sort_colors=False, emptycols=2)

    #sphinx_gallery_thumbnail_number = 3
    plot_colortable(mcolors.CSS4_COLORS, "CSS Colors")

    # Optionally plot the XKCD colors (Caution: will produce large figure)
    #xkcd_fig = plot_colortable(mcolors.XKCD_COLORS, "XKCD Colors")
    #xkcd_fig.savefig("XKCD_Colors.png")
    plt.show()


# scatter plot + box plot on top/right.
def scatter05box(df, parameter_x, parameter_y, title):
    import matplotlib.pyplot as plt

    df = df
    x = df[parameter_x]
    y = df[parameter_y]
    title = title

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.08]
    rect_histy = [left + width + spacing, bottom, 0.08, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    # scatter plot
    ax_scatter = plt.axes(rect_scatter)
    plt.grid(linestyle='--', lw=0.5)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # top hist
    ax_histx = plt.axes(rect_histx)
    plt.grid(linestyle='--', lw=0.5, axis='y')
    ax_histx.tick_params(direction='in', labelbottom=False)
    plt.xlabel(parameter_x)
    #     plt.ylabel('Counts')
    plt.title(title)

    # right hist
    ax_histy = plt.axes(rect_histy)
    plt.grid(linestyle='--', lw=0.5, axis='x')
    ax_histy.tick_params(direction='in', labelleft=False)
    #     plt.xlabel('Counts')
    plt.ylabel(parameter_y)

    # the scatter plot:
    ax_scatter.scatter(x, y, edgecolor='black', lw=0.5, alpha=0.7, facecolor='darkorange')

    # now determine nice limits by hand:
    #     ax_histx.hist(x, bins=bins,edgecolor='black',facecolor='darkorange',alpha=0.7)
    #     ax_histy.hist(y, bins=bins, orientation='horizontal',edgecolor='black',facecolor='darkorange',alpha=0.7)

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)

    x = ax_histx.boxplot(x, flierprops=red_square, vert=False, widths=0.5, patch_artist=True)
    for patch in x['boxes']:
        patch.set_facecolor('orange')

    y = ax_histy.boxplot(y, flierprops=red_square, widths=0.5, patch_artist=True)
    for patch in y['boxes']:
        patch.set_facecolor('orange')

    #     ax_histx.set_xlim(ax_scatter.get_xlim())
    #     ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [to be validated. update:12/28]
# scatter plot + hist plot + linear regression
def scatter06histlr(df, parameter_x, parameter_y, bins, title):
    import matplotlib.pyplot as plt
    from scipy.stats import linregress
    import numpy as np

    df = df
    x = df[parameter_x]
    y = df[parameter_y]
    lr = linregress(x, y)
    title = title

    lr_label = '[L.R] y = ' + str("{0:.3g}".format(lr[0])) + ' *x + ' + str("{0:.3g}".format(lr[1])) + ' (r=' + str(
        "{0:.3g}".format(lr[2])) + '|p=' + str("{0:.3g}".format(lr[3])) + '|σ=' + str("{0:.3g}".format(lr[4])) + ')'

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    # scatter plot
    ax_scatter = plt.axes(rect_scatter)
    plt.grid(linestyle='--', lw=0.5)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # top hist
    ax_histx = plt.axes(rect_histx)
    plt.grid(linestyle='--', lw=0.5, axis='y')
    ax_histx.tick_params(direction='in', labelbottom=False)
    plt.xlabel(parameter_x)
    plt.ylabel('Counts')
    plt.title(title)

    # right hist
    ax_histy = plt.axes(rect_histy)
    plt.grid(linestyle='--', lw=0.5, axis='x')
    ax_histy.tick_params(direction='in', labelleft=False)
    plt.xlabel('Counts')
    plt.ylabel(parameter_y)

    # the scatter plot:
    ax_scatter.scatter(x, y, edgecolor='black', lw=0.5, alpha=0.7, facecolor='darkorange')

    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)
    ax_scatter.plot(x, poly1d_fn(x), '-', lw=1, color='blue', label=lr_label)
    ax_scatter.legend(loc='lower left')

    bins = bins

    # now determine nice limits by hand:
    ax_histx.hist(x, bins=bins, edgecolor='black', facecolor='darkorange', alpha=0.7)
    ax_histy.hist(y, bins=bins, orientation='horizontal', edgecolor='black', facecolor='darkorange', alpha=0.7)

    ax_histx.set_xlim(ax_scatter.get_xlim())
    #     ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()


# scatter plot + boxplot + linear regression
def scatter07boxlr(df, parameter_x, parameter_y, title):
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import linregress

    df = df
    x = df[parameter_x]
    y = df[parameter_y]

    lr = linregress(x, y)
    title = title

    lr_label = '[L.R] y = ' + str("{0:.3g}".format(lr[0])) + ' *x + ' + str("{0:.3g}".format(lr[1])) + ' (r=' + str(
        "{0:.3g}".format(lr[2])) + '|p=' + str("{0:.3g}".format(lr[3])) + '|σ=' + str("{0:.3g}".format(lr[4])) + ')'
    #     print(lr_label)

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.08]
    rect_histy = [left + width + spacing, bottom, 0.08, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    # scatter plot
    ax_scatter = plt.axes(rect_scatter)
    plt.grid(linestyle='--', lw=0.5)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # top hist
    ax_histx = plt.axes(rect_histx)
    plt.grid(linestyle='--', lw=0.5, axis='y')
    ax_histx.tick_params(direction='in', labelbottom=False)
    plt.xlabel(parameter_x)
    #     plt.ylabel('Counts')
    plt.title(title)

    # right hist
    ax_histy = plt.axes(rect_histy)
    plt.grid(linestyle='--', lw=0.5, axis='x')
    ax_histy.tick_params(direction='in', labelleft=False)
    #     plt.xlabel('Counts')
    plt.ylabel(parameter_y)
    # the scatter plot:
    ax_scatter.scatter(x, y, edgecolor='black', lw=0.5, alpha=0.7, facecolor='darkorange')

    #     print(ploy1d_fn(x))
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)
    ax_scatter.plot(x, poly1d_fn(x), '-', lw=1, color='blue', label=lr_label)
    ax_scatter.legend(loc='lower left')

    # now determine nice limits by hand:
    #     ax_histx.hist(x, bins=bins,edgecolor='black',facecolor='darkorange',alpha=0.7)
    #     ax_histy.hist(y, bins=bins, orientation='horizontal',edgecolor='black',facecolor='darkorange',alpha=0.7)

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)

    x = ax_histx.boxplot(x, flierprops=red_square, vert=False, widths=0.5, patch_artist=True)
    for patch in x['boxes']:
        patch.set_facecolor('orange')

    y = ax_histy.boxplot(y, flierprops=red_square, widths=0.5, patch_artist=True)
    for patch in y['boxes']:
        patch.set_facecolor('orange')

    #     ax_histx.set_xlim(ax_scatter.get_xlim())
    #     ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()




# show correlation line + error zone. with scatter plot:


# [planning ↓]

# heatmap() / correlation map
# Line plot (x-时间序列: 4.移动平均图 Arima  5.时间序列预测 等种种）
# my.data analytics ppt里的图表
# 多因子相关性矩阵图/
# SSAP用户报告里绘制的图
# 多项式回归拟合
# 聚类算法 DBSCAN.
# regression model: