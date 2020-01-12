######################################################################################################################################
#1. Load packages
######################################################################################################################################
rm(list=ls(all=TRUE)) #empties your R environment

#Load packages - you will have to install the packages first time you run the script
# install.packages("devtools")
library(devtools)
# install.packages("digest")
# install_github("MRCIEU/TwoSampleMR") #re-run this to update MR BASE
library(TwoSampleMR)
# install.packages("ggplot2")
library(ggplot2)
# install.packages("knitr")
library(knitr)
# install_github('qingyuanzhao/mr.raps')
library(mr.raps)
#
library(MRInstruments)

######################################################################################################################################
#2. Read in exposure and outcome; harmonise
######################################################################################################################################
# trait_list names = 
#SLEEP: sleepless/insomnia 'UKB-b:3957 & UKB-a:13' ; chronotype '1087', sleep duration 'UKB-b:4424';Diagnoses - main ICD10: G47 Sleep disorders id:UKB-a:527 ; sleep apnoea UKB-b:16781 (JSON read ERR) ; 
#WELLBEING: subj wellbeing 1009/1018 ; Happiness || id:UKB-b:4062
#LONELINESS: loneliness UKB-b:8476
#PHYSICAL activity: 'UKB-b:13702','UKB-b:151','UKB-b:2115','UKB-b:4710'(n days moderate activity),'UKB-b:8865','UKB-b:4000' (sports club) 
#PERSONALITY: '113', '114', '115', '116' (JSON read ERR), '117'
#SOCIAL: UKB-b:4171' (pub/social club), 'UKB-b:5076' (none), 'UKB-b:4077'(other), 'UKB-b:4000' (sports club), 'UKB-b:1553' (adult class), 'UKB-b:4667' (religious)
#WORKHRS: 'UKB-b:1712' (shifts), 'UKB-b:10162'(night shifts)
#SCHIZO: 22
#DEPRESS: 1187 (MDD), 1000 (depressive symptoms)
#ANXIETY: UKB-b:17243 (anxiety/panic), UKB-b:6519 (worrier/anxious feelings)
#ALCOHOL: UKB-b:5779 (alcohol freq)
#SMOK: 961 (cigs/d)
#DRUGS: UKB-b:1585 (psychoative substance use)
#DIGITAL: UKB-b:4779 (games) UKB-a:6 (computer) UKB-b:17999 (mobile use)
#EDU: 1239 (years of schooling)
#BMI: UKB-b:19953 
#OCD: 1189
#Intelligence: UKB-b:5238

#For game organised: first line are modifiable risk factors, second line are psychological traits/pathologies
trait_list <- c('UKB-b:4424','UKB-b:8476','UKB-b:4710','UKB-b:4077','UKB-b:10162','UKB-b:5779','961','UKB-b:1585','UKB-b:4779','UKB-b:17999','1239','UKB-b:19953',
                '1018','22','1187','UKB-b:6519','1189','UKB-b:5238'
                )

exposure_dat <- extract_instruments(outcomes=trait_list,
                                    #force_server = TRUE (was causing issue returning 404 html page into json)
                                    )
outcome_dat <- extract_outcome_data(exposure_dat$SNP, trait_list,
                                    proxies = 1, 
                                    rsq = 0.8, 
                                    align_alleles = 1, 
                                    palindromes = 1, 
                                    maf_threshold = 0.3)
dat <- harmonise_data( 
  exposure_dat = exposure_dat,
  outcome_dat = outcome_dat,
  action = 2
)

######################################################################################################################################
#3. Run MR & save report
######################################################################################################################################

res <- mr(dat)
res

setwd("C:/Users/Chris Moreno-Stokoe/OneDrive/Documents/Research/G4S - Games for Science/data") #change to your location
write.csv(res, "estimatorNetwork.csv", row.names=F, quote=F)
