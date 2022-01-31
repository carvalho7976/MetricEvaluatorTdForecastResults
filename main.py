from numpy import NaN
import pandas as pd
from sklearn import datasets





if __name__ == '__main__':
    #CSV HEAD
    #EXP PROJECT VERSIONS_AHEAD CONFIG FIT_MEAN FIT_STD SCORE_MEAN SCORE_STD MAE RMSE MAPE R2 
    DATASET = ['apache_groovy_measures',
                'apache_incubator_dubbo_measures',
                'apache_kafka_measures',
                'apache_nifi_measures',
                'apache_ofbiz_measures',
                'apache_systemml_measures',
                'google_guava_measures',
                'igniterealtime_openfire_measures',
                'java_websocket_measures',
                'jenkinsci_jenkins_measures',
                'spring-projects_spring-boot_measures',
                'square_okhttp_measures',
                'square_retrofit_measures',
                'zxing_zxing_measures']
    for d in DATASET:
        print("Computing " + d )
        df = pd.read_csv('dataset-td-forecast/' +d +'-model-find.csv',sep=";")
        grouped = df.groupby('CONFIG')
        grouped = grouped.filter(lambda g: all(g.RMSE != NaN)).dropna()
        grouped = grouped.groupby('CONFIG').filter(lambda g: len(g) == 30).dropna()
        grouped = grouped.drop(grouped[grouped.VERSIONS_AHEAD == 'average'].index)
        grouped = grouped.groupby('CONFIG').agg({'RMSE': ['mean', 'std']})
        grouped = grouped.xs('RMSE', axis=1, drop_level=True)
        grouped = grouped.reset_index('CONFIG')
        grouped = grouped.sort_values('mean')
        #grouped.rename(columns={"mean":"mean"}, inplace=True)
        grouped.to_csv("results/" + d + "-result.csv",sep=";")
    print("Done!")