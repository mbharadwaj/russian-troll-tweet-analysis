## Introduction

Experimental analysis of the tweets dataset published by FiveThirtyEight. Please refer their [article](https://fivethirtyeight.com/features/why-were-sharing-3-million-russian-troll-tweets/)
related to the dataset. The [dataset](git clone https://github.com/fivethirtyeight/russian-troll-tweets.git) is on github.

The primary goal was to use various leading cloud based machine-learning APIs in analyzing the content.
GCP, AWS and Azure were explored. Code samples to invoke APIs for "translate" are included in the repo.

## Setup to run code

The code is in python. You will need python 3.6.x or greater to be installed.

* Download the tweets dataset from github

      git clone https://github.com/fivethirtyeight/russian-troll-tweets.git
    
* Setup virtual env  

      virtualenv venv
      source venv/bin/activate

* Install all dependencies

      pip install -r requirements.txt
      
      
* Optionally install [Jupyter[(http://jupyter.org/)] locally.
  * Jupyter can also be installed as a [docker[(https://www.docker.com/)] container     


      docker run -p 8888:8888 jupyter/datascience-notebook      
      
## Translation APIs

### GCP

Get access to GCP and Translate by following instructions at:
https://cloud.google.com/translate/docs/translating-text

At the end of this process you will have downloaded a json file whcih has the credentials to 
access the translate API.

This file needs to be available to the code execution environment. Environment variable approach, as
suggested by GCP is the best to follow.

"google-cloud-translate" python library is used to programmatically access GCP translate.

### AWS

Get access to AWS and various services by following instructions at:
https://docs.aws.amazon.com/translate/latest/dg/what-is.html

Once AWS cli is installed and configured, the credentials needed will be available in the "default"
configuration. If the credentials for translate is not in the "default", the code will need to be changed.

"boto" python library is used to programatically access AWS translate.

### Azure

Setup access to API by following documentation from Microsoft
https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-text-how-to-signup

## Experiments and Analysis

### Jupyter notebook

A Jupyter based notebook [russian-troll-tweet-analysis.ipynb](./russian-troll-tweet-analysis.ipynb) shows how the CSV
files can be loaded and analyzed interactively. 

### Translation of "unclassified" content

The tweet dataset classifies the text into a few categories. The csv column "content" has the original content. "language"
column identifies the source language. "account_category" is the classification. 

The categories are "Fearmonger", "NewsFeed", "RightTroll", "LeftTroll", "Commercial", "HashtagGamer" and "NonEnglish".

Category "NonEnglish" is the one of interest for this analysis.

#### Steps

* The text "content" in the "NonEnglish" caterogy is translated to English
     * The "source" language is not specified in invoking the APIs
     * This is to test the capability of the different translate APIs

#### Results

* "aws_translated" folder has a sample of data that was translated with AWS      
* "azure_translated" folder has a sample of data that was translated with Azure      
* "gcp_translated" folder has a sample of data that was translated with GCP

The translation APIs are pricey. All of them charge by characters. 

For reference, all the translations in the "gcp_translated" cost about $100.      
     
#### Observations

* Google offers the most comprehensive set of source-target languages
* Google's limits are flexible. In the console invocation limit can be set to "unlimited"
* All platforms have limits for invocation and throttling
* AWS has few languages and for this analysis was lacking as it does not support Russian
* AWS fails when it can't detect the source language with a good confidence number
* AWS setup is the simplest. "translate" is available by default for the user in "administrator" IAM role
* GCP is reasonably straightforward. A single click to enable "translate" from console
* Azure setup seems a bit involved.
     * First the "Translator Text" API needs to picked from Marketplace 
     * A name is needed
     * Further needs a subscription "tier" to be picked
     * Finally a resource group has to be created 

## Classification using cloud ML

For all classification experiments data was prepared by selecting English content from "classified".
The file name has the category and this extracted and a CSV created with just the content and category.
The training data has 250 samples for each cateory.

Refer to [./prepare_data_for_cloud_ml.py](./prepare_data_for_cloud_ml.py)

The training data is created in [./cloud_ml/training_data.csv](./cloud_ml/training_data.csv)

### GCP

AutoML is the newest service offered by GCP. 

The training data csv was uploaded via AutoML UI. AutoML takes a while to ingest the data (order of 10s of minutes).
The next stage was training and it took hours.

### AWS

"Machine Learning" is the name of the service. 

Steps:
* Upload model to to S3 via AWS console
* Follow the steps in the Machine Learning console

Observations:
* The steps were straight-forward
* The model was created quite fast (order of minutes).
* The model had an F1 score of 60 
 
## To Do

* Compare translations from each platform
     * Manual validation (spot check)
     
### AWS
* Play around with the training data to increase F1

### GCP

### Azure
* Use ML APIs with training data and compare
     


                       