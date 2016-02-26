---
title: "Tweet Exploration"
author: "Scott Brenstuhl"
date: "December 8, 2015"
output: html_document
---


```r
library(dplyr)
library(lubridate)
```


```r
# Read in tweets produced by twitter_scraper.py
tweets <- read.csv('canidate_tweets.csv', stringsAsFactors = FALSE)

# convert Twitters API format to one we can work with
tweets$datetime <- paste(substr(tweets$created,27,31),
                         substr(tweets$created, 5, 19)) %>%
    ymd_hms() %>%
    as.POSIXct()

tweets$is_retweet <- ifelse(grepl('*RT', tweets$text), TRUE, FALSE)

# retain raw version in case its useful later
tweets$rawtext <- tweets$text

tweets$text <- gsub('\\\n',' ', tweets$text)

# Grab all links before removing punctuation charicters
tweets$links <- strsplit(tolower(tweets$text), " ") %>%
    lapply(grep, pattern= 'http', value = TRUE)

# Remove puntuation that isn't part of words
tweets$text <- gsub('[\\.\\\",!?:]', '', tweets$text)

tweets$hashtags <- strsplit(tolower(tweets$text), " ") %>%
    lapply(grep, pattern= '#', value = TRUE)

tweets$hashtags[tweets$hashtags == 'character(0)'] <- NA

tweets$mentions <- strsplit(tolower(tweets$text), " ") %>%
    lapply(grep, pattern= '@', value = TRUE)

# Split all the words out to work with, but ignore things that are in their own column
# should add quotation mark
tweets$split <- strsplit(tolower(tweets$text), " ") %>%
    lapply(grep, pattern= 'http|@|#|^(rt)$', value = TRUE, invert=TRUE)
```


```r
blobs <- group_by(subset(tweets, tweets$is_retweet==FALSE), canidate) %>%
    summarise(count = n(), 
              hashtags = paste(unlist(hashtags), collapse = ","),
              words = strsplit(paste(unlist(split), collapse = ","), ","),
              mentions = paste(unlist(mentions), collapse = ","),
              retweets = sum(retweets),
              likes = sum(likes)
              )


blobs$word_counts <- lapply(blobs$words, table) %>%
    lapply(sort, decreasing = TRUE)


blobs$word_counts[[1]]['weak']
```

```
## weak 
##    1
```

```r
sort(table(strsplit(blobs$words[1], ",")))
```

```
## Error in strsplit(blobs$words[1], ","): non-character argument
```

```r
?strsplit
Filter(function(x) !identical(character(0),x), blobs$hashtags[1])
```

