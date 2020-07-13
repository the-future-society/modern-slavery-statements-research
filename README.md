# Research on Modern Slavery 

This repository is going to contain a collection of experiments and analyses performed on the Modern Slavery Statements Dataset.


## Introduction
[The UN Sustainable Development Goal 8.7](https://sustainabledevelopment.un.org/sdg8) states:
Take immediate and effective measures to eradicate forced labour, end modern slavery and human trafficking and secure the prohibition and elimination of the worst forms of child labour, including recruitment and use of child soldiers, and by 2025 end child labour in all its forms.

In 2018, [the Global Slavery Index](https://www.globalslaveryindex.org/2018/findings/highlights/) found that there were 40.3 M people in modern slavery, of whom 25M were in forced labor producing computers, clothing, agricultural products, raw materials, etc and 15M were in forced marriage.

[The Future Society](https://thefuturesociety.org/), an independent nonprofit think-and-do tank [launched a partnership](https://thefuturesociety.org/2020/06/23/project-aims-artificial-intelligence-against-modern-slavery/) with the [Walk Free Initiative](https://www.minderoo.org/walk-free/) to automate the analysis of modern slavery statements produced by businesses to boost compliance and help combat and eradicate modern slavery. [The team](https://thefuturesociety.org/our-team/) at The Future Society is curating an up-to-date repository of >16K modern slavery statements (and counting) to boost machine learning research in this area. The data is scraped based on the collection of report links provided by the [modernslaveryregistry.org](modernslaveryregistry.org).

By sharing your analysis and contributing to this repository you help the global community to hold multi-national corporations accountable for how they treat their workforce and suppliers.


## How to access the data?

The data is available in the `modern-slavery-dataset-txt` bucket in AWS S3. The future plans involve releasing the dataset for the general public access.

The bucket contains multiple copies of statements from various scraping runs so the logic is to always pick the latest folder.  The raw documents are found in the `/data/raw_statements/` folder in the `modern-slavery-dataset-raw`  bucket. Metadata is found in `s3://modern-slavery-dataset-raw/data/ms_registry/` following the same logic.

As it's work in progress, at present, if you'd like to work with this data, please send an email to edgar@bravetech.io with a link to your social profile (linkedin, facebook or similar ) and you'll receive IAM user credentials on the first possible instance that would allow you to download and access the data.

### Quickstart

First clone the repository
```
git clone https://github.com/the-future-society/modern-slavery-statements-research
```

#### Option 1 - notebook
Copy [this notebook](https://github.com/the-future-society/modern-slavery-statements-research/blob/master/notebooks/Tutorial%20-%20Download%20Corpus.ipynb) and follow the instructions there.

#### Option 2 - CLI

Navigate to the project folder.
```
modern-slavery-statements-research/modern_slavery_statements_research
```

If you've set up your modern slavery project related [AWS CLI](https://aws.amazon.com/cli/) credentials as default you can simply run
```
python download_corpus.py
```

If your modern slavery project credentials are not default you can specify them as arguments.
```
python download_corpus.py -i {aws_access_key_id} -a {aws_secret_access_key}
```

You can explore more options by running `python download_corpus.py --help`




## Get Help
If you'd like to get help with domain expertise or technical requirements and implementations then get in touch with [Adriana](mailto:adriana.bora@thefuturesociety.org) or [Edgar](mailto:edgar@bravetech.io) respectively.


## Roadmap

Over the next few weeks and months, the following improvements are planned to the dataset and the repository:

1. ~~Provide a convenient one-command entry point to the data~~, including download to a pandas dataframe.
2. Improve the dataset quality by continuously including more documents and improving the data cleaning pipeline.
3. Provide examples of analysis.
4. Provide manually annotaded labels for a subset of the corpus to enable analyses using supervised methods.
5. Open source the data and research for public access. 



## Citation

If you intend to share any form of public research and analysis based on the data from this repository and the `modern-slavery-dataset-raw` and `modern-slavery-dataset-txt` buckets in AWS S3, then please include the following citation to your publication:


The Future Society. (2020) Modern Slavery Statements Research. Retrieved from https://github.com/the-future-society/modern-slavery-statements-research.


## Contributions

Add Colab notebooks here.

- Rey Farhan's [initial exploration](https://colab.research.google.com/drive/1Xk3TZ-30CfNmUxxiDRrWh9S3nR74pZlj?usp=sharing).
