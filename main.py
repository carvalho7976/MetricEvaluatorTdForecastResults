from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt
import csv





if __name__ == '__main__':
    #CSV HEAD
    #EXP PROJECT VERSIONS_AHEAD CONFIG FIT_MEAN FIT_STD SCORE_MEAN SCORE_STD MAE RMSE MAPE R2 
    DATASET = [#'apache_groovy_measures',
              #  'apache_incubator_dubbo_measures',
             #   'apache_kafka_measures',
             #   'apache_nifi_measures',
             #   'apache_ofbiz_measures',
             #   'apache_systemml_measures',
                'commonsio_measures'
             #   'google_guava_measures',
            #    'igniterealtime_openfire_measures',
            #    'java_websocket_measures',
            #    'jenkinsci_jenkins_measures',
            #    'spring-projects_spring-boot_measures',
             #   'square_okhttp_measures',
             #   'square_retrofit_measures',
             #   'zxing_zxing_measures'
              ]
    for d in DATASET:
        print("Computing " + d )
        df = pd.read_csv('dataset-td-forecast/' +d +'-model-find.csv',sep=";")
        grouped = df.groupby('CONFIG')
        grouped = grouped.filter(lambda g: all(g.RMSE != NaN)).dropna()
        grouped = grouped.groupby('CONFIG').filter(lambda g: len(g) == 18).dropna()
        #grouped = grouped.drop(grouped[grouped.VERSIONS_AHEAD == 'average'].index)
        grouped.to_csv("results/" + d + "-all-results.csv",sep=";")
        #calculate mean and std from all
        grouped = grouped.groupby('CONFIG').agg({'RMSE': ['mean', 'std']})
        grouped = grouped.xs('RMSE', axis=1, drop_level=True)
        grouped = grouped.reset_index('CONFIG')
        grouped = grouped.sort_values('mean')
        #grouped.rename(columns={"mean":"mean"}, inplace=True)
        grouped.to_csv("results/" + d + "-result.csv",sep=";")
        x = []
        y = []
        
        with open("results/" + d + "-result.csv",'r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ';')
            i = 0
            for row in plots:
                if(i > 10):
                    break
                if(i == 0):
                    x.append(row[0])
                    y.append(row[2])
                else:
                    x.append(row[0])
                    y.append('{0:.2f}'.format(float(row[2])))

                i += 1
        
        plt.bar(x, y, color = 'g', label = "RMSE")
        plt.xlabel('RMSE')
        plt.ylabel('Config')
        plt.title('Mean RMSE')
        plt.legend()
        plt.savefig("results/charts/" + d + "-plot.pdf") 
        plt.close()
    print("Done!")