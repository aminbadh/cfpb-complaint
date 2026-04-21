Evaluating Model 
Performance
Many years ago, when only the wealthy could afford access to education, tests and 
the teachers—parents wanted to know whether their children were learning enough 
Now, such evaluations are used to distinguish between high and low-achieving 
accurate student assessments. A fair assessment will have a large number of 
questions to cover a wide breadth of topics and reward true knowledge over lucky 
guesses. The assessment should also include some questions requiring the student 
to think about a problem he or she has never faced before. Correct responses would 
indicate that the student can apply the knowledge more generally.
A similar process of exam writing can be used to imagine the practice of evaluating 
machine learners. As different algorithms have varying strengths and weaknesses, it 
is necessary to use tests that reveal distinctions among the learners when measuring 
how a learner will perform on future data.
This chapter provides the information needed to assess machine learners, such as:
performance, and the performance measures you might use instead
model's ability to predict or forecast unseen data
How to use R to apply these more useful measures and methods to the 
predictive models we learned in previous chapters
Evaluating Model Performance
[ 294 ]
someone else, the process of teaching machine learners will also provide you with 
a greater insight into how to better the use of machine learning methods you've 
learned so far.
To measure
accuracy that divided the proportion of correct predictions by the total number of 
predictions. This number indicates the percentage of cases in which the learner is 
99,990 out of 100,000 newborn babies are carriers of a treatable but potentially-fatal 
genetic defect. This would imply an accuracy of 99.99 percent and an error rate of 
only 0.01 percent.
be wise to collect additional information before trusting your child's life to the test. 
predicts "no defect" regardless of circumstances will still be correct for 99.99 percent 
children with birth defects.
This is one consequence of the class imbalance problem, which refers to the trouble associated with data having a large 
at its intended purpose. For this reason, it is crucial to have measures of model 
performance that measure utility rather than raw accuracy. Toward this end, we will 
begin working with a variety of measures derived from predictions presented in a 
familiar format: the confusion matrix. Before we get started, however, we need to 
There are three main types of data that are used to
Actual class values
Predicted class values
Estimated probability of the prediction
Chapter 10
[ 295 ]
vectors of data: one holding the true, or actual class values and the other holding the 
predicted class values. Both vectors must have the same number of values stored in 
the same order. The predicted and actual values may be stored as separate R vectors 
or columns in a single R data frame. Either of these approaches will work with most 
R functions.
The actual class values come directly from the target feature in the test dataset. For 
instance, if your test data are in a data frame named , and the target is in 
a column named , we can create a vector of actual values using a command 
similar to . Predicted class values are obtained using the model. For most machine learning 
packages, this involves applying the 
frame of test data, such as: . Until now, we predictions using these two vectors 
of data. Yet hidden behind-the-scenes is another piece of useful information. Even 
percent certain that a SMS with the words "free" and "ringtones" is 99 percent spam, 
but is only 51 percent certain that a SMS with the word "tonight" is spam. In both 
the other.
Studying these internal prediction probabilities is useful to evaluate the model 
performance and is the source of the third type of evaluation data. If two models 
make the same number of mistakes, but one is more able to accurately assess its 
Unfortunately, obtaining the internal prediction probabilities can be tricky because 
 function for 
a single predicted class, such as spam or ham, you typically specify type. To 
obtain the prediction probability, you typically specify a type such as , , 
, or .provide such probabilities; the parameter for doing so 
is included in the syntax box introducing each model.
Evaluating Model Performance
[ 296 ]
described in Chapter 4, , you 
would use with the prediction function, such as: 
. Chapter 5, Divide and 
 is: 
