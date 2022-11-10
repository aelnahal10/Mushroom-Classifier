import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score


def main():
    st.header("Classifier Web App")
    st.sidebar.title("Binary Classsification Web App")
    st.markdown("Are your mushrooms poisonous or edible ?")
    st.sidebar.markdown("Are your mushrooms poisonous or edible?")

    @st.cache(persist=True)  # use the cached data for running the data instead of loading the whole data every time
    def load_data():
        data = pd.read_csv('mushrooms.csv')
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data

    @st.cache(persist=True)  # use the cached data for running the data instead of loading the whole data every time
    def split(df):
        y = df.type
        x = df.drop('type', axis=1)

        X_train, x_test, Y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
        return X_train, x_test, Y_train, y_test

    def plot_metrics(metrics_list):
        st.set_option('deprecation.showPyplotGlobalUse', False)
        if 'Confusion Matrix' in metrics_list:
            st.subheader('Confusion Matrix')
            plot_confusion_matrix(model, x_test, y_test, display_labels=class_names)
            st.pyplot()

        if 'ROC Curve' in metrics_list:
            st.subheader('ROC curve')
            plot_roc_curve(model, x_test, y_test)
            st.pyplot()

        if 'Precision-Recall Curve' in metrics_list:
            st.subheader('Precision-Recall Curve')
            plot_precision_recall_curve(model, x_test, y_test)
            st.pyplot()

    df = load_data()

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Mushroom Classification Dataset")
        st.write(df)

    X_train, x_test, Y_train, y_test = split(df)
    class_names = ['edible', 'poisonous']
    st.sidebar.subheader("Choose Classifier")
    classifier = st.sidebar.selectbox("Classifier", (
    "Support Vector Machine", "Logistic Regression", "Random Forest"))  # dropdownlist

    if classifier == 'Support Vector Machine':
        st.sidebar.subheader("Select Model parameters")
        C = st.sidebar.number_input("C(Regularizatiion parameter)",0.01,10.0,step=0.01,key='C')
        kernel = st.sidebar.radio("Kernel",("rbf","linear"),key='kernel')
        gamma = st.sidebar.radio("Gamma (Kernel Coeeficient)",("scale","auto"),key='gamma')

        metrics = st.sidebar.multiselect("What metricss to plot",('Confusion Matrix','ROC Curve','Precision-Recall Curve'))
        if st.sidebar.button("Classify",key='classify'):
            st.subheader("Support Vector Machine (SVM) Results")
            model = SVC(C=C,kernel=kernel,gamma=gamma)
            model.fit(X_train,Y_train)
            accuarcy = model.score(x_test,y_test)
            y_predict = model.predict(x_test)
            st.write("Accuracy: ",accuarcy.round(2))
            st.write("Precision: ", precision_score(y_test,y_predict,labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test,y_predict,labels=class_names).round(2))
            plot_metrics(metrics)


    if classifier == 'Logistic Regression':
        st.sidebar.subheader("Select Model parameters")
        C = st.sidebar.number_input("C(Regularizatiion parameter)",0.01,10.0,step=0.01,key='C_lr')
        max_iter = st.sidebar.slider("Maximum no. of iterations",100,500,key='max_iter')

        metrics = st.sidebar.multiselect("What metricss to plot",('Confusion Matrix','ROC Curve','Precision-Recall Curve'))
        if st.sidebar.button("Classify",key='classify'):
            st.subheader("Logistic Regression Results")
            model = LogisticRegression()
            k = model.fit(X_train,Y_train)
            accuarcy = model.score(x_test,y_test)
            y_predict = model.predict(x_test)
            st.write("Accuracy: ",accuarcy.round(2))
            st.write("Precision: ", precision_score(y_test,y_predict,labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test,y_predict,labels=class_names).round(2))
            plot_metrics(metrics)


    if classifier == 'Random Forest':
        st.sidebar.subheader("Select Model parameters")
        estimators = st.sidebar.number_input("The number of trees in the forest is",100,1000,step=10,key='estimators')
        max_depth = st.sidebar.number_input("The max depth of the tree is",1,20,step=1,key='max_depth')
        bootStrap = st.sidebar.radio("Bootstrap samples when building trees",('True','False'),key='bootStrap')
        metrics = st.sidebar.multiselect("What metricss to plot",('Confusion Matrix','ROC Curve','Precision-Recall Curve'))
        if st.sidebar.button("Classify",key='classify'):
            st.subheader("Random Forest Results")
            model = RandomForestClassifier(n_estimators=estimators,max_depth=max_depth,bootstrap=bootStrap,n_jobs=1)
            k = model.fit(X_train,Y_train)
            accuarcy = model.score(x_test,y_test)
            y_predict = model.predict(x_test)
            st.write("Accuracy: ",accuarcy.round(2))
            st.write("Precision: ", precision_score(y_test,y_predict,labels=class_names).round(2))
            st.write("Recall: ", recall_score(y_test,y_predict,labels=class_names).round(2))
            plot_metrics(metrics)

if __name__ == '__main__':
    main()