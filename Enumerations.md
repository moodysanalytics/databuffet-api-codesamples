Frequencies
-----------------------------
Frequency, freq, is an optional parameter. It performs a frequency conversion. 

| value | name |
|-------------|--------------|
| 0 | UNDEFINED (DEFAULT) |
| 16 | INDEX  |
| 49 | DAILY  |
| 50 | BUSINESS , BUSINS  |
| 65 | WSUNDAY , WSUN  |
| 66 | WMONDAY , WMON |
| 67 | WTUESDAY , WTUE |
| 68 | WWEDNESDAY , WWED |
| 69 | WTHURSDAY , WTHU |
| 70 | WFRIDAY , WFRI |
| 71 | WSATURDAY , WSAT |
| 80 | TENDAY  |
| 97 | BWSUN1  |
| 98 | BWMON1  |
| 99 | BWTUE1  |
| 100 | BWWED1  |
| 101 | BWTHU1  |
| 102 | BWFRI1  |
| 103 | BWSAT1  |
| 104 | BWSUN2  |
| 105 | BWMON2  |
| 106 | BWTUE2  |
| 107 | BWWED2  |
| 108 | BWTHU2  |
| 109 | BWFRI2  |
| 110 | BWSAT2  |
| 112 | SEMMON  |
| 128 | MONTHLY , MONTH   |
| 155 | BIMNOV  |
| 156 | BIMDEC  |
| 170 | QTROCT  |
| 171 | QTRNOV  |
| 172 | QUARTERLY ,QTRDEC   |
| 183 | SEMJUL  |
| 184 | SEMAUG  |
| 185 | SEMSEP  |
| 186 | SEMOCT  |
| 187 | SEMNOV  |
| 188 | SEMIANNUAL  |
| 193 | ANNJAN  |
| 194 | ANNFEB  |
| 195 | ANNMAR  |
| 196 | ANNAPR  |
| 197 | ANNMAY  |
| 198 | ANNJUN  |
| 199 | ANNJUL  |
| 200 | ANNAUG  |
| 201 | ANNSEP  |
| 202 | ANNOCT  |
| 203 | ANNNOV  |
| 204 | ANNUAL , ANNDEC  |



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