. Keep in mind that in most cases the function will return a probability 
for each level of the outcome. For example, in the case of a two-outcome 
yes/no model, the might be a matrix or data frame as shown 
in the following expression:
Be careful while constructing an evaluation dataset to ensure that you are using 
the correct probability for the class level of interest. To avoid confusion, in the case 
of a binary outcome, you might even consider dropping the vector for one of the 
two alternatives.
To illustrate typical evaluation data, we'll use a data frame containing predicted class 
values, actual class values, and the estimated probability of a spam as determined 
Chapter 4, 
. To follow along with the examples here, download the 
website and load to a data frame using the command: 
Chapter 10
[ 297 ]
The data frame is simple; shown in the following command and 
its output, it contains three vectors of 1,390 values. One vector contains values 
indicating the actual type of SMS message ( or ), one vector indicates 
the model's predicted type, and the third vector indicates the probability that the 
message was spam:
Notice that when the predicted type is , the value is extremely close 
to zero. Conversely, when the predicted type was , the value is 
equal to one, which implies that the model was 100 percent certain that the SMS was 
spam. The fact that the estimated probability of spam falls on such extremes suggests 
 function, we can identify a 
few of these records:
Notice that the probabilities are somewhat less extreme, particularly row 
. applying various error metrics to this evaluation data. In fact, many such metrics are 
based on a tool we've already used extensively in previous chapters.
Evaluating Model Performance
[ 298 ]
A closer look at confusion matrices
A confusion matrix is a table that categorizes predictions according to whether 
they match the actual value in the data. One of the table's dimensions indicates the 
possible categories of predicted values while the other dimension indicates the same 
for actual values. Although, we have only seen 2 x 2 confusion matrices so far, a 
matrix can be created for a model predicting any number of classes. The following 
3 x 3 confusion matrix for a three-class model.
When the predicted value is the same as the actual value, this is a correct 
(denoted by O). The off-diagonal matrix cells (denoted by X) indicate the cases where 
the predicted value differs from the actual value. These are incorrect predictions. 
predictions falling on and off the diagonal in these tables:
The most common performance measures consider the model's ability to discern one 
class versus all others. The class of interest is known as the positive class, while all 
others are known as negative. The use of the terminology positive and negative is not intended 
it necessarily suggest that the outcome is present or absent (that 
is, birth defect versus none). The choice of the positive outcome 
can even be arbitrary, as in cases where a model is predicting 
categories such as sunny versus rainy, or dog versus cat.
Chapter 10
[ 299 ]
The relationship between positive class and negative class predictions can be 
depicted as a 2 x 2 confusion matrix that tabulates whether predictions fall into 
one of four categories:
True Positive (TP)
True Negative (TN)
False Positive (FP)
False Negative (FN)
For the birth defect 
tabulate whether the model's predicted birth defect status matches the patient's 
actual birth defect status, as shown in the following diagram:
Using confusion matrices to measure 
performance
With the 2 x 2 confusion matrix, we can formalize our
accuracy (sometimes called the success rate) as:
Evaluating Model Performance
[ 300 ]
In this formula, the terms TP, TN, FP, and FN refer to the number of times the 
model's predictions fell into each of these categories. Therefore, the accuracy is the 
proportion that represents the number of true positives and true negatives divided 
by the total number of predictions.
The error rate
Notice that the error rate can be calculated as one minus the accuracy. Intuitively, 
this makes sense; a model that is correct 95 percent of the time is incorrect 5 percent 
of the time.
A quick-and-dirty way to tabulate a confusion matrix is to use the function. It's 
easy to remember, and will count the number of occurrences of each combination of 
values—exactly what we need for a confusion matrix. The command for creating a 
confusion matrix for the SMS data is shown as follows. The counts in this table could 
then be used to calculate accuracy and other statistics:
If you would like to create a confusion matrix with more detailed output, the 
 function in the package offers a highly-customizable 
