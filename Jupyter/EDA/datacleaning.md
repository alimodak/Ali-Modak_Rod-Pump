### Select a maximum acceptable percent null for columns to remain in the dataset

* We have already decided to drop three columns:

  `GrossStrokeLength` -> 53% null

  `gasanchor_od` -> 46% null

  `Fillage` -> 28% null

* And the following columns exhibit similarly high null percentages

  `max_unguided_sideload` -> 31% null

  `shallow_max_sideload` -> 31% null

  `overall_max_sideload` -> 31% null

  `YesterdaysAverageSPM` -> 36% null

#### The complexity of the sideload columns

We assume `overall_max_sideload` is the broadest of sideload categories:

All columns with a null `overall_max_sideload` value also have null `max_unguided_sideload` and `shallow_max_sideload` values

In our meeting with Sap and Sarah, they identified the sideload values as potentially very significant - it may be a bad idea to try and impute these values

Dropping null sideload values would decrease our sample size by 31%, to a final row count of 1187

### Identify columns with 'unknown' or 'other' members and decide how to address these values

* `pump_bore` -> 19 'other' values
* `DESANDDEGAS_TYP` -> 552 'unknown' values

### Identify columns with a large proportion of 'zero' members and understand the significance of these values

* `CHROME_LENGTH` -> 1708 zero values
* `POLY_LENGTH` -> 1707 zero values
* `ENDURALLOY_LENGTH` -> 1442 zero values
* `H2S_CONCENTRATION` -> 1627 zero values