```
## [1] "#nhpolitics,NA,#takeastand,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#unidosconbernie,NA,NA,NA,#peoplebeforepolluters,#exxonknew,#peoplebeforepolluters,#peoplebeforepolluters,#peoplebeforeprofits,#peoplebeforeprofits,#peoplebeforepolluters,#peoplebeforepolluters,NA,NA,NA,#postalbanking,#nhpolitics,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,#solidarity,NA,#fitn,NA,#periscope,NA,NA,#nhpolitics,#solidarity,#nhpolitics,#fitn,#nhpolitics,#periscope,#solidarity,#standwithpp,#solidarity,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#standwithpp,NA,NA,NA,#exxonknew,#worldaidsday,NA,NA,NA,NA,NA,NA,NA,NA,#fitn,#nhpolitics,#nhpolitics,NA,NA,#jjdinner,NA,#fitn,#jjdinner,#nhdpjj,NA,#jjdinner,#nhdpjj,#jjdinner,#nhdpjj,NA,NA,#nhdpjj,NA,NA,NA,#fitn,NA,NA,NA,NA,NA,NA,NA,#standwithpp,NA,#blackfriday,#blackfriday,NA,#blackfriday,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#nhpolitics,NA,NA,#orangetheworld,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinatl,#bernieinatl,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,#bernieinatl,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#2020approach,NA,NA,#2020approach,#2020approach,NA,#2020approach,NA,NA,#bernieinsc,NA,NA,NA,NA,NA,NA,#nhpolitics,NA,NA,#dapaanniversary,#transdayofrememberance,NA,NA,NA,NA,#justice4jamar,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieatgu,#bernieatgu,#blacklivesmatter,#bernieatgu,NA,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,#bernieatgu,NA,#bernieatgu,NA,#bernieatgu,#changingworkplaces,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#nhpolitics,NA,NA,NA,NA,#fightfor15,NA,NA,NA,NA,NA,#bernieinthecle,NA,NA,#bernieinthecle,NA,NA,#bernieinthecle,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinthecle,NA,NA,NA,NA,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#berniesright,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#berniesright,#debatewithbernie,NA,#ourwalmartvoices,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,NA,#debatewithbernie,NA,NA,NA,NA,NA,#debatewithbernie,#nhpolitics,NA,NA,NA,NA,NA,NA,NA,#millionstudentmarch,NA,NA,NA,NA,NA,NA,#blackoncampus,NA,NA,#fitn,NA,#veteransday,NA,NA,NA,#veteransday,#veteransday,#gopdebate,#gopdebate,#gopdebate,#gopdebate,#raisethewage,#gopdebate,NA,NA,NA,#fitn,NA,NA,NA,NA,#fightfor15,#fightfor15,#fightfor15,NA,#nhpolitics,NA,NA,#feelthebern,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinvegas,#bernieinvegas,#bernieinvegas,#bernieinvegas,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,#unidosconbernie,#bernieinsc,#bernieinsc,NA,NA,NA,NA,#fitn,NA,NA,#votingrights,#demforum,#demforum,#demforum,#demforum,NA,#demforum,#demforum,#demforum,#demforum,#demforum,#msnbc2016,NA,NA,NA,#keystonexl,NA,NA,#exxonknew,NA,NA,NA,NA,NA,NA,#fitn,NA,NA,NA,NA,NA,NA,#fitn,NA,NA,NA,#keepitintheground,#keepitintheground,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#electionday,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#nhpolitics,NA,NA,NA,#nhpolitics,NA,NA,NA,#yesonprop1,NA,NA,#rockinthebern,NA,NA,NA,NA,NA,#getthefacts,NA,NA,NA,NA,NA,#theirmoneytheirvote,#gopdebate,#studentsforbernie,#studentsforbernie,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#assaultatspringvalleyhigh,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#idpjj,#idpjj,#idpjj,#idpjj,#idpjj,#idpjj,#idpjj,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#rockinthebern,NA,NA,NA,NA,NA,NA,NA,NA,NA,#phonejustice,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#debatewithlarry,#demdebate,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#exxonknew,NA,NA,NA,NA,#blacklivesmatter,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#debatewithbernie,#demdebate,NA,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,NA,NA,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#demdebate,#demdebate,#demdebate,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#demdebate,#debatewithbernie,NA,#demdebate,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpp,#bernieinboulder,#bernieinboulder,NA,#bernie2016,#bernieinboulder,NA,NA,NA,NA,#bernieintucson,#bernieintucson,NA,#bernieintucson,NA,NA,NA,#tpp,#bernieintucson,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpp,#chci,#chci,#2015hhm,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpp,#stoptpp,NA,NA,#tpp,NA,#tpp,NA,NA,NA,NA,NA,NA,NA,#tpp,NA,#tpp,#stoptpp,NA,NA,#stoptpp,#stoptpp,NA,NA,NA,NA,NA,NA,NA,#bernieinboston,#bernieinma,#bernieinma,NA,#bernieinma,#bernieinma,#bernieinma,NA,#bernieinma,#bernieinma,#bernieinma,#bernieinma,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#standwithpp,#pinkout,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#iopsanders,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#iacaucus,NA,NA,NA,NA,NA,NA,#nhpolitics,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#feelthebern,NA,#popeinus,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieatunh,#bernieatunh,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#nhpolitics,#nhpolitics,NA,#nhpolitics,#nhdems2016,#unh,#bernieatunh,NA,NA,NA,#feelthebern,#colbern,#lssc,NA,NA,NA,NA,NA,NA,#uhspresidance,NA,NA,win#istandwithpp,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#gopdebate,#debatewithbernie,#gopdebate,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#gopdebate,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,NA,NA,NA,NA,NA,NA,#gopdebate,#debatewithbernie,NA,NA,NA,NA,#justicesummer,NA,NA,#iacaucus,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinva,#bernieinva,#bernieinva,#bernieinva,#bernieinva,NA,NA,NA,NA,NA,#libertyconvo,#libertyconvo,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinnc,#bernieinnc,NA,#bernieinnc,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinsc,NA,NA,NA,#bernieinsc,NA,#bernieinsc,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tbt,NA,NA,NA,NA,NA,NA,#irandeal,NA,NA,#irandeal,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#iacaucus,#hbdbernie,NA,NA,NA,#hbdbernie,NA,#iacaucus,#iacaucus,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,#bernie2016,NA,NA,NA,NA,NA,#uniteiowa,NA,NA,NA,#bernie2016,NA,NA,#dems15,#dems15,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,#bernie2016,#bernie2016,NA,NA,NA,NA,#bernie2016,NA,#bernie2016,#bernie2016,NA,NA,NA,#bernie2016,NA,#bernieinreno,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,#bernie2016,NA,#bernie2016,NA,#bernie2016,NA,#bernie2016,#bernie2016,#bernieinsc,#bernie2016,#bernieinsc,#bernie2016,#bernie2016,NA,NA,#bernie2016,NA,NA,#bernie2016,#bernieinsc,#bernieinsc,#bernieinsc,#bernieinsc,#bernie2016,#bernie2016,#bernie2016,#bernie2016,NA,#bernie2016,NA,#bernie2016,#bernie2016,#bernie2016,NA,NA,#tbt,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,#bernieinreno,#bernieinreno,#bernieinnv,#bernie2016,NA,NA,NA,NA,#bernie2016,#bernie2016,#bernie2016,#bernie2016,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#iacaucus,NA,#bernie2016,NA,#bernie2016,NA,NA,#iacaucus,NA,NA,#bernie2016,#notthebillionaires,NA,NA,#wingding,NA,#wingding,#wingding,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernieinla,#bernieinla,NA,#bernieinla,#bernieinla,#bernieinla,NA,NA,NA,NA,NA,NA,NA,#nurses,NA,NA,#dontshootpdx,NA,NA,NA,#bernieinportland,#bernieinportland,NA,#bernieinportland,#bernieinportland,#bernieinportland,#berniepdx,#bernieinportland,#bernieinportland,NA,NA,#bernie2016,NA,#iacaucus,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#debatewithbernie,#bts,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#vra50,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,NA,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#gopdebate,#gopdebate,#debatewithbernie,#gopdebate,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,#debatewithbernie,#debatewithbernie,#debatewithbernie,NA,NA,NA,#votingrights,#vra50,NA,NA,#vr50,#votingrights,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#shellno,NA,NA,NA,#saveourcities,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#medicare4all,#medicare4all,NA,#bernie2016,#bernie2016,#bernie2016,NA,#bernie2016,NA,NA,NA,#keystone,#tpp,NA,NA,NA,NA,NA,NA,NA,NA,NA,#blackwomenequalpay,NA,#bernie2016,NA,NA,NA,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#sclc,#sclc,#sclc,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#fightfor15,NA,NA,NA,NA,NA,NA,NA,NA,NA,#equalityforward,#fightfor15,NA,NA,NA,NA,NA,#fightfor15,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#blacklivesmatter,NA,NA,NA,NA,NA,NA,NA,NA,#nn15townhall,NA,#idphof,#idphof,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#irandeal,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,#teambernie,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,#periscope,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#scotus,NA,#votingrights,NA,NA,NA,NA,NA,NA,NA,NA,NA,#chairchats,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,NA,NA,NA,#periscope,NA,#fitn,#nhpolitics,#lovewins,NA,#periscope,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpp,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,#periscope,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpa,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tpa,#tpp,#iacaucus,NA,#nafta,NA,#tpp,#tpa,#tpa,#tpa,NA,NA,NA,NA,#blacklivesmatter ,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,#bernie2016,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#bernie2016,NA,#mn,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#periscope,#periscope,#periscope,#periscope,NA,#bernie2016,NA,NA,NA,NA,NA,#instagram,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#teambernie,NA,#collegeforall,NA,NA,NA,NA,#collegeforall,#collegeforall,#collegeforall,#collegeforall,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#notpp,NA,NA,NA,NA,NA,NA,NA,NA,#wadr,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#tbt,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#nh,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#southcarolina,#sc,#washingtondc,NA,#newhampshire,NA,#newhampshire,NA,NA,#msnbc,NA,NA,#tpp,NA,NA,NA,#tpp,NA,NA,NA,#chicago,NA,#sf,#austin,NA,#lasvegas,#vegas,NA,NA,#sanfrancisco,NA,NA,NA,#chicagoelection2015,#chicago,NA,#berniesbrigade,NA,NA,NA,#newhampshire,NA,NA,NA,NA,NA,NA,#npclunch,NA,NA,NA,#keystonexl,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,#netneutrality,NA,NA,NA,#iowa,NA,NA,NA,NA,NA,NA,NA"
```

```r
View(head(blobs))
```

```
## Error in check_for_XQuartz(): X11 library is missing: install XQuartz from xquartz.macosforge.org
```

```r
names(tweets)
```

```
##  [1] "id"         "canidate"   "created"    "text"       "likes"     
##  [6] "retweets"   "datetime"   "is_retweet" "rawtext"    "links"     
## [11] "hashtags"   "mentions"   "split"
```


