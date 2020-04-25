
                                   Lifelogging - Temporal Human Activity Classification

This study attempts to find patterns in a lifelogger’s daily activity and thus can be used to perform behavioral analysis as studies suggest. This study focuses on testing the efficiency of analyzing temporal segmentation of human activities in order to understand a lifelogger’s daily life pattern.

The NTCIR-14 lifelog data consists of data from wearable biometric trackers every minute along with the continual blood glucose data observed every 15 minutes from 21 days. The Dataset consists of 16 features with few substantial attributes like calories burnt, minute id, heart rate, glucose, scanned glucose, activity, location, steps, and distance.

Feature Engineering

1.	Imputation – Multiple Linear Regression - user1 data preprocessing.py
2. 	Z- Score Normalisation - RandomForest.py
3. One hot label Encoding of Categorical variable - randomForest.py
4. DateTime Object conversion for Time series Analysis  - user1 data preprocessing.py
5. Missing Activity Clustering - user1_activityclassification.py

Models

1.	Ensemble Learning - Random Forest Classifier, Decision Trees - RandomForest.py
2.	Ensemble Learning – Boosting, AdaBoost with Logistic regression - AdaBoost_LR.py
3.	Artificial Neural Networks – Multi-layer Perceptron (3- layer Classifier) - multi-layer Perceptron.py

Model Classifiers - Results	
	
Classifier	                                       F-1 Score

|| MLP Without L2, 5 - fold Cross Validated  	   =     70.40% || 
|| Random Forest - 10 fold -Cross Validation	    =      70.80% ||
|| Boosting - Logistic Regression 5 fold validation  =	  68.42% ||


