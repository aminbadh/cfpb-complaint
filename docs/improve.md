Improving Model 
Performance
When a sports team falls short of meeting its goal—whether it is to obtain an 
Olympic gold medal, a league championship, or a world record time—it must 
begin a process of searching for improvements to avoid a similar fate in the future. 
Imagine that you're the coach of such a team. How would you spend your practice 
to maximize every bit of their potential. Or, you might place a greater emphasis on 
teamwork, which could utilize the athletes' strengths and weaknesses more smartly.
machine learning algorithm—perhaps to enter a competition, such as those posted 
on the Kaggle website ( ), to win the million 
dollar ), or simply to improve the 
Although the context of the competition may differ, many strategies one might use 
to improve a sports team's performance can also be used to improve the performance 
techniques and teamwork skills that allow you to meet your performance goals.
This chapter builds upon the material covered in this book so far to introduce a set 
of techniques for improving the predictive performance of machine learners. You 
will learn:
for the optimal set of training conditions
Methods for combining models into groups that use teamwork to tackle the 
most challenging problems
Cutting edge techniques for getting the maximum level of performance out 
of machine learners
Improving Model Performance
[ 326 ]
Not all of these methods will be successful on every problem. Yet if you look at the 
of them has been employed. To remain competitive, you too will need to add these 
skills to your repertoire.
Tuning stock models for better 
performance
Some learning problems are well suited to the stock models presented in previous 
the model; it may perform well enough as it is. On the other hand, some problems are 
complex, requiring an understanding of many subtle relationships, or it may have 
Developing models 
bit an art as it is a science. Sometimes, a bit of intuition is helpful when trying 
improvements will require a brute-force, trial and error approach. Of course, the 
process of searching numerous possible improvements can be aided by the use of 
automated programs.
In Chapter 5, , we 
Although we were able to use performance tuning methods to obtain a respectable 
Chapter 10, Evaluating Model Performance, we realized that the high accuracy was a bit 
misleading. In spite of the reasonable accuracy, the kappa statistic was only about 
0.20, which suggested that the model was actually performing somewhat poorly. In 
this section, we'll revisit the credit scoring model to see if we can improve the results.
To follow along with the examples, download the 
using the command: 
parameter to increase the number of boosting iterations. By increasing the trials from 
the default of 1 up to the values of 10 and 100, we were able to increase the model's 
parameter tuning.
Chapter 11
[ 327 ]
Parameter tuning is not limited to decision trees. For instance, we tuned k-nearest 
neighbor models when we searched for the best value of , and used a number 
the number of nodes, hidden layers, or choosing different kernel functions. Most 
your liking. Although this allows the model to be tailored closely to the data, the 
complexity of all the possible options can be daunting. A more systematic approach 
is warranted.
Using caret for automated parameter tuning
Rather than choosing arbitrary values for each of the model's parameters—a task 
The package, which we used extensively in Chapter 10, Evaluating Model 
Performance, provides tools to assist with automated parameter tuning. The core 
functionality is provided by a function that serves as a standardized 
interface to train 150 different 
regression tasks. By using this function, it is possible to automate the search for 
optimal models using a choice of evaluation methods and metrics.
Do not feel overwhelmed by the large number of models—we've 
already covered many of them in earlier chapters. Others are 
simple variants or extensions of the base concepts. Given what 
ability to understand all of the 150 choices.
Automated parameter tuning requires you to consider three questions:
Improving Model Performance
[ 328 ]
machine learning task and one of the 150 models. Obviously, this requires an 
understanding of the breadth and depth of machine learning models. This book 
provides the background needed for the former, while additional practice will help 
with the latter. Additionally, it can help to work through a process of elimination: 
nearly half of the models can be eliminated depending on whether the task is 
the need to avoid black box models, and so on. In any case, there's also no reason you 
can't try several approaches and compare the best result of each.
Addressing the second question is a matter largely dictated by the choice of model, 
since each algorithm utilizes a unique set of parameters. The available tuning 
parameters for each of the predictive models covered in this book are listed in the 
following table. Keep in mind that although some models have additional options not 
shown, only those listed in the table are supported by for automatic tuning.
For a complete list of the 150 models and corresponding 
tuning parameters covered by , refer to the table 
provided by package author Max Kuhn at: 
Model Learning task Method name Parameters
k-Nearest Neighbors Classification
Naïve Bayes Classification , Decision Trees Classification , , OneR Rule Learner Classification None
RIPPER Rule Learner Classification
Linear Regression Regression None
Regression Trees Regression
Model Trees Regression , , Neural Networks Dual use , Support Vector 
Machines (Linear 
Kernel)
Dual use
Support Vector 
Machines (Radial Basis 
Kernel)
Dual use
Random Forests Dual use
Chapter 11
[ 329 ]
The goal of automatic tuning is to search a set of candidate models comprising a 
matrix, or grid, of possible combinations of parameters. Because it is impractical 
to search every conceivable parameter value, only a subset of possibilities is used 
to construct the grid. By default, searches at most three values for each of p
parameters, which means that candidate models will be tested. For example, by 
default, the automatic tuning of k-nearest neighbors will compare candidate 
models, for instance, one each of , , and . Similarly, tuning a decision tree 
could result in a comparison of up to 27 different candidate models, comprising the 
grid of possible combinations of , , and settings. In 
practice, however, only 12 models are actually tested. This is because the and 
 parameters can only take two values ( versus and versus 
, respectively), which makes the grid size 
Since the package's default search grid may not 
be ideal for your learning problem, it also allows you 
command which we will cover later.
to identify the best model among the candidates. This uses the methods discussed 
in Chapter 10, Evaluating Model Performance such as the choice of resampling strategy 
to create training and test datasets, and the use of model performance statistics to 
measure the predictive accuracy.
All of the resampling strategies and many of the performance statistics we've learned 
are supported by . These include statistics such as accuracy and kappa 
also be used if desired.
By default, when choosing the best model, will select the model with the largest 
value of the desired performance measure. Because this practice sometimes results in 
the selection of models that achieve marginal performance improvements via large 
increases in model complexity, alternative model selection functions are provided.
Given the wide variety of options, it is helpful that many of the defaults are reasonable. 
For instance, it will use prediction accuracy on a bootstrap sample to choose the best 
tweak the function to design a wide variety of experiments.
Improving Model Performance
[ 330 ]
Creating a simple tuned model
To illustrate the process of tuning a model, let's begin by observing what happens 
when we attempt to tune the credit scoring model using the package's default 
The simplest way to tune a learner requires only that you specify a model type 
via the parameter. Since we used C5.0 decision trees previously with the 
credit model, we'll continue our work by optimizing this learner. The basic 
command for tuning a C5.0 decision tree using the default settings is as follows:
First, the function is used to initialize R's random number generator to a 
set starting position. You may recall that we have used this function in several prior 
chapters. By setting the seed parameter (in this case to the arbitrary number ), 
, which use random sampling, to be repeated with identical results—a very 
helpful feature if you are sharing code or attempting to replicate a prior result.
. This models 
loan default status ( or ) using all of the other features in the data frame. 
The parameter tells to use the C5.0 decision tree algorithm.
(dependent upon your computer's capabilities) as the tuning process occurs. Even 
though this is a fairly small dataset, a substantial amount of calculation must occur. R 
is repeatedly generating random samples of data, building decision trees, computing 
performance statistics, and evaluating the result.
. If you would 
 will list all the associated 
data—but this can be quite overwhelming. Instead, simply type the name of the 
 yields the 
following output:
Chapter 11
[ 331 ]
The summary includes four main components:
1. A brief description of the input dataset: If you are familiar with your data 
and have applied the function correctly, none of this information 
should come as a surprise.
2. A report of preprocessing and resampling methods applied: Here we see 
that 25 bootstrap samples, each including 1000 examples, were used to train 
the models.
3. A list of candidate models evaluated
12 different models were tested, based on combinations of three C5.0 tuning 
parameters: , , and . The average and standard deviation 
(labeled ) of the accuracy and kappa statistics for each candidate model are 
also shown.
4. The choice of best model: As noted, the model with the largest accuracy 
value ( ) was chosen as the best. This was the model that used a 
, , and .
Improving Model Performance
[ 332 ]
The function uses the tuning parameters from the best model (as indicated 
by #4 previously) to build a model on the full input dataset, which is stored in the 
. In most cases, you will not need to work directly with the 
 function with the 
generate predictions as expected, while also providing added functionality that will 
be described shortly. For example, to apply the best model to make predictions on 
the training data, you would use the following commands:
Of the 1000 
Keep in mind that this is the resubstitution error and should not be viewed as 
indicative of performance on unseen data. The bootstrap estimate of 73 percent 
(shown in the summary output) is a more realistic estimate of future performance.
, directly 
on directly or training a 
new model using the optimized parameters.
First, any data preprocessing steps that the function applied to the data 
will be similarly applied to the data used for generating predictions. This includes 
transformations like centering and scaling (that is, when using k-nearest neighbors), 
missing value imputation, and others. This ensures that the data preparation steps 
used for developing the model remain in place when the model is deployed.
Second, the function for models provides a standardized interface 
for obtaining predicted class values and predicted class probabilities—even for 
models that ordinarily would require additional steps to obtain this information. 
The predicted classes are provided by default as follows:
Chapter 11
[ 333 ]
To obtain the estimated probabilities for each class, add an additional parameter 
specifying :
Even in cases where the underlying model refers to the prediction probabilities using 
a different string (for example, for a model), automatically 
translates to the appropriate string behind the scenes.
Customizing the tuning process
The decision tree we created previously demonstrates the package's ability to 
produce an optimized model with minimal intervention. The default settings allow 
strongly performing models to be created easily. However, without digging deeper, 
you may miss out on the upper echelon of performance. Or perhaps you want 
to change the default evaluation criteria to something more appropriate for your 
learning problem. Each step in the process can be customized to your learning task.
explained previously to mirror the process we had used in Chapter 10, Evaluating 
Model Performance. If you recall from that chapter, we had estimated the kappa 
statistic using 10-fold cross-validation. We'll do the same here, using kappa to 
optimize the boosting parameter of the decision tree (boosting the accuracy of 
decision trees was previously covered in Chapter 5, Using Decision Trees and Rules).
The function
 function. These options 
allow for the management of model evaluation criteria such as the resampling 
strategy and the measure used for choosing the best model. Although this function 
can be used to modify nearly every aspect of a tuning experiment, we'll focus on two 
important parameters: and . If you're eager for more details, you can use the 
 help command for a list of all parameters.
Improving Model Performance
[ 334 ]
For the function, the parameter is used to set the 
resampling method, such as holdout sampling or k-fold cross-validation. The 
following table lists the shortened name string uses to call the method, as well 
Although the default options for these resampling methods follow popular 
and the complexity of your model.
Resampling method Method name Additional options and default 
values
Holdout sampling (training data proportion)
k-fold cross-validation (number of folds)
Repeated k-fold crossvalidation
 (number of folds)
 (number of 
iterations)
Bootstrap sampling (resampling iterations)
0.632 bootstrap (resampling iterations)
Leave-one-out cross-validation None
The parameter can be used to choose a 
function that selects the optimal model among the various candidates. Three such 
functions are included. The function simply chooses the candidate with the best 
functions are used to choose the most parsimonious (that is, simplest) model that 
is within a certain threshold of the best model's performance. The function 
chooses the simplest candidate within one standard error of the best performance, 
and 
 pacakage's ranking 
of models by simplicity. For information on how models are 
ranked, see the help page for the selection functions by typing 
 at the R command prompt.
 that uses 10-fold cross-validation and the 
 selection function, use the following command. Note that is 
included only for clarity; since this is the default value for , it could 
have been omitted.
We'll use the result of this function shortly.
Chapter 11
[ 335 ]
parameters to optimize. The grid must include a column for each parameter in the 
means we'll need columns with the names , , and . For other 
models, refer to the table presented earlier in this chapter. Each row in the data frame 
represents a particular combination of parameter values.
Rather than creating this 
possible combinations of parameter values—we can use the 
function, which creates data frames from the combinations of all values supplied. For 
example, suppose we would like to hold constant and 
 while searching eight different values of . This can be created as:
The resulting data frame contains rows:
Each row will be used to generate a candidate model for evaluation, built using that 
row's combination of model parameters.
Given this search grid and the control list created previously, we are ready to run a 
thoroughly customized experiment. As before, we'll set the random seed to 
while adding a parameter , indicating the statistic to be used by 
the model evaluation function—in this case, . The full command is as follows:
Improving Model Performance
[ 336 ]
Although much of the output is similar to the previously tuned model, there are 
a few differences of note. Because 10-fold cross-validation was used, the sample 
size to build each candidate model was reduced to 900 rather than the 1000 used in 
the bootstrap. As we requested, eight candidate models were tested. Additionally, 
because and were held constant, their values are no longer shown in 
the results; instead, they are listed as a footnote.
best model used whereas here, the best used . This 
 rule rather the 
 rule to select the optimal model. Even though the 35-trial model offers the 
best raw performance according to kappa, the 1-trial model offers nearly the same 
performance yet is a much simpler model. Not only are simple models more 
Chapter 11
[ 337 ]
Improving model performance with 
meta-learning
As an alternative to increasing the performance of a single model, it is possible to 
combine several models to form a powerful team. Just as the best sports teams have 
players with complementary rather than overlapping skillsets some of the best machine 
learning algorithms utilize teams of complementary models. Because a model brings 
a unique bias to a learning task, it may readily learn one subset of examples but have 
trouble with another. Therefore, by intelligently using the talents of several diverse 
team members, it is possible to create a strong team of multiple weak learners.
This technique of combining and managing the predictions of multiple models 
falls within a wider set of meta-learning methods that broadly encompass any 
technique that involves learning how to learn. This might include anything from 
simple algorithms that gradually improve performance by automatically iterating 
over design decisions—for instance, the automated parameter tuning used earlier 
in this chapter—to highly complex algorithms that use concepts borrowed from 
evolutionary biology and genetics for self-modifying and adapting to learning tasks.
For the remainder of this chapter, we'll focus on meta-learning only as it pertains to 
modeling a relationship between the predictions of several models and the desired 
outcome. The teamwork-based techniques covered here are quite powerful, and are 
Understanding ensembles
Suppose you were a contestant on a television trivia show that allowed you to 
million-dollar prize. Most people would try to stack the panel with a diverse set 
science, history, and art, along with a current pop-culture expert would be a safely 
a question that stumps the panel.
The meta-learning approach that utilizes a similar principle of creating a varied team 
of experts is known as an ensemble. All ensemble methods are based on the idea 
that by combining multiple weaker learners, a stronger learner is created. Using this 
simple principle, a large variety of algorithms has been developed distinguished 
largely by two questions:
How are the weak learners' predictions combined to make a single 
Improving Model Performance
[ 338 ]
When answering these questions, it can be helpful to imagine the ensemble in 
terms of the process diagram as follows; nearly all ensemble approaches follow 
this pattern.
First, input training data is used to build a number of models. The allocation function
dictates whether each model receives the full training dataset or merely a sample. 
Since the ideal ensemble includes a diverse set of models, the allocation function 
learners. For instance, it might use bootstrap sampling to construct unique training 
datasets or pass on a different subset of features or examples to each model. On the 
other hand, if the ensemble already includes a diverse set of algorithms—such as a 
might pass on the data relatively unchanged.
After the models are constructed, they can be used to generate a set of predictions, 
which must be managed in some way. The combination function governs how 
disagreements among the predictions are reconciled. For example, the ensemble might 
strategy such as weighting each model's votes based on its prior performance.
Some ensembles even utilize another model to learn a combination function from 
various combinations of predictions. For example, when M1 and M2 both vote 
the actual class value is usually , then the ensemble might ignore the votes of 
M1 and M2 and instead predict . This process of using the predictions of several 
stacking.
Chapter 11
[ 339 ]
in pursuit of a single best model. Instead, you can train a number of reasonably 
strong candidates and combine them. Yet convenience isn't the only reason why 
ensemble-based methods continue to rack up wins in machine learning competitions; 
ensembles also offer a number of performance advantages over single models:
Better generalizability to future problems: Because the opinions of several 
Improved performance on massive or miniscule datasets: Many models run 
into memory or complexity limits when an extremely large set of features 
than a single full model. Additionally, it is often trivial to parallelize an 
ensemble using distributed computing methods. Conversely, ensembles 
also do well on the smallest datasets because resampling methods like 
bootstrapping are inherently part of many ensemble designs.
The ability to synthesize of data from distinct domains: Since there is no 
ensemble's ability to incorporate evidence from multiple types of learners is 
increasingly important as Big Data continues to draw from disparate domains.
: Real-world 
phenomena are often extremely complex with many interacting intricacies. 
Models that divide the task into smaller portions are likely to more 
accurately capture subtle patterns that a single global model might miss.
take a look at several of the most popular ensemble methods and how they can be 
used to improve the performance of the credit model we've been working on.
Bagging
 gain widespread acceptance used a technique 
called bootstrap aggregating, or bagging for short. As described by in 
1994, bagging generates a number of training datasets by bootstrap sampling the 
original training data. These datasets are then used to generate a set of models using 
a single learning algorithm. The models' predictions are combined using voting 
For additional information on bagging, refer to: , 
, pp. 123-140, by (1996).
Improving Model Performance
[ 340 ]
Although bagging is a relatively simple ensemble, it can perform quite well as long 
as it is used with relatively unstable learners, that is, those generating models that 
tend to change substantially when the input data changes only slightly. Unstable 
models are essential to ensure the ensemble's diversity in spite of only minor 
variations between the bootstrap training datasets. For this reason, bagging is often 
used with decision trees, which have the tendency to vary dramatically given minor 
changes in input data.
The package offers a classic implementation of bagged decision trees. To 
train the model, the function works similar to many of the models used 
previously. The parameter is used to control the number of decision trees voting 
in the ensemble (with a default value of 
task and the amount of training data, increasing this number may improve the model's 
performance, up to a limit. The downside is that this comes at the expense of additional 
computational expense; a large number of trees may take some time to train.
After installing the package, we can create the ensemble as follows: 
We'll stick to the default value of 25 decision trees:
The resulting model works as expected with the function:
well. To see how this translates into future performance, we can use the bagged 
trees with 10-fold CV via the function in the package. Note that the 
method name for the bagged trees function is as follows:
Chapter 11
[ 341 ]
The kappa statistic of for this model suggests that the bagged tree model 
performs on par with our best-tuned C5.0 decision tree.
To get beyond bags of decision trees, the package also provides a more 
general function. It includes out-of-the-box support for a handful of models, 
though it can be adapted to more types with a bit of additional effort. The 
and one for aggregating the votes.
For example, suppose we wanted to create a bagged support vector machine (SVM) 
model, using the function in the package we used in Chapter 7, 
. The function 
requires us to provide functionality for training the SVMs, making predictions, and 
counting votes.
Rather than writing these ourselves, the package's built-in 
supplies three functions we can use for this purpose:
Improving Model Performance
[ 342 ]
By looking at the function, we see that it simply calls the 
function from the package and returns the result:
The and functions for are also similarly straightforward. By 
studying these functions and creating your own in the same format, it is possible to 
use bagging with any machine learning algorithm you would like.
The 
of naive Bayes models ( ), decision trees ( ), 
and neural networks ( ).
Applying the three functions in the list, we can create a bagging 
By using this with the function and the ) 
that the package is required for this to work; you may need to install it if 
you have not done so previously.
Chapter 11
[ 343 ]
Given that the kappa statistic is below 0.30, it seems that the bagged SVM model 
performs more poorly than the bagged decision tree model. It's worth pointing out 
that the standard deviation of the kappa statistic (labeled ) is fairly large 
compared to the bagged decision tree model. This suggests that the performance 
varies substantially among the folds in the cross-validation. Such variation may 
imply that the performance could be improved further by upping the number of 
models in the ensemble.
Boosting
Another popular ensemble-based method is called boosting, because it boosts the 
performance of weak learners to attain the performance of stronger learners. This 
method is based largely on the work of Rob Schapire and Yoav Freund, who have 
published extensively on the topic.
For additional information on boosting, refer to: 
and Algorithms Understanding Rule Learners by R. Schapire, and Y. 
Freund, (The MIT Press, 2012).
Schapire
and Freund discovered that boosting will result in performance often quite better 
and certainly no worse than the best of these models. Essentially, this allows one 
to increase performance to an arbitrary threshold simply by adding more weak 
Similar to bagging, boosting uses ensembles of models trained on resampled data 
and the vote is weighted based on each model's performance rather than giving each 
an equal vote.
Improving Model Performance
[ 344 ]
A boosting algorithm called AdaBoost, or adaptive boosting, was proposed in 1997. 
The algorithm is based on the idea of generating weak leaners that iteratively learn 
Beginning from an 
examples. The process continues until the desired overall error rate is reached or 
according to its accuracy on the training data on which it was built.
Though boosting principles can be applied to nearly any type of model, the 
principles are most commonly used with decision trees. We already used boosting in 
this way in Chapter 5, , as a method to improve the performance of a C5.0 decision tree. 
The AdaBoost.M1 algorithm provides an alternative tree-based implementation 
earlier, AdaBoost.M1 is not covered here.
The AdaBoost.M1 algorithm can be found in the R 
package. For more information refer to 
, Journal of Statistical 
, , pp. 1-35, by 
Garcia (2013).
Random forests
Another ensemble-based method called random forests (or decision tree forests) focus 
only on ensembles of decision trees. This method was championed by 
and Adele Cutler, and combines the base principles of bagging with random feature 
selection to add additional diversity to the decision tree models. After the ensemble of 
trees (the forest) is generated, the model uses a vote to combine the trees' predictions.
For more detail on how random forests are constructed, 
refer to Random forests, , pp. 5-32, 
by (2001).
Chapter 11
[ 345 ]
Random forests combine versatility and power into a single machine learning 
approach. Because the ensemble uses only a small, random portion of the full feature 
set, random forests can handle extremely large datasets, where the so-called "curse of 
dimensionality" might cause other models to fail. At the same time, its error rates for 
most learning tasks are on par with nearly any other method.
Although the term "Random Forests" is trademarked by 
 and Cutler (see 
 for details), the term is 
used sometimes colloquially to refer to any type of decision 
tree ensemble. A pedant would use the more general term 
"decision tree forests" except when referring to the algorithm 
by and Cutler. The following table lists the general strengths and weaknesses of random forest 
models. It's worth noting that relative to other ensemble-based methods, random 
forests are quite competitive and offer key advantages relative to the competition. 
Strengths Weaknesses
An all-purpose model that performs 
well on most problems
Can handle noisy or missing data; 
categorical or continuous features
Selects only the most important 
features
Can be used on data with an extremely 
large number of features or examples
Unlike a decision tree, the model 
is not easily interpretable
May require some work to tune 
the model to the data
Due to their power, versatility, and ease of use, random forests are quickly becoming 
one of the most popular machine learning methods. Later on in this chapter, we'll 
compare a random forest model head-to-head against the boosted C5.0 tree.
Improving Model Performance
[ 346 ]
Training random forests
Though there are several packages to create random forests in R, the 
package
and Cutler for automated tuning. 
The syntax for training this model is as follows:
As noted previously, by default, the function creates an ensemble 
of 500 trees that consider random features at each split (where is the 
number of features in the training dataset). Whether or not these parameters are 
appropriate depends on the nature of the learning task and training data. Generally, 
more complex learning problems and larger datasets (both more features as well as 
more examples) work better with a larger number of trees.
Chapter 11
[ 347 ]
The goal of using a large number of trees is to train enough that each feature has a 
chance to appear in several models. This is the basis of the default value 
for the 
substantial random variation occurs from tree-to-tree. For example, since the credit 
data has 16 features, each tree would be limited to splitting on 
features at any time.
Let's see how the default parameters work with the credit data. 
function ensures that the result can be repeated).
To look at a summary of the model's performance, we can simply type the resulting 
As expected, the output notes that the random forest included 500 trees and tried 4 
variables at each split. You might be alarmed at the seemingly poor resubstitution 
error according to the display confusion matrix—the error rate of 23.8 percent is far 
worse than any of the other ensemble methods so far. In fact, this confusion matrix 
out-of-bag error rate (labeled 
), which is an unbiased estimate of the test set error. 
This means that it should be a fairly reasonable estimate of future performance.
Improving Model Performance
[ 348 ]
The out-of-bag estimate is computed during the construction of the random forest. 
Essentially, any example not selected for a single tree's bootstrap sample can be used 
as a way to test the model's performance on unseen data. At the end of the forest 
construction, the predictions for each example each time it was held out are tallied, 
rate of such predictions becomes the out-of-bag error rate.
Evaluating random forest performance
As mentioned previously, the function is also supported by 
, which allows us to optimize the model while at the same time calculating 
performance measures beyond the out-of-bag error rate. To make things interesting, 
let's compare an auto-tuned random forest to the best auto-tuned boosted C5.0 
model we've been working on. We'll treat this experiment as if we were hoping to 
identify a candidate model for submission to a machine learning competition.
 and set our training control options. For the most accurate 
comparison of model performance, we'll use repeated 10-fold cross-validation: 10 
times 10-fold CV. While this means that the models will take a much longer time and 
we should be very sure that we're making the right choice—the winner of this 
showdown will be our only entry into the machine learning competition.
Next, we'll set up the tuning grid for the random forest. The only tuning parameter for 
this model is 
split. By default, we know that the random forest will use features. 
To be thorough, we'll also test values half of that, twice that, as well as the full set of 
features. Thus, we need to create a grid with values of , , , and as follows:
A random forest that considers the full set of features at each 
split is essentially the same as a bagged decision tree model.
Chapter 11
[ 349 ]
We can supply the resulting grid to the function with the 
follows. We'll use the kappa metric to select the best model.
The preceding command may take some time to complete as it has quite a bit of 
, , , and iterations:
side-by-side. For the random forest model the results are:
For the boosted C5.0 model the results are:
Improving Model Performance
[ 350 ]
With a kappa of , the random forest model with was the winner 
among these eight models. It was marginally higher than the best C5.0 decision tree, 
which had a kappa of . Based on these results, we would submit the random 
data, we have no way of knowing for sure whether it will end up winning; but given 
our performance estimates, it's the safer bet. With a bit of luck, perhaps we'll come 
away with the prize.
Summary
After reading this chapter, you now know the base techniques that can be used 
to win data mining and machine learning competitions. Automated tuning 
methods can assist with squeezing every bit of performance out of a single model. 
On the other hand, performance gains are also possible by creating groups of 
machine learning models that work together.
Although this chapter was designed to help you prepare competition-ready 
models keep in mind that your fellow competitors have access to the same 
techniques. You won't be able to get away with stagnancy; you have to keep 
working to add proprietary methods to your bag of tricks. Perhaps you can 
include an eye for detail in data preparation. In any case, practice makes perfect, 
so take advantage of open competitions to test, evaluate, and improve your own 
machine learning skillset.
In the next chapter—the last in this book—we'll take a bird's eye look at ways to 
You'll gain the knowledge needed to apply machine learning to tasks at the cutting 