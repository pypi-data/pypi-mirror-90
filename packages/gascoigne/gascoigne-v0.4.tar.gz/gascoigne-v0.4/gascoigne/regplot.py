import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


def create_df(list_of_models,model_names="none"):
    data=pd.DataFrame()
    if isinstance(list_of_models, list)==False:
        list_of_models=[list_of_models]
    if model_names=="none":
        model_names=["".join(["model_",str(v)]) for v in range(1,len(list_of_models)+2)]
    
    i=0
    for mod in list_of_models:
        # Create dataframe of results summary 
        coef_df = pd.DataFrame(mod.summary().tables[1].data)
        # Drop the extra row with column labels
        coef_df=coef_df.drop(0)
        coef_df.iloc[:,1:]=coef_df.iloc[:,1:].applymap(lambda x:float(x))
        # Add column names
        coef_df.columns=["varname","coef","std_err","t","pvalue","0.25","0.975"]
        coef_df["err"]=coef_df["coef"].apply(lambda x:float(x))-coef_df["0.25"].apply(lambda x: float(x))
        coef_df["model"]=model_names[i]
        data=data.append(coef_df)
        i+=1
    return data

def coeff_plot(data,colors="standard",marker_colors="standard",bar_colors="standard",linewidth=2,markersize=8,marker="^",legend=True,smf=True,orientation="horizontal"):

    """
    data: a pandas dataframe with four columns [coef,err,model,varname]

    colors: a unique or a list of colors for bar and markers
    marker_colors: a list of colors for markers
    bar_colors: a list of colors for bar

    linewidth:width of the bar
    markersize: size of the marker
    marker: type of marker (triangle, point, etc... see: https://matplotlib.org/3.3.3/api/markers_api.html)
    color_line: a unqque or a list of colors for bar
    legend: show legend or not
    """
    ### shape data
    if smf==False:
        if (data.columns[0:4]!=["coeff","err","model","varname"]).any()==False:
            raise Exception("columns of the dataframe are not correct. please make sure the dataframe has columns named coef, err, model and varname") 
    else:
        data=create_df(data)

    ## start plotting
    fig,axs=plt.subplots(figsize=(10,5))

    ### this is to have the name of the variable
    var_to_show=list(data["varname"].unique())

    ## index unique combinations of variables
    indx=data.loc[data["varname"].isin(var_to_show),"varname"].drop_duplicates().index

    ### the baseline plot
    if orientation=="horizontal":
        data.loc[indx,:].plot(y="coef",x="varname",kind="scatter",ax=axs,color="none")
    else:
        data.loc[indx,:].plot(x="coef",y="varname",kind="scatter",ax=axs,color="none")


    ### axis limits of the plot
    data["coef"]+data["err"]
    ax_min=(data["coef"]-data["err"]).min()*1.10
    ax_max=(data["coef"]+data["err"]).max()*1.10

    if orientation=="horizontal":
        axs.set_ylim(ax_min,ax_max)
    else:
        axs.set_xlim(ax_min,ax_max)



    ### collections of model
    list_of_model=[]
    for model in data["model"].unique():
        list_of_model.append(data.loc[data["model"]==model,:])

    ### list_of_colors
    if (colors=="standard")&(marker_colors=="standard")&(bar_colors=="standard"):
        marker_colors=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
        bar_colors=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    else:
        if colors!="standard":
            if len([colors])==1:
                marker_colors=[colors]*len(list_of_model)
                bar_colors=[colors]*len(list_of_model)

        if marker_colors!="standard":
            if bar_colors=="standard":
                bar_colors=["black"]*len(list_of_model)
            if len([marker_colors])==1:
                marker_colors=[marker_colors]*len(list_of_model)

        if bar_colors!="standard":
            if marker_colors=="standard":
                marker_colors=["black"]*len(list_of_model)
            if len([bar_colors])==1:
                bar_colors=[bar_colors]*len(list_of_model)

    ## name of model
    list_name_model=data["model"].unique()

    ### positioner
    variable_count=data.groupby("varname",as_index=False)["coef"].count()
    variable_count["even"]=variable_count["coef"]%2
    distance_between=0.1
    positioner=[]
    for i,row in variable_count.iterrows():
        ## if even
        if row["coef"]%2==0:
              positioner.append([v for v in np.arange(row.name-(row["coef"]/20)+distance_between/2,row.name+(row["coef"]/20)+0.001, distance_between)])
        else:
            positioner.append([v for v in np.arange(row.name-(row["coef"]/20)+distance_between/2,row.name+(row["coef"]/20)+0.001, distance_between)])
    variable_count["positions"]=positioner
    variable_count["counter"]=0

    

    for bar_color,mrk_color,model in zip(bar_colors,marker_colors,list_of_model):
        ### markers
        for i,row in model.iterrows():
            ## plot lines
            x_count=variable_count.loc[variable_count["varname"]==row["varname"],"counter"].iloc[0]
            x_position=variable_count.loc[variable_count["varname"]==row["varname"],"positions"].iloc[0][x_count]
            
            if orientation=="horizontal":
                ## plot bar
                axs.vlines(x=x_position,
                           ymin=row["coef"]-row["err"],
                           ymax=row["coef"]+row["err"],linewidth=linewidth,color=bar_color)
                ###  
                plt.axhline(y=0, color='grey', linestyle='--',linewidth=linewidth/2)
                #axs.hlines(y=0,xmin=-1,xmax=len(var_to_show)+0.5,linewidth=1,linestyle="--",color="grey")
                ## plot markers
                axs.plot(x_position,row["coef"], 
                         color=mrk_color, 
                         marker=marker, 
                         linestyle='dashed',linewidth=2, markersize=8)  
            else:
                ## plot bar
                axs.hlines(y=x_position,
                           xmin=row["coef"]-row["err"],
                           xmax=row["coef"]+row["err"],linewidth=linewidth,color=bar_color)
                ###  
                plt.axvline(x=0, color='grey', linestyle='--',linewidth=linewidth/2)
                #axs.hlines(y=0,xmin=-1,xmax=len(var_to_show)+0.5,linewidth=1,linestyle="--",color="grey")
                ## plot markers
                axs.plot(row["coef"],x_position, 
                         color=mrk_color, 
                         marker=marker, 
                         linestyle='dashed',linewidth=2, markersize=8)  
                
        ### update the counter
        variable_count.loc[variable_count["varname"].isin(model["varname"].unique()),"counter"]+=1

    ## create legend
    if legend==True:        
        custom_rectangles=[Rectangle((0.2,0.2,0.2),0.2,0.2,color=v) for v in marker_colors]
        axs.legend(custom_rectangles,list_name_model);
    plt.tight_layout()
    return None