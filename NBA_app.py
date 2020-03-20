import streamlit as st
import pandas as pd
import numpy as np


#regression packages
import sklearn.linear_model as lm
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score


#for validating your classification model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics

# feature selection
from sklearn.feature_selection import RFE

# grid search
from sklearn.model_selection import GridSearchCV

from collections import deque

st.title('WNBA Lineup Machine')
# st.title('NBA Lineup Machine')
st.markdown('_Please see left sidebar for more details._')

currentStats = pd.read_csv('https://github.com/neelganta/neel_project/edit/master/wnba19.csv') #Dynasty
# currentStats = pd.read_csv('https://raw.githubusercontent.com/neelganta/neel_project/master/2020stats_salary.csv') #Current
regModel = pd.read_csv('https://raw.githubusercontent.com/neelganta/neel_project/master/WNBAreg.csv')
regModel = regModel.fillna(0)
# regModel = regModel.drop(columns=['Unnamed: 0'])

y = regModel['NET_RATING'] 
X = regModel.drop(['NET_RATING', 'MIN', 'Unnamed: 0'], axis =1)
# Fit the model below
# model1 =  lm.LinearRegression() #higher alpha (penality parameter), fewer predictors
# model1.fit(X, y)
# model1_y = model1.predict(X)

lasso = lm.Lasso(alpha=.1)        #higher alpha (penality parameter), fewer predictors
lasso.fit(X, y)
lasso_y = lasso.predict(X)

players = []
players = currentStats['Player']
players= deque(players) 
players.appendleft('2019 WNBA Players') 
# players.appendleft('2020 NBA Players') #Current
players = list(players) 


player1 = st.selectbox('Select first player: (Example: Type "LAS" to find all Sparks)', players)
player2 = st.selectbox('Select second player: (Example: Type "PG" to find all Point Guards)', players)
player3 = st.selectbox('Select third player: (Example: Type "Alexis" to find all players with the name Alexis)', players)
player4 = st.selectbox('Select fourth player: ', players)
player5 = st.selectbox('Select fifth player: ', players)


playerlist = [player1, player2, player3, player4, player5]

# playerlist = st.multiselect("Select 5 players for your lineup: ", players)



# with st.spinner('Loading...'):
if(player1 != '2019 WNBA Players' and player2 != '2019 WNBA Players' and player3 != '2019 WNBA Players' and player4 != '2019 WNBA Players' and player5 != '2019 WNBA Players'):

# if(player1 != '2020 NBA Players' and player2 != '2020 NBA Players' and player3 != '2020 NBA Players' and player4 != '2020 NBA Players' and player5 != '2020 NBA Players'): #current
# if(len(playerlist) > 4 and len(playerlist) < 6):
    userdf = pd.DataFrame(playerlist)
    userdf['Player'] = userdf[0]

    merged = userdf.merge(right = currentStats, on ='Player')
    merged['index'] = merged[0]
    merged['index'] = 'lineup'
    merged.set_index('index')
    merged.drop(['Player'], axis =1)
    dictionary = merged.groupby('index').apply(lambda dfg: dfg.drop('index', axis=1).to_dict(orient='list')).to_dict()
    converted = pd.DataFrame.from_dict(dictionary, orient= 'index')
    WNBA_converted = pd.concat([pd.DataFrame(col.tolist()).add_prefix(i) 
                        for i,col in converted.items()],axis = 1)
    WNBA_converted.index = converted.index
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='5')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='6')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='7')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='8')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='9')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='10')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='11')))]
    WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='12')))]

    st.write('Lineup DataFrame:')
    st.write(WNBA_converted)

#     total_salary = new_df['Salary0'] + new_df['Salary1'] + new_df['Salary2']+ new_df['Salary3']+ new_df['Salary4']
#     total_salary = int(total_salary)
#     cap = 109140000
#     tax = 132627000
#     # tax_room = tax - cap
#     percent = float(total_salary / cap)
#     cap_left = cap - total_salary
#     tax_left = tax - total_salary
#     over_tax = total_salary - tax
    
