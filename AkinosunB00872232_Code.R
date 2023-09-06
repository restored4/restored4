# loading the required libraries
library (nnet)
library(MASS)
library(dplyr)
library(tidyverse)
install.packages("devtools")
devtools::install_github("r-lib/conflicted", force = TRUE)

# importing  the data set
my_data <- read.csv("C:/Users/MY PC/Downloads/sanitation.csv")

# previewing the data
head(my_data)

# data cleaning
# removing unwanted columns
my_data <- select(my_data, Region, Residence.Type, Year, Population, Service.level)
colnames(my_data)

# changing column names
colnames(my_data) <- c("Income", "Location", "Year", "Population", "Sanitation_level")
colnames(my_data)
head(my_data)

# using ggplot to visualize relationships between response and covariates
# ggplot(data=my_data, aes(x=Population, y=Sanitation_level, color=Location)) + geom_point() + facet_grid(Year~Income)
ggplot(data=my_data, aes(x=Location, y= Population, color=Sanitation_level)) + geom_point() + facet_grid(Income~Year)

# scaling the Population column to smaller values
my_data$Population <- my_data$Population/1000000
# my_data$Population <- round(my_data$Population, 0)

# changing categorical variables to numeric keys
my_data$Income <- factor(my_data$Income, levels = c("Low-income", "Lower-middle-income", "Upper-middle-income", "High-income"), labels = c(1,2,3,4))
my_data$Sanitation_level <- factor(my_data$Sanitation_level, levels = c("Open defecation","Unimproved", "Limited service", "Basic service", "Safely managed service"), labels = c(1, 2, 3, 4, 5))
my_data$Location <- factor(my_data$Location, levels = c("rural", "urban"), labels = c(1, 2))
head(my_data)

# visualizing the ggplot after scaling population values and changing categorical variables to numeric
ggplot(data=my_data, aes(x=Location, y= Population, color=Sanitation_level)) + geom_point() + facet_grid(Income~Year)

# visualizing with box plot
ggplot(my_data, aes(x = Income, y = Population)) +
  geom_boxplot() +
  xlab("Income") +
  ylab("Population") +
  ggtitle("Box Plot of Income against Population")

ggplot(my_data, aes(x = Sanitation_level, y = Population)) +
  geom_boxplot() +
  xlab("Sanitation Level") +
  ylab("Population") +
  ggtitle("Box Plot of Population against Sanitation Level")

ggplot(my_data, aes(x = Location, y = Population)) +
  geom_boxplot() +
  xlab("Location") +
  ylab("Population") +
  ggtitle("Box Plot of Location against Population")

library(ggplot2)

# bar charts of other categorical variables against Population
ggplot(my_data, aes(x = Sanitation_level, y = Population)) +
  geom_bar(stat = "identity")
ggplot(my_data, aes(x = Location, y = Population)) +
  geom_bar(stat = "identity")
ggplot(my_data, aes(x = Income, y = Population)) +
  geom_bar(stat = "identity")
# bar chart of Population against Year
ggplot(my_data, aes(x = Year, y = Population)) +
  geom_bar(stat = "identity")

# fitting the model using Multinomial Logistic Regression
library(nnet)
mlr_model <- multinom(Sanitation_level ~ Location + Year + Income + Population, data = my_data)
# print mlr_model
summary(mlr_model)

# fit MLR without 'year'
#mlr_model2 <- multinom(Sanitation_level ~ Location + Income + Population, data = my_data)
# print mlr_model2
#summary(mlr_model2)

# fit the model using Poisson Regression with log link
# converting Sanitation level (response variable) to numeric
#my_data$Sanitation_level <- as.numeric(as.character(my_data$Sanitation_level))
# Fit Poisson regression model
#pr_model <- glm(Sanitation_level ~ Location + Income + Population, data = my_data, family = poisson(link = "log"))
# print Poisson model summary
#summary(pr_model)
# checking model accuracy using chi-square test
#chi_sq <- anova(pr_model, test = "Chisq")
# Print the chi-square test results
#print(chi_sq)


# fitting the model using Ordinal Logistic Regression
library(MASS)
olr_model <- polr(Sanitation_level ~ Location + Year + Income + Population, data = my_data)
# print olr_model
summary(olr_model)

# fit ordinal logistic regression model without 'year'
#olr_model2 <- polr(Sanitation_level ~ Location + Income + Population, data = my_data)
# print olr_model
#summary(olr_model2)

# fit the model using Random Forest algorithm
install.packages("randomForest")
library(randomForest)
rf_model <- randomForest(Sanitation_level ~ Location + Year + Income + Population, data = my_data)
# print rf_model
print(rf_model)

# fit random forest model without 'year'
#rf_model2 <- randomForest(Sanitation_level ~ Location + Income + Population, data = my_data)
# print rf_model
#print(rf_model2)