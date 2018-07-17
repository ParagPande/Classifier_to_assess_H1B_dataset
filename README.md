# Classifier_to_assess_H1B_dataset
This project aims at creating a classifier which predicts the status of a H1B visa application

The H1B is an employment-based, non-immigrant visa category for temporary foreign workers in the United States. For a foreign national to apply for H1B visa, an US employer must offer a job and petition for H1B visa with the US immigration department. This is the most common visa status applied for and held by international students once they complete college/ higher education (Masters, Ph.D.) and work in a full-time position.

Dataset can be accessed at https://www.kaggle.com/nsharan/h-1b-visa

The columns in the dataset include:

CASE_STATUS: Status associated with the last significant event or decision. Valid values include “Certified,” “Certified-Withdrawn,” Denied,” and “Withdrawn”.
EMPLOYER_NAME: Name of employer submitting labour condition application.
SOC_NAME: the Occupational name associated with the SOC_CODE. SOC_CODE is the occupational code associated with the job being requested for temporary labour condition, as classified by the Standard Occupational Classification (SOC) System.
JOB_TITLE: Title of the job
FULL_TIME_POSITION: Y = Full Time Position; N = Part Time Position
PREVAILING_WAGE: Prevailing Wage for the job being requested for temporary labour condition. The wage is listed at annual scale in USD. The prevailing wage for a job position is defined as the average wage paid to similarly employed workers in the requested occupation in the area of intended employment. The prevailing wage is based on the employer’s minimum requirements for the position.
YEAR: Year in which the H1B visa petition was filed
WORKSITE: City and State information of the foreign worker’s intended area of employment
lon: longitude of the Worksite
lat: latitude of the Worksite