#     salary_string = str(format(total_salary, ","))
#     cap_left_string = str(format(cap_left, ","))
#     over_tax_string = str(format(over_tax, ","))
#     tax_left_string = str(format(tax_left, ","))
#     if (percent < .5): 
#         st.success('The total salary for this lineup is $'+ salary_string + ', leaving $' + cap_left_string + ' left to spend on the rest of the roster.')
#     elif(percent < .99):
#         st.warning('The total salary for this lineup is $' + salary_string + ', leaving $' + cap_left_string + ' left to spend on the rest of the roster.')
#     elif(total_salary/tax > 1): 
#         st.error('The total salary for this lineup is $' + salary_string + ', putting this team over the tax by  $' + over_tax_string + '.')
#     else: 
#         st.error('The total salary for this lineup is $' + salary_string + ', putting this team in the tax and leaving $' + tax_left_string + ' left to spend on the rest of the roster.')

    with st.spinner('Loading...'):
        import itertools
        x = []
        average = []
        t=list(itertools.permutations(playerlist,len(playerlist)))
        for i in range(0,len(t)):
            x = t[i]
            userdf = pd.DataFrame(x)
            userdf['Player'] = userdf[0]

            merged = userdf.merge(right = currentStats, on ='Player')
            merged['index'] = merged[0]
            merged['index'] = 'lineup'
            merged.set_index('index')
            merged.drop(['Player'], axis =1)
            dictionary = merged.groupby('index').apply(lambda dfg: dfg.drop('index', axis=1).to_dict(orient='list')).to_dict()
            converted = pd.DataFrame.from_dict(dictionary, orient= 'index')
            WNBA_converted = pd.concat([pd.DataFrame(col.tolist()).add_prefix(i) 
                                for i,col in converted.items()],axis = 1)
            WNBA_converted.index = converted.index
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='5')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='6')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='7')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='8')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='9')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='10')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='11')))]
            WNBA_converted = WNBA_converted[WNBA_converted.columns.drop(list(WNBA_converted.filter(regex='12')))]
#             new_df = new_df[new_df.columns.drop(list(new_df.filter(regex='Salary')))]
            user_pred = lasso.predict(WNBA_converted)
            num = int(user_pred)
            average.append(num)


        
        if st.button('PREDICT'):

                # with st.spinner('Predicting...'):
                #     import time 
                #     time.sleep(3)

            avg = sum(average) / len(average)

            string = str(round(avg, 2))

            if(avg < 0):
                st.error("The predicted Net Rating for this lineup is " + string +".")
            elif (avg > 10 and avg < 20): 
                st.success("The predicted Net Rating for this lineup is " + string +".")
            elif (avg > 20):
                st.success("The predicted Net Rating for this lineup is " + string +".")
                st.balloons()
            else:
                st.warning("The predicted Net Rating for this lineup is " + string +".")





st.video(data = 'https://www.youtube.com/watch?v=le3cMnQ7_74&feature=youtu.be')
# st.markdown('_Currently the best lineup in the NBA (by at least 100 minutes played) is Paul/Gallinari/Schroder/Adams/Gilgeous-Alexander of the OKC Thunder. The NBA Net Rating Machine predicts this lineup with a Net Rating of 16.7. The bar has been set, can you beat it?_')
st.markdown('_Presented by Neel Ganta._')

st.sidebar.video(data = 'https://www.youtube.com/watch?v=le3cMnQ7_74&feature=youtu.be')
st.sidebar.markdown('**ABOUT THE WNBA LINEUP MACHINE:**  After creating the _[NBA Lineup Machine](https://nba-lineup-machine.herokuapp.com)_, which allows the user to predict the Net Rating of any lineup possible in the current NBA, Neel Ganta went about to answer a similar set of questions in regards to the WNBA. The NBA Lineup Machine was first incepted roughly one year ago while Neel Ganta was pondering the current lineup problem in the NBA. Should teams go small? Three shooters? Five? How can we see what our team would look like with a player before trading for them? Seeing a problem and no publicly available solution, Neel decided to create what could be the next big GM tool. Please enjoy the WNBA Lineup Machine which allows you to input any five players in the WNBA, and utilizes a machine learning algorithm to predict an overall Net Rating for the lineup.')
st.sidebar.markdown('_**Poor: ** Net Rating **< 0** | **Average:** Net Rating **> 0** | **Good:** Net Rating **> 5** | **Excellent:** Net Rating **> 10** | **Hall of Fame:** Net Rating **> 20**_')
st.sidebar.markdown('_Players, teams, and positions are searchable in the drop down selectors. For example: type "2012 to find all players in the year 2012. Type "CLE" to find all Cavaliers. Type "PG" to find all point guards. Type "James" to find all players with James in their name. Type "MVP" to find all MVPs from each year._')
st.sidebar.markdown('_An asterisk "*" by a player name deontes a hall of fame inductee._')

st.sidebar.markdown('**ABOUT NEEL GANTA**: Neel Ganta is graduating with a Finance and Computer Science degree from Kansas State, and completed internships at the Federal Reserve, JPMorgan Chase, the **Boston Celtics**, and currently serves as an analytics consultant for **Brad Underwood, Head Basketball Coach at the University of Illinois.** Neel grew up using his passion for basketball to connect with others, and can be found playing 5 on 5 in his local city league tournament or rec center. When he is taking a break from practicing dunks and _NBA_ three pointers, he is sharpening his machine learning skills and seeking new avenues to provide basketball insights.')
# st.sidebar.video('https://youtu.be/-OoM5XvLo20')
st.sidebar.markdown('**The Neel Ganta Fighting Illini Story:**')
st.sidebar.video(data = 'https://www.youtube.com/watch?v=Zfw0AevYR-4')
st.sidebar.markdown('**CONTACT:**')
st.sidebar.markdown('neelganta@gmail.com')
st.sidebar.markdown('https://www.linkedin.com/in/neelganta/')
st.sidebar.markdown('@lineup_machine')
