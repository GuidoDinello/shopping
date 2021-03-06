from cProfile import label
import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    #create a dictionary Month:Month_id
    month_dict = dict()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    count=0
    for month in months:
        month_dict[month]=count
        count += 1

    evidence = []   #should be length 17
    labels = []     #shoul be length 1
    index_float_types = [1, 3, 5, 6, 7, 8, 9]
    #index_int_types = [0, 2, 4, 11, 12, 13, 14, 15, 16]

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) #skip column names
        #for each row
        for row in csv_reader:
            tempEvidence = []
            #for each col in row
            for col in range(18):
                # print('=='*10)
                # print(row)
                # print(col)
                # print(row[col])
                #Month
                if col == 10:
                    month = row[col]
                    tempEvidence.append(month_dict[month])
                #VisitorType
                elif col == 15:
                    if row[col] == "Returning_Visitor":
                        tempEvidence.append(1)
                    else:
                        tempEvidence.append(1)
                #Weekend
                elif col == 16:
                    if row[col] == True:
                        tempEvidence.append(1)
                    else:
                        tempEvidence.append(0)
                #Revenue
                elif col == 17:
                    if row[col] == 'TRUE':
                        labels.append(1)
                    else:
                        labels.append(0)
                #float_types
                elif col in index_float_types:
                    tempEvidence.append(float(row[col]))
                #int_types
                else:
                    tempEvidence.append(int(row[col]))

            evidence.append(tempEvidence)
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    #Initialize model
    model = KNeighborsClassifier(n_neighbors=1)
    #Training model on data 
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #number of purchasers
    positive = float(0)
     #number of not purchasers
    negative = float(0)
    #predicted as purhcaser and purchaser
    correct_pos_predictions = float(0)
    #predicted as not purhcaser and not purchaser
    correct_neg_predictions = float(0)

    for c, d in zip(labels,predictions):               
        if c:
            positive += 1
            if d:
                correct_pos_predictions += 1
        else:
            negative += 1
            if not d:
                correct_neg_predictions += 1

    sensitivity = correct_pos_predictions / positive
    specificity = correct_neg_predictions / negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