Chapter 2, Managing and 
Understanding Data. However, if you didn't install the package at that time, you will 
need to do so using the command . By default, the output includes proportions in each cell that indicate 
that cell's count as a percentage of the row, column, or total for the table. It also 
includes row and column totals. As shown in the following code, the syntax is 
similar to the function:
The result is confusion matrix with much more details:
Chapter 10
[ 301 ]
We've used in several previous chapters, so by now you should be 
familiar with the output. If you don't remember, you can refer to the table's key 
(labeled ), which provides a description of each number in the table.
We can use the contingency table to obtain the accuracy and error rate. Since 
accuracy is , we can calculate:
We can also calculate the error rate, as:
This is the same as one minus accuracy:
Evaluating Model Performance
[ 302 ]
Although these calculations may seem simple, it can be a helpful exercise to practice 
thinking about how the components of the confusion matrix relate to one another. 
In the next section, you will see how these same pieces can be combined in different 
ways to create a variety of additional performance measures.
Beyond accuracy – other measures of 
performance
A comprehensive description of every performance measure is not feasible. 
disciplines as diverse as medicine, information retrieval, marketing, and signal 
detection theory, among others. Instead, we'll consider only some of the most 
commonly-cited measures in machine learning literature.
Regression Training ( ) package by Max Kuhn includes 
functions for computing many such performance measures. This package provides 
a large number of tools for preparing, training, evaluating, and visualizing 
machine learning models and data. In addition to its application here, we will 
also employ caret extensively in Chapter 11, Improving Model Performance. Before 
proceeding, install the package using the command . For more information on , please refer to the 
publication: 
, Iss. 5, by Max Kuhn (2008).
The package adds yet another function for creating a confusion matrix. As 
shown in the following commands, the syntax is similar to , but the positive 
will set .
Chapter 10
[ 303 ]
This results in the following output:
The output includes a confusion matrix and a set of performance measures. Let's take 
a look at a few of the most commonly used statistics.
The kappa statistic
The kappa statistic (labeled 
accounting for the possibility of a correct prediction by chance alone. Kappa values 
range to a maximum value of 1, which indicates perfect agreement between the 
model's predictions and the true values—a rare occurrence. Values less than one 
indicate imperfect agreement.
Depending on how your model is to be used, the interpretation of the kappa statistic 
might vary. One common interpretation is shown as follows:
Poor agreement = Less than 0.20
Fair agreement = 0.20 to 0.40
Moderate agreement = 0.40 to 0.60
Good agreement = 0.60 to 0.80
Very good agreement = 0.80 to 1.00
Evaluating Model Performance
[ 304 ]
agreement" may be more than adequate for predicting someone's favorite ice cream 
on the surface of the moon.
For more information on the previous scale, refer to: The 
measurement of observer agreement for categorical data, Vol. 33, pp.159-174, by J.R. Landis and G.G. Koch (1977).
The following is the formula for calculating the kappa statistic. In this formula, 
Pr refers to the proportion of actual (a) and expected (e) agreement between the 
The most common method, described here, uses Cohen's 
of agreement for nominal scales, Education and Psychological 
Measurement Vol. 20, pp. 37-46, by J. Cohen (1960).
These proportions are easy to obtain from a confusion matrix once you know where 
with the function, duplicated as follows:
Chapter 10
[ 305 ]
Remember that the bottom value in each cell indicates the proportion of all instances 
falling into that cell. Therefore, to calculate the observed agreement , we simply 
add the proportion of all instances where the predicted type and actual SMS type 
agree. Thus, we can calculate as:
For this
will 
relative to the expected agreement, , which is the probability that chance alone 
would lead the predicted and actual values to match, under the assumption that both 
are selected randomly according to the observed proportions.
Chapter 4, . Assuming two events 
are independent (meaning one does not affect the other), probability rules note that 
the probability of both occurring is equal to the product of the probabilities of each 
one occurring. For instance, we know that the probability of both choosing is:
And the probability of both choosing is:
The probability that the predicted or actual type is or can be obtained from 
the row or column totals. For instance, .
 can be calculated as the sum of the probabilities that either the predicted and 
actual values agree that the message is spam, or they agree that the message is ham. 
Since the probability of either of two mutually exclusive events (that is, they cannot 
happen simultaneously) occurring is equal to the sum of their probabilities, we 
simply add both products. In R code, this would be:
Since is , by chance alone we would expect the observed and actual 
values to agree about 78.4 percent of the time.
Evaluating Model Performance
[ 306 ]
This means that we now have all the information needed to complete the kappa 
formula. Plugging the and 
The kappa is about 0.89, which agrees with the previous output 
(the small difference is due to rounding). Using the suggested interpretation, we 
actual values.
There are a couple of R functions to calculate kappa automatically. The 
function (be sure to note the capital ) in the Visualizing Categorical Data ( ) 
package uses a confusion matrix of predicted and actual values. After installing the 
package using the command , the following commands 
can be used to obtain kappa:
We're interested in the unweighted kappa. The value 0.89 matches what 
we expected.
The weighted kappa is used when there are varying degrees 
of agreement. For example, using a scale of cold, warm, and 
hot, a value of warm agrees more with hot than it does with 
the value of cold. In the case of a two-outcome event, such 
as spam and ham, the weighted and unweighted kappa 
statistics will be identical.
The function in the Inter-Rater Reliability ( ) package can be used to 
calculate kappa from vectors of predicted and actual values stored in a data frame. 
After installing the package using the command , the 
following commands can be used to obtain kappa:
Chapter 10
[ 307 ]
In both cases, the same kappa statistic is reported, so use whichever option you are 
more comfortable with.
Be careful not to use the built-in function. It is unrelated 
to the Kappa statistic reported previously.
 often involves a balance between being overly conservative and overly 
eliminate every spam message by aggressively eliminating nearly every ham message 
at the same time. On the other hand, a guarantee that no ham messages will be 
The sensitivity of a model (also called the true positive rate), measures the 
the following formula, it is calculated as the number of true positives divided by the 
The of a model (also called the true negative rate), measures the 
this is computed as the number of true negatives divided by the total number of 
negatives—the true negatives plus the false positives.
Evaluating Model Performance
[ 308 ]
numbers in the output are correct. For example, the calculation 
for sensitivity is:
The package
directly from vectors of predicted and actual values. Be careful to specify the 
 or parameter appropriately, as shown in the following lines:
range from 0 to 1, with values close to 1 being more 
For example, in this case the sensitivity of 0.842 implies that 84 percent of spam 
SMS messages may be unacceptable, or it may be a reasonable tradeoff given the 
reduction in spam.
Typically, changes are made to the model, and different models are tested until 
such as those discussed later in this chapter, can also assist with understanding the 
Chapter 10
[ 309 ]
Precision and recall
in the context of information retrieval, these statistics are intended to provide an 
indication of how interesting and relevant a model's results are, or whether the 
predictions are diluted by meaningless noise.
The precision
proportion of positive examples that are truly positive; in other words, when a model 
the positive class in cases very likely to be positive. It will be very trustworthy.
Consider what would happen if the model was very imprecise. Over time, the results 
would be less likely to be trusted. In the context of information retrieval, this would 
be similar to a search engine such as Google returning unrelated results. Eventually 
high precision means that the model is able to carefully target only the spam while 
ignoring the ham.
On the other hand, recall is a measure of how complete the results are. As shown in 
number of positives. You may recognize that this is the same as sensitivity, only 
the interpretation differs. A model with high recall captures a large portion of the 
positive examples, meaning that it has wide breadth. For example, a search engine 
with high recall returns a large number of documents pertinent to the search query. 
We can calculate precision and recall from the confusion matrix. Again, assuming 
that spam is the positive class, the precision is:
Evaluating Model Performance
[ 310 ]
And the recall is:
The package can be used to compute either of these measures from vectors of 
predicted and actual classes. Precision uses the function:
While recall uses the function as we had done before.
Similar to the inherent 
recall. It is easy to be precise if you target only the low-hanging fruit—the easy to 
classify examples. Similarly, it is easy for a model to have high recall by casting a 
very wide net, meaning that that the model is overly aggressive at predicting the 
positive cases. In contrast, having both high precision and recall at the same time is 
The F-measure
A measure of model performance that combines precision and recall into a single 
number is known as the F-measure (also sometimes called the F1 score or the 
F-score). The F-measure combines precision and recall using the harmonic mean. 
The harmonic mean is used rather than the more common arithmetic mean since 
both precision and recall are expressed as proportions between zero and one. The 
following is the formula for F-measure:
To calculate the F-measure, use the precision and recall values computed previously:
Chapter 10
[ 311 ]
This is the same as using the counts from the confusion matrix:
Since the F-measure reduces model performance to a single number, it provides a 
convenient way to compare several models side-by-side. However, this assumes that 
equal weight should be assigned to precision and recall, an assumption that is not 
always valid. It is possible to calculate F-scores using different weights for precision 
and recall, but choosing the weights can be tricky at best and arbitrary at worst. A 
better practice is to use measures such as the F-score in combination with methods 
that consider a model's strengths and weaknesses more globally, such as those 
described in the next section.
Visualizing performance tradeoffs
Visualizations are often helpful for understanding how the performance of 
machine learning algorithms varies from situation to situation. Rather than thinking 
recall, visualizations allow you to examine how measures vary across a wide range 
of values. They also provide a method for comparing learners side-by-side in a 
single chart.
The package provides an easy-to-use suite of functions for creating 
functions for computing a large set of the most common performance measures and 
visualizations. The ROCR website, , includes 
a list of the full set of features as well as several examples of the visualization 
capabilities. Before continuing, install the package using the command 
. For more information on the development of , see: 
, 21, pp. 3940-3941, by 
T. Lengauer (2005).
To create visualizations with 
contain the class values predicted, and the second must contain the estimated 
be examined through plotting functions of .
Evaluating Model Performance
[ 312 ]
probabilities ( ), and the actual class labels ( ). These are 
combined using the function in the following lines:
 provides a function for computing measures of performance 
, which was used in previous code example. The 
 function. Given 
these three functions, a large variety of depictions can be created.
ROC curves
The ROC curve (Receiver Operating Characteristic) is commonly used to examine 
the tradeoff between the detection of true positives, while avoiding the false positives. 
As you might suspect from the name, ROC curves were developed by engineers in the 
signals needed a method to discriminate between true signals and false alarms. The 
The characteristics of a typical ROC diagram are depicted in the following plot. 
and the proportion of false positives on the horizontal axis. Because these values 
are equivalent to sensitivity and ( ), respectively, the diagram is also 
Chapter 10
[ 313 ]
The points comprising ROC curves indicate the true positive rate at varying false 
Beginning at the origin, each prediction's impact on the true positive rate and false 
positive rate will result in a curve tracing vertically (for a correct prediction), or 
horizontally (for an incorrect prediction).
plot. First, the diagonal line from the bottom-left to the top-right corner of the 
diagram represents a 
very useful. Similarly, has a curve that passes through the point at 
100 percent true positive rate and 0 percent false positive rate. It is able to correctly 
; they fall somewhere in the 
zone between perfect and useless.
values. This can be measured using a statistic known as the area under the ROC 
curve (abbreviated AUC). The AUC, as you might expect, treats the ROC diagram 
as a two-dimensional square and measures the total area under the ROC curve. 
academic letter grades:
0.9 – 1.0 = A (outstanding)
 (excellent/good)
0.7 – 0.8 = C (acceptable/fair)
0.6 – 0.7 = D (poor)
0.5 – 0.6 = F (no discrimination)
As with most scales similar to this, the levels may work better for some tasks than 
It's also worth noting that two ROC curves may be shaped 
very differently, yet have identical AUC. For this reason, 
AUC can be extremely misleading. The best practice is to 
use AUC in combination with qualitative examination of 
the ROC curve.
Evaluating Model Performance
[ 314 ]
Creating ROC curves with the 
for the 
positive rates versus false positive rates, we simply call the function 
while specifying the and measures, as shown in the following code:
Using the 
function. As shown in the following code lines, many of the standard parameters 
 (for adding a title), (for 
changing the line color), and 
Although the command, used in 
a valid ROC curve, it is helpful to add a reference line to indicate the performance of 
For plotting such a line, we'll use the function. This function can be used 
to specify a line in slope-intercept form, where is the intercept and is the slope. 
Since we need an identity line that passes through the origin, we'll set the intercept to 
 and the slope to as shown in the following plot. The 
the line thickness, while the 
 indicates a dashed line.
The end result is an ROC plot with a dashed reference line:
Chapter 10
[ 315 ]
Qualitatively, we can see that this ROC curve appears to occupy the space in the 
, as shown in the 
following code:
Since 
information in positions known as slots. The function can be used to see 
 symbol. To access the AUC value, which 
is stored as a list in the slot, we can use the notation along with the 
to answer such questions, we need to better understand how far we can extrapolate a 
model's predictions beyond the test data.
Estimating future performance
Some R machine learning packages present confusion matrices and performance 
measures during the model building process. The purpose of these statistics is to 
provide insight about the model's resubstitution error, which occurs when the 
training data is incorrectly predicted in spite of the model being built directly from 
this data. This information is intended to be used as a rough diagnostic, particularly 
to identify obviously poor performers.
Evaluating Model Performance
[ 316 ]
The resubstitution error is not a very useful marker of future performance, however. 
For example, a model that used rote memorization to perfectly classify every training 
instance (that is, zero resubstitution error) would be unable to make predictions on 
data it has never seen before. For this reason, the error rate on the training data can 
be extremely optimistic about a model's future performance.
Instead of relying on resubstitution error, a better practice is to evaluate a model's 
performance on data it has not yet seen. We used such a method in previous chapters 
when we split the available data into a set for training and a set for testing. In some 
cases, however, it is not always ideal to create training and test datasets. For instance, 
in a situation where you have only a small pool of data, you might not want to 
reduce the sample any further by dividing it into training and test sets.
Fortunately, there are other ways to estimate a model's performance on unseen 
data. The package that we used previously for calculating performance 
measures also, offers a number of functions for this purpose. If you are following 
along with the R code examples and haven't already installed the package, 
please do so. You will also need to load the package to the R session using the 
 command.
The holdout method
The procedure of partitioning data into training and test datasets that we used in 
previous chapters is known as the holdout method. As shown in the following 
diagram, the training dataset is used to generate the model, which is then applied to 
the test dataset to generate predictions for evaluation. Typically, about one-third of 
the data is held out for testing and two-thirds used for training, but this proportion 
can vary depending on the amount of data available. To ensure that the training and 
test data do not have systematic differences, examples are randomly divided into the 
two groups.
Chapter 10
[ 317 ]
For the holdout method to result in a truly accurate estimate of future performance, 
is easy to unknowingly violate this rule by choosing a best model based upon the 
results of repeated testing. Instead, it is better to divide the original data so that in 
addition to the training and test datasets, a third validation dataset is available. The 
estimated error rate for future predictions. A typical split between training, test, and 
validation would be 50 percent, 25 percent, and 25 percent respectively.
A keen reader will note that holdout test data was used in 
previous chapters to compare several models. This would 
indeed violate the rule as stated previously, and therefore the 
test data might have been more accurately termed validation 
data. If we use test data to make a decision, we are cherrypicking results and the evaluation is no longer an unbiased 
estimate of future performance.
A simple method for creating holdout samples uses random number generators to 
Chapter 5, Divide and 
 to create training and 
test datasets.
If you'd like to follow along with the following examples, 
download the dataset from the Packt 
Publishing's website and load to a data frame using the 
command . Suppose we have a data frame named credit with 1000 rows of data. We can divide 
this into three partitions:
line creates a vector of randomly ordered row IDs from 1 to 1000. These 
IDs are then used to divide the credit data frame into 500, 250, and 250 records 
comprising the training, validation, and test datasets.
Evaluating Model Performance
[ 318 ]
One problem with holdout sampling is that each partition may have a larger or smaller 
proportion of some classes. In certain cases, particularly those in which a class is a very 
small proportion of the dataset, this can lead a class to be omitted from the training 
In order to reduce the chance that this will occur, a technique called 
random sampling can be used. Although, on average, a random sample will contain 
sampling ensures that the generated random partitions have approximately the same 
proportion of each class as the full dataset.
The package provides a function that will create 
of training and test data for the dataset is shown in the following commands. 
 refers 
to whether a loan went into default), in addition to a parameter 
proportion of instances to be included in the partition. The parameter 
prevents the result from being stored in list format:
The vector indicates row numbers included in the training sample. 
We can use these row numbers to select examples for the data 
frame. Similarly, by using a negative symbol, we can use the rows not found in 
the vector for the dataset.
Since models trained on larger datasets generally perform 
better, a common practice is to retrain the model on the full 
set of data (that is, training plus test and validation) after a 
model maximum use of available data.
Although it does not guarantee 
other types of representativeness. Some samples may have too many or too few 
datasets, which may not have a large enough portion of such cases to divide among 
training and test sets.
Chapter 10
[ 319 ]
In addition to potentially biased samples, another problem with the holdout method 
is that substantial portions of data must be reserved for testing and validating the 
model. Since these data cannot be used to train the model until its performance has 
been measured, the performance estimates are likely to be overly conservative.
A technique called repeated holdout is sometimes used to mitigate the problems 
of randomly composed training datasets. The repeated holdout method is a special 
case of the holdout method that uses the average result from several random holdout 
samples to evaluate a model's performance. As multiple holdout samples are used, 
it is less likely that the model is trained or tested on non-representative data. We'll 
expand on this idea in the next section.
Cross-validation
The repeated holdout is the basis of a technique known as k-fold cross-validation
(or k-fold CV), which has become the industry standard for estimating model 
performance. But rather than taking repeated random samples that could potentially 
use the same record more than once, k-fold CV randomly divides the data into 
completely separate random partitions called folds.
Although can be set to any number, by far the most common convention is to use 
10-fold cross-validation
(each comprising 10 percent of the total data), a machine learning model is built on 
the remaining 90 percent of data. The fold's matching 10 percent sample is then used 
for model evaluation. After the process of training and evaluating the model has 
occurred for 10 times (with 10 different training/testing combinations), the average 
performance across all folds is reported.
An extreme case of k-fold CV is the leave-one-out method, which performs k-fold CV using a fold for each one of the data's 
examples. This ensures that the greatest amount of data is used 
for training the model. Although this may seem useful, it is so 
computationally expensive that it is rarely used in practice.
Datasets for cross-validation can be created using the function in 
the 
will attempt to maintain the same class balance in each of the folds as in the original 
dataset. The following is the command for creating 10 folds:
Evaluating Model Performance
[ 320 ]
The result of the function is a list of vectors storing the row numbers 
for each of the requested folds. We can peek at the contents using :
, and stores 100 integers indicating the 
100 rows in the 
to build and evaluate a model, one more step is needed. The following commands 
sampling, we'll assign the selected examples to the training dataset and use the 
negative symbol to assign everything else to the test dataset:
To perform the full 10-fold CV, this step would need to be repeated a total of 10 
times, building a model, and then calculating the model's performance each time. 
At the end, the performance measures would be averaged to obtain the overall 
performance. Thankfully, we can automate this task by applying several of the 
techniques we've learned before.
To demonstrate the process, we'll estimate the kappa statistic for a C5.0 decision tree 
model of the data using 10-fold CV. First, we need to load (for creating 
the folds), (for the decision tree), and (for calculating kappa). The latter two 
packages were chosen for illustrative purposes; if you desire, you can use a different 
model or a different performance measure with the same series of steps.
Chapter 10
[ 321 ]
Next, we'll create a list of 10 as we have done previously. The 
function is used here to ensure that the results are consistent if you run the same 
code again:
Finally, we will apply a series of identical steps to the list of folds using the 
function. As shown in the following code, because there is no existing function that 
. Our custom function divides the data frame into training and test data, creates 
a decision tree using the function on the training data, generates a set of 
predictions from the test data, and compares the predicted and actual values using 
the function:
The resulting kappa statistics are compiled into a list stored in the 
:
Evaluating Model Performance
[ 322 ]
In this way, we've transformed our list of IDs for 10 folds into a list of kappa 
these 10 values. Although you will be tempted to type , because 
 is not a numeric vector the result would be an error. Instead, use the 
 function, which eliminates the list structure and reduces to a 
