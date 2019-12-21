#statistics about proteoms

options(stringsAsFactors = FALSE)
proteoms <- read.csv2('proteoms_info.csv')
plot(proteoms$Div.Time, proteoms$Proteom.volume)

actual_proteoms <- subset(proteoms, Proteom.volume > 100)
plot(actual_proteoms$Div.Time, actual_proteoms$Proteom.volume,
     main = 'Распределение протеомов объемом более 100 белков',
     ylab = 'Объем протеомаб шт. белков', xlab = 'Время дивергенции')

actual_small <- subset(actual_proteoms, Proteom.volume < 5000)
plot(actual_small$Div.Time, actual_small$Proteom.volume,
     main = 'Распределение протеомов объемом более 100 и менее 1000 белков',
     ylab = 'Объем протеомаб шт. белков', xlab = 'Время дивергенции')