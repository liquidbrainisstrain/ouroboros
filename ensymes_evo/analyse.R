options(stringsAsFactors=FALSE)
#при рассмотрении варианта с матрицей, где имена строк - все возможные буквы, а значения - количество букв в данной позиции
#для этого стоит отсортировать лексиграфически

formate_sins <- function(filename){
  data <- read.csv2(filename)
  cleaner <- function (sample){
    cell <- unlist(strsplit(unlist(strsplit(as.character(sample), ' ', fixed = T)), '-', fixed = T))
    tabl <- data.frame(numbers = as.numeric(cell[seq(2, length(cell), 2)]), letters = cell[seq(1, length(cell), 2)], stringsAsFactors = F)
    return(tabl)
  }
  result <- list()
  for (i in (1:length(data[2,]))){
       result <- c(result, list(cleaner(data[2,][i])) )
   }
  return(list(data[1,], result))
}

make_fac <- function(result){

}

work <- formate_sins('/Users/liquidbrain/projects/proteomics/ensymes_evo/result.csv')
sample <- work[[2]][[96]]
resample <- as.factor(rep(sample$letters, sample$numbers))
