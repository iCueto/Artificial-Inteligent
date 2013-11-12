# Discuss on decision tree

1. Did one of the data sets prove more challenging than the others?

  Data as follow:

        -breast-cancer.arff-
         noise:     17/1140=1.49%
         precision: 139/178=78.09%
         recall:    139/203=68.47%
         accuracy:  182/285=63.86%
        -nursery.arff-
         noise:     0/51840=0.00%
         precision: 4332/4332=100.00%
         recall:    4332/4332=100.00%
         accuracy:  8338/8338=100.00%

  `nursery.arff` has no noise, accuracy is `100.00%`, but `breast-cancer.arff` just has `64%`, which means it's much more challenging.

2. What was the difference between training and test set accuracy? Was your tree overfitting on any of the data sets?

  Basically the accuracy of the training dataset would be higher than the test dataset.

  Accuracy of the training dataset is `100% - noise`. In `breast-cancer.arff`, the accuracy of the training dataset is `98.51%`. It's much higher than the accuracy of the test dataset. It means in this case it's overfitting. `nursery.arff` doesn't have this problem.

3. Did it appears that any of the datasets was noisy or had other interesting issues?

  `breast-cancer.arff` has less than `2%` noise, `nursery.arff` even has no noise.

  `breast-cancer.arff` has one more attributes to test than `nursery.arff`, but `nursery.arff`'s accuracy is `100%` much higher than `breast-cancer.arff`. This tells us the size of the dataset is much more important to the accuracy than the numbers of the attributes.

4. Did the trees look very different between the different folds?

  It's pretty stable. For `breast-cancer.arff`, it stay around `60%~70%`.

## Extra

Run the same 5-fold cross validations through your original ZeroR learning algorithm from HW1. What was the precision, recall, and accuracy? How much worse was this than your decision tree?

    -ZeroR-nursery.arff-
    noise:     6938/10368=66.92%
    precision: 889/2591=34.31%
    recall:    889/889=100.00%
    accuracy:  889/2591=34.31%

    -DT-nursery.arff-
    noise:     0/51840=0.00%
    precision: 4332/4332=100.00%
    recall:    4332/4332=100.00%
    accuracy:  8338/8338=100.00%

    -ZeroR-breast-cancer.arff-
    noise:     69/228=30.26%
    precision: 41/57=71.93%
    recall:    41/41=100.00%
    accuracy:  41/57=71.93%

    -DT-breast-cancer.arff-
    noise:     17/1140=1.49%
    precision: 139/178=78.09%
    recall:    139/203=68.47%
    accuracy:  182/285=63.86%

For `breast-cancer.arff`, it's not much worse. But for `nursery.arff`, it's worse about `191.46%`.
