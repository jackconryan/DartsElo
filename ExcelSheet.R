##Read in librarys

library(readxl)
library(writexl)
library(openxlsx)



##Create Function

ExpectedWinPercenatge <- function( PlayerA, PlayerB){
  AWins <- 1/(1+10^((PlayerB-PlayerA)/400))
  BWins <- 1/(1+10^((PlayerA-PlayerB)/400))
  return(list(AWins,BWins,PlayerA,PlayerB))
}
NewRating <- function( PlayerAPct, PlayerBPct, PlayerA, PlayerB){
  PlayerA <- PlayerA+32*(1-PlayerAPct)
  PlayerB <- PlayerB+32*(0-PlayerBPct)
  return(list(PlayerA,PlayerB))
}


##Read in the sheets

Rankings <- read_excel("C:\\Users\\User\\Documents\\Elo\\Coolmoyne Leaderboards.xlsx", 
                                     sheet = "Starting Rank")
Matches <- read_excel("C:\\Users\\User\\Documents\\Elo\\Coolmoyne Leaderboards.xlsx", 
                                     sheet = "Matches")


##Extract the ratings

Daniel <- as.numeric(Rankings[1,2])
Eoghan <- as.numeric(Rankings[2,2])
Ricky <- as.numeric(Rankings[3,2])
Zak <- as.numeric(Rankings[4,2])


##Matches Data

for(i in 1:nrow(Matches)){
  PlayerA <- Matches[i,1]
  PlayerB <- Matches[i,4]
  
  for(j in 1:nrow(Rankings)){
    if (PlayerA[1, 1] == Rankings[j, 1]) {
      PlayerA = as.numeric(Rankings[j, 2])
      break
    }
  }
  for(k in 1:nrow(Rankings)){
    if (PlayerB[1, 1] == Rankings[k, 1]) {
      PlayerB = as.numeric(Rankings[k, 2])
      break
    }
  }
  
  Percentages<-ExpectedWinPercenatge(PlayerA,PlayerB)
  
  PlayerAPct <- Percentages[[1]]
  PlayerBPct <- Percentages[[2]]
  PlayerA <- Percentages[[3]]
  PlayerB <- Percentages[[4]]
  
  RatingsUpdate <- NewRating(PlayerAPct, PlayerBPct, PlayerA, PlayerB)
  
  PlayerA <- RatingsUpdate[[1]]
  PlayerB <- RatingsUpdate[[2]]
  
  Rankings[j,2] <- PlayerA
  Rankings[k,2] <- PlayerB
  

}

existing_wb <- loadWorkbook("C:/Users/User/Documents/Elo/Coolmoyne Leaderboards.xlsx")
removeWorksheet(existing_wb, sheet = 3)
addWorksheet(existing_wb, "Rankings")
writeData(existing_wb, sheet = "Rankings", x = Rankings, startRow = 1)
table_style <- createStyle(fontColour = "white", fgFill = "#0070C0", halign = "CENTER", textDecoration = "BOLD")
addStyle(existing_wb, sheet = "Rankings", style = table_style, rows = 1, cols = 1:ncol(Rankings))
saveWorkbook(existing_wb, "C:/Users/User/Documents/Elo/Coolmoyne Leaderboards.xlsx", overwrite = TRUE)