numeric vector. From there, we can calculate the mean kappa as expected:
Unfortunately, this kappa statistic is fairly low—in fact, this corresponds to "poor" 
on the interpretation scale—which suggests that the credit scoring model does 
not perform much better than random chance. In the next chapter, we'll examine 
automated methods based on 10-fold CV that can assist us with improving the 
performance of this model.
Perhaps the current gold standard method for reliably estimating 
model performance is repeated k-fold CV. As you might guess 
from the name, this involves repeatedly applying k-fold CV and 
averaging the results. A common strategy is to perform 10-fold 
CV ten times. Although computationally intensive, this provides 
a very robust estimate.
Bootstrap sampling
A slightly less popular, but still fairly widely-used alternative to k-fold CV is 
known as bootstrap sampling, the bootstrap, or bootstrapping for short. Generally 
speaking, these refer to statistical methods of using random samples of data to 
estimate properties of a larger set. When this principle is applied to machine learning 
model performance, it implies the creation of several randomly-selected training and 
test datasets, which are then used to estimate performance statistics. The results 
future performance.
Chapter 10
[ 323 ]
divides the data into separate partitions, in which each example can appear only 
once, the bootstrap allows examples to be selected multiple times through a process 
of sampling with replacement. This means that from the original dataset of n
examples, the bootstrap procedure will create one or more new training datasets 
that also contain n examples, some of which are repeated. The corresponding test 
datasets are then constructed from the set of examples that were not selected for the 
respective training datasets.
Using sampling with replacement as described previously, the probability that any 
given instance is included in the training dataset is 63.2 percent. Consequently, the 
probability of any instance being in the test dataset is 36.8 percent. In other words, 
the training data represents only 63.2 percent of available examples, some of which 
are repeated. In contrast with 10-fold CV, which uses 90 percent of examples for 
training, the bootstrap sample is less representative of the full dataset.
As a model trained on only 63.2 percent of the training data is likely to perform 
worse than a model trained on a larger training set, the bootstrap's performance 
estimates may be substantially lower than what will be obtained when the model 
is later trained on the full dataset. A special case of bootstrapping known as the 
0.632 bootstrap accounts
function of performance on both the training data (which is overly optimistic) and test train error = 0.632 error 0.368 error
One advantage of the bootstrap over cross-validation is that it tends to work better 
with very small datasets. Additionally, bootstrap sampling has applications beyond 
performance measurement. In particular, in the following chapter we'll learn how 
the principles of bootstrap sampling can be used to improve model performance.
Evaluating Model Performance
[ 324 ]
Summary
This chapter presented a number of the most common measures and techniques for 
accuracy provides a simple method for examining how often a model is correct, this 
can be misleading in the case of rare events because the real-life cost of such events 
may be inversely proportional to how frequently they appear in the data.
A number of measures based on confusion matrices better capture the balance 
among the costs of various types of errors. Closely examining the tradeoffs between 
about the implications of errors in the real world. Visualizations such as the ROC 
curve are also helpful toward this end.
It is also worth mentioning that sometimes the best measure of a model's 
instance, you may need to explain a model's logic in simple language, which would 
eliminate some models from consideration. Additionally, even if it performs very 
completely useless.
An obvious extension of measuring performance is to identify automated ways to 
work so far to investigate ways to make smarter models by systematically iterating, 