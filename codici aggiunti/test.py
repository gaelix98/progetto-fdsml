import pandas 
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
df=pandas.read_csv("interessi_dataset.csv")

#df=df.loc[df["cluster"]==3]
#print(df)
X=df.drop(["nome"], axis=1)
scaler = MinMaxScaler()
scaler.fit(X)
X=scaler.transform(X)
print(X)
inertia = []
for i in range(1,16):
    kmeans = KMeans(n_clusters=i, init="k-means++",n_init=10,tol=1e-04, randomstate=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia)
fig = go.Figure(data=go.Scatter(x=np.arange(1,16),y=inertia))
fig.update_layout(title="Inertia vs Cluster Number",xaxis=dict(range=[0,16],title="Cluster Number"),
                  yaxis={'title':'Inertia'},
                 annotations=[
        dict(
            x=3,
            y=inertia[2],
            xref="x",
            yref="y",
            text="Elbow!",
            showarrow=True,
            arrowhead=7,
            ax=20,
            ay=-40
        )
    ])
kmeans = KMeans(
        n_clusters=3, init="k-means++",
        n_init=10,
        tol=1e-04, randomstate=42
    )
kmeans.fit(X)
clusters=pd.DataFrame(X,columns=df.drop("nome",axis=1).columns)
clusters['label']=kmeans.labels
polar=clusters.groupby("label").mean().reset_index()
polar=pd.melt(polar,id_vars=["label"])
fig4 = px.line_polar(polar, r="value", theta="variable", color="label", line_close=True,height=800,width=1400)
fig4.show()
pie=clusters.groupby('label').size().reset_index()
pie.columns=['label','value']
torta=px.pie(pie,values='value',names='label',color=['blue','red','green'])
torta.show()