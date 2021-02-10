import pandas as pd
from git import Repo


path='/home/mayijun/GITHUB/td-plotly'
df=pd.DataFrame()
df['a']=range(0,10)
df['b']=range(1,11)
df.to_csv(path+'/df.csv')


def git_push():
    try:
        repo = Repo(path)
        repo.git.add('df.csv')
        repo.index.commit('autoupdate')
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()

