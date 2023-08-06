# pyduq

pyduq [py = python, d=data quality, uq = University of QLD, Australia]

This project is a generic, meta-driven data quality validation suite. This project
was developed by Shane J. Downey as part of his M.Phil research study. 

The purpose of pyduq is to provide a detailed analysis of the quality of data by
comparing actual data against a set of generic data quality rules. The data quality 
rules are an implementation of LANG. LANG is a prior research study that provided
a set of data quality pseudo-SQL statements that implement the 8 dimensions of 
data quality.

pyduq has been provided as open source unde the GNU licence. 

pyduq - get all your data ducks in a row!

Documentation:
--------------
Please see the /doc folder on the Homepage for detailed instrucitons on usage.

Examples:
---------
Please see the /examples folder on the Homepage for many examples of using pyduq features to validate Open Data sources.

Installation:
--------------
Before installing pyduq some prerequisties must be installed:

pip install dicttoxml
pip install unidecode

python 
import nltk
nltk.download('stopwords')


References
----------
Jayawardene, V., Sadiq, S., & Indulska, M. (2013). An Analysis of Data Quality Dimensions. Retrieved from http://espace.library.uq.edu.au/view/UQ:312314/n2013-01_TechnicalReport_Jayawardene.pdf

Zhang, R., Jayawardene, V., Indulska, M., Sadiq, S., & Zhou, X. (2014). A Data Driven Approach for Discovering Data Quality Requirements. 
ICIS 2014 Proceedings, 1–10. Retrieved from http://aisel.aisnet.org/icis2014/proceedings/DecisionAnalytics/13

