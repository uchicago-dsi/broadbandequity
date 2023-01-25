#### Priorities for Winter 2023:

+ Finishing the standard dataframe and fixing the edge case issues surrounding overlap.
  + The “edge case issues” involve overlap between census tracts and neighborhoods. Because neighborhoods are created by socialization in an area but census tracts are methodologically created, they do not perfectly align. Some census tracts then exist within multiple neighborhoods.   + We need to decide how to assign a census tract to a neighborhood or multiple neighborhoods. Our current code assigns a census tract to a neighborhood if at least 40% of the census tract’s area overlaps with the neighborhood.
  + The code for the standard dataframe and the edge case issue is found within: lib/standard_dataframe.py
+ Providing a dataset to Jared to run some models (possibly with the students)
+ Updates
  + Newer data (which data needs to be updated? acs? census? )
  + What code needs to be changed (and where in the code base) for race to be better encoded
  + Updated definition of internet access / availability (where in code would this change?)
+ Documentation and cleaning up the repository
+  While we do want to pursue the neighborhood level, we want to run the analysis by census tract as well. We need to add code to create a standard dataframe at the census level - this shouldn’t take much extra code
+ Think about the one-year versus five-year estimates. Also the change over time, with the pandemic as an exogenous shock, would be important in this work — having two timepoints (2014/15-2019 versus 2018-2022  AND comparing pre-pandemic to current one-year estimates (2022 and 2021))
  + For more information, see: https://www.census.gov/data/developers/data-sets/acs-5year.html
+ Adding additional cities, depending on time

---

#### Other notes:

+ Notes on the Race Variable:
  + Do we use a one-year estimate and a five-year estimate and compare?
  + Just one note on that existing dataset on the portal that Marc mentions. As far as I recall, the output from this data merge needs to be updated as far as how it processes the ACS data on race/Hispanic ethnicity. Many computer scientists are not aware of the conventions for using Census data on race and Hispanic ethnicity. Here are the basics:
  + The “race” variable includes black, white, various Asian national origins, and others, but does not include “Hispanic/Latino.”
  + There is a separate “Hispanic” variable that indicates whether the respondent is Hispanic/Latino or not (and then some subcategories of different H/L national origins, e.g., Mexican, Cuban, Puerto Rican, etc.
  + Given that convention is to report the major “race” groups as white, black, Hispanic, Asian, American Indian, and other, it is necessary to process and report the data as: “Hispanic (of any race);” “non-Hispanic white,” “non-Hispanic black,” “non-Hispanic Asian,” etc.
  + It is also now possible to choose more than one race category, so that could be “non-Hispanic two or more races.”
+ I believe that the existing dataset on the portal does not separate out “Hispanic” from “non-Hispanic” in the various racial groups as noted in #3. So the students would need to make that change before using that codebase for the clinic project. This was done correctly for the spring clinic project in Chicago.

----

#### Tabled Questions
