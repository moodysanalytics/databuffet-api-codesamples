Frequencies
-----------------------------
Frequency, freq, is an optional parameter. It performs a frequency conversion. 

| Value | Name |
|-------------|--------------|
| 0 | Default |
| 16 | INDEX  |
| 49 | Daily  |
| 50 | Business daily (Mon- Fri) |
| 65 | Weekly ending on Sunday  |
| 66 | Weekly ending on Monday |
| 67 | Weekly ending on Tuesday |
| 68 | Weekly ending on Wednesday |
| 69 | Weekly ending on Thursday |
| 70 | Weekly ending on Friday |
| 71 | Weekly ending on Saturday |
| 80 | 3 Times a month 10th, 20th and end of month  |
| 97 | Bi-Weekly, ending on alternating Sunday starting January, 27th 1850. <br>E.g. Jan 27 1850, Feb 10 1850, ... ,Dec 31 2017, Jan 14 2018, Jan 28 2018  |
| 98 | Bi-Weekly, ending on alternating Monday starting January, 14th 1850. <br>E.g. Jan 14 1850, Jan 28 1850, ... ,Dec 18 2017, Jan 1 2018, Jan 15 2018  |
| 99 | Bi-Weekly, ending on alternating Tuesday starting January, 15th 1850. <br>E.g. Jan 15 1850, Jan 29 1850, ... ,Dec 19 2017, Jan 2 2018, Jan 16 2018 |
| 100 | Bi-Weekly, ending on alternating Wednesday starting January, 16th 1850. <br>E.g. Jan 16 1850, Jan 30 1850, ... ,Dec 20 2017, Jan 3 2018, Jan 17 2018  |
| 101 | Bi-Weekly, ending on alternating Thursday starting January, 17th 1850. <br>E.g. Jan 17 1850, Jan 31 1850, ... ,Dec 21 2017, Jan 4 2018, Jan 18 2018  |
| 102 | Bi-Weekly, ending on alternating Friday starting January, 18th 1850. <br>E.g. Jan 18 1850, Feb 1 1850, ... ,Dec 22 2017, Jan 5 2018, Jan 19 2018  |
| 103 | Bi-Weekly, ending on alternating Saturday starting January, 19th 1850. <br>E.g. Jan 19 1850, Feb 2 1850, ... ,Dec 23 2017, Jan 6 2018, Jan 20 2018  |
| 104 | Bi-Weekly, ending on alternating Sunday starting January, 20th 1850. <br>E.g. Jan 20 1850, Feb 3 1850, ... ,Dec 24 2017, Jan 7 2018, Jan 21 2018  |
| 105 | Bi-Weekly, ending on alternating Monday starting January, 21st 1850. <br>E.g. Jan 21 1850, Feb 4 1850, ... ,Dec 25 2017, Jan 8 2018, Jan 22 2018 |
| 106 | Bi-Weekly, ending on alternating Tuesday starting January, 22nd 1850. <br>E.g. Jan 22 1850, Feb 5 1850, ... ,Dec 26 2017, Jan 9 2018, Jan 23 2018  |
| 107 | Bi-Weekly, ending on alternating Wednesday starting January, 23rd 1850. <br>E.g. Jan 23 1850, Feb 6 1850, ... ,Dec 27 2017, Jan 10 2018, Jan 24 2018  |
| 108 | Bi-Weekly, ending on alternating Thursday starting January, 24th 1850. <br>E.g. Jan 24 1850, Feb 7 1850, ... ,Dec 28 2017, Jan 11 2018, Jan 25 2018  |
| 109 | Bi-Weekly, ending on alternating Friday starting January, 25th 1850. <br>E.g. Jan 25 1850, Feb 8 1850, ... ,Dec 29 2017, Jan 12 2018, Jan 26 2018   |
| 110 | Bi-Weekly, ending on alternating Saturday starting January, 26th 1850. <br>E.g. Jan 26 1850, Feb 9 1850, ... ,Dec 30 2017, Jan 13 2018, Jan 27 2018   |
| 112 | Semi-Monthly, 15th and end of month  |
| 128 | Monthly  |
| 155 | Bi-Monthly, with year ending in November  |
| 156 | Bi-Monthly, with year ending in December  |
| 170 | Quarterly, with year ending in October |
| 171 | Quarterly, with year ending in November |
| 172 | Quarterly, with year ending in December  |
| 183 | Semi-Annual, with year ending in July |
| 184 | Semi-Annual, with year ending in August |
| 185 | Semi-Annual, with year ending in September |
| 186 | Semi-Annual, with year ending in October |
| 187 | Semi-Annual, with year ending in November  |
| 188 | Semi-Annual, with year ending in December  |
| 193 | Annual, with year ending in January  |
| 194 | Annual, with year ending in February |
| 195 | Annual, with year ending in March |
| 196 | Annual, with year ending in April |
| 197 | Annual, with year ending in May|
| 198 | Annual, with year ending in June |
| 199 | Annual, with year ending in July |
| 200 | Annual, with year ending in August |
| 201 | Annual, with year ending in September |
| 202 | Annual, with year ending in October |
| 203 | Annual, with year ending in November |
| 204 | Annual, with year ending in December |



Transformation
-----------------------------
Transformation, trans, is an optional parameter. 

| Value | Name |
|-------------|--------------|
| 0 | None (DEFAULT) |
| 1 | YearOverYearPctChange |
| 2 | SimpleDifference |
| 3 | AnnualizedGrowth |
| 4 | PctChange |
| 8 | YearOverYearDiff |

ConversionType
-----------------------------
Data Buffet provides for the conversion of a time series from its native frequency to a different output frequency (either higher or
lower), but the appropriate mathematical process depends on the nature of the series. There are three options, of which Cubic is the
default.

| Value | Name |
|-------------|--------------|
| 0 | Linear |
| 1 | Constant |
| 2 | Cubic (DEFAULT) |
| 3 | Discrete |


DateOption
-----------------------------

| Value | Name |
|-------------|--------------|
| 0 | StartAndEnd |
| 1 | Start |
| 2 | EntireSeries |
| 3 | Period |

