from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,recall_score,f1_score,average_precision_score,roc_auc_score,accuracy_score,confusion_matrix
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import scikitplot as skplt
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

def run_random_forest(X_data,Y_data,test_size=0.0,model_path="rmf.pkl",n_estimators=100,random_state=0):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    if test_size==0:
        clf.fit(X_data, Y_data)
        pickle.dump(clf, open(model_path, 'wb'))
        print(accuracy_score(Y_data,clf.predict(X_data)))
    else:
        X_train,X_test,y_train,y_test=train_test_split(X_data,Y_data,test_size=test_size)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open(model_path, 'wb'))

        y_pred=clf.predict(X_test)
        print(y_pred)
        print(accuracy_score(y_test,y_pred))
        print(precision_score(y_test,y_pred))
        print(recall_score(y_test,y_pred))
        print(f1_score(y_test,y_pred))
        print(average_precision_score(y_test,y_pred))
        print(roc_auc_score(y_test,y_pred))
        print(confusion_matrix(y_test,y_pred))

def search_best_random_forest(X_data,Y_data,cv=5,model_path="",params={}):
    clf = RandomForestClassifier(random_state=0)

    if len(params)==0:
        parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    else:
        n_estimators=params.get("n_estimators")
        max_depth=params.get("max_depth")
        if n_estimators and max_depth and isinstance(n_estimators, list) and isinstance(max_depth, list):
            parameters = {'n_estimators': n_estimators, 'max_depth': max_depth}
        else:
            print("------params参数错误------")
            parameters = {'n_estimators': range(10, 200, 20), 'max_depth': range(5, 30, 5)}
    gsearch = GridSearchCV(estimator=clf, param_grid=parameters, scoring='accuracy', cv=cv)
    gsearch.fit(X_data, Y_data)
    print("gsearch.best_params_", gsearch.best_params_)
    print("gsearch.best_score_", gsearch.best_score_)
    print("gsearch.best_estimator_", gsearch.best_estimator_)

    gsearch.best_estimator_.fit(X_data, Y_data)
    if model_path:
        pickle.dump(clf, open(model_path, 'wb'))
    else:
        pickle.dump(clf, open(f"best_rmf_n_estimators_{gsearch.best_params_.get('n_estimators')}_max_depth_{gsearch.best_params_.get('max_depth')}.pkl", 'wb'))

def evaluate_random_forest(X_data,Y_data,cv=5,n_estimators=100,max_depth=20):
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=0)
    scores = cross_val_score(clf, X_data, Y_data, cv=cv, scoring='accuracy')
    print(scores)
    print(sum(scores)/cv)

def draw_confusion_matrix(y, predictions, normalize=False, title=None):
    skplt.metrics.plot_confusion_matrix(y,predictions,normalize=normalize,title=title)
    plt.show()

def draw_roc(y, prediction_probas,title='ROC Curves'):
    skplt.metrics.plot_roc(y, prediction_probas,title=title)
    plt.show()

def draw_precision_recall_curve(y, prediction_probas,title='Precision-Recall Curve',curves=('micro', 'each_class')):
    skplt.metrics.plot_precision_recall_curve(y, prediction_probas,title=title,curves=curves)
    plt.show()

def draw_learning_curve(clf, X, y,title='Learning Curve', cv=None):
    skplt.classifiers.plot_learning_curve(clf, X, y,title=title, cv=cv)
    plt.show()

def draw_feature_importances(clf,title='Feature Importance',feature_names=None, max_num_features=20,order='descending'):
    skplt.classifiers.plot_feature_importances(clf, title=title,feature_names=feature_names, max_num_features=max_num_features,order=order)
    plt.show()

def draw_pca_2d_projection(X, y, title='PCA 2-D Projection'):
    pca = PCA(random_state=1)
    pca.fit(X)
    skplt.decomposition.plot_pca_2d_projection(pca, X, y,title=title)
    plt.show()

def analyse_by_histogram(x_data,y_data,y_data2,names=('正常', '恶意'),title="正常与恶意对比"):
    font_size = 10  # 字体大小
    fig_size = (20, 6)  # 图表大小
    scores = (y_data, y_data2)

    import matplotlib as mpl
    # 更新字体大小
    mpl.rcParams['font.size'] = font_size
    # 更新图表大小
    mpl.rcParams['figure.figsize'] = fig_size
    # 设置柱形图宽度
    bar_width = 0.35

    index = np.arange(len(scores[0]))
    # 绘制正常数据
    rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])
    # 绘制恶意数据
    rects2 = plt.bar(index + bar_width, scores[1], bar_width, color='#ED1C24', label=names[1])
    # X轴标题
    plt.xticks(index + bar_width, x_data)
    # Y轴范围
    # plt.ylim(ymax=100, ymin=0)
    # 图表标题
    plt.title(title)
    # 图例显示在图表下方
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fancybox=True, ncol=5)