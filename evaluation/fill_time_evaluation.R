library(ggplot2)
n <- as.numeric(seq(200, 2000, 200))
pt<-n^2
EFCI_time <- c(0.6213223,  2.1391383,  4.7030277,  8.6129912, 12.804200, 18.6040736,
                   25.3454888, 35.5477936, 43.6108282, 52.9715368)/8
Scan_flood_Fill_time <- c(0.9488865,3.6848951,  8.1348466, 14.0689563, 22.0978533, 32.9906861,
                   45.3960636, 59.6061367, 75.6862172, 93.7243237)/8
EFCI <- data.frame(
  pt = n^2,
  time = EFCI_time
)

Scan_flood_Fill <- data.frame(
  pt = n^2,
  time = Scan_flood_Fill_time
)

log_EFCI <- data.frame(
  pt = n^2,
  log_time = log(EFCI_time)
)
log_Scan_flood_Fill <- data.frame(
  pt = n^2,
  log_time = log(Scan_flood_Fill_time)
)


prescription <- merge(x = EFCI, y = Scan_flood_Fill, suffixes = c(".EFCI",".Scan-flood Fill"), by="pt")
prescriptionMelted <- reshape2::melt(prescription, id.var='pt')
head(prescriptionMelted)

ggplot(prescriptionMelted, aes(x=pt, y=value, col=variable)) + 
  geom_line(size = 3)+
  xlab('points in an image') +
  ylab('filling time(s)')+
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=14,face="bold")) 


EFCI_time_lm <- lm(EFCI_time~pt)
summary(EFCI_time_lm)

Scan_flood_Fill_time_lm <- lm(Scan_flood_Fill_time ~ pt)
summary(Scan_flood_Fill_time_lm)


ggplotRegression <- function (fit) {
  
  require(ggplot2)
  
  ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) + 
    geom_point() +theme(axis.text=element_text(size=12),
                        axis.title=element_text(size=14,face="bold"))+
    stat_smooth(method = "lm", col = "red") +
    labs(title = paste("Adj R2 = ",signif(summary(fit)$adj.r.squared, 5),
                       "Intercept =",signif(fit$coef[[1]],5 ),
                       " Slope =",signif(fit$coef[[2]], 5),
                       " P =",signif(summary(fit)$coef[2,4], 5)))
}

#ggplotRegression(EFCI_time_lm)
#ggplotRegression(Scan_flood_Fill_time_lm)
#ggplotRegression(Scan_fill_time_lm)


fit <-EFCI_time_lm
fit2<-Scan_flood_Fill_time_lm
ggplot(prescriptionMelted, aes(x=pt, y=value, col=variable)) + 
  geom_line(size = 3)+
  xlab('pixels in an image') +
  ylab('filling time(s)')+
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=14,face="bold")) +
  labs(title = paste("EFCI Adj R2 = ",signif(summary(fit)$adj.r.squared, 5),
                     "Intercept =",signif(fit$coef[[1]],5 ),
                     " Slope =",signif(fit$coef[[2]], 5), "\n",
       "Scan-flood Fill Adj R2 = ",signif(summary(fit2)$adj.r.squared, 5),
       "Intercept =",signif(fit2$coef[[1]],5 ),
       " Slope =",signif(fit2$coef[[2]], 5)))



