library(mongolite)
library(ggplot2)
pept_all <- mongo(collection="mono_counted1", db="bioregulation", url="mongodb://localhost:27017/");

#-----------------KE----------------------
ke_df <- data.frame(name = pept_all$find()$name,
                    len = pept_all$find()$length,
                    loc = pept_all$find()$location,
                    fun = pept_all$find()$Function,
                    c_ke = pept_all$find()$c_ke,
                    t_ke = pept_all$find()$t_ke)

nucl <- subset(ke_df, loc == "nucleus")
nucl$loc <- "Ядерные"
membr <- subset(ke_df, loc == "membrane")
membr$loc <- "Мембранные"
cyt <- subset(ke_df, loc =="cytoplasm")
cyt$loc <- "Цитоплазматические"
oth <- ke_df[which((ke_df$loc != "nucleus") & (ke_df$loc != "membrane") & (ke_df$loc != "cytoplasm") & (ke_df$loc != "?")),]
oth$loc <- "Прочие"
membr_r <- membr[sample(1:3951, 3951),]
other <- subset(ke_df, (loc != 'nucleus' & loc != 'membrane'))
nucletmembr_r <- rbind(nucl, membr_r)
nucletmembr <- subset(ke_df, (loc == "nucleus" | loc == "membrane"))
# breaks = seq(0, 1500, 100)

new <- rbind(nucl, oth)
w <- new[which(new$c_ke > 0),]
w$c_ke <- log(w$c_ke)
ggplot(w, aes(c_ke, fill = loc))+
  geom_density(col = "black", alpha = 0.5)+
  theme(plot.caption=element_text(size=15))+
  scale_x_continuous(name = "Среднее значение натурального логарифма количества вхождений KE в белок", breaks = seq(0, 8, 1))+
  scale_y_continuous(name = "Количество белков, тысячи",  breaks = seq(0, 2, 0.2))+
  labs(caption = "Распределение белков в зависимости от количества вхождений KE в последовательность")

#t tests
t.test(nucl$c_ke, cyt$c_ke)
length(which(membr$c_ke == 0))


#t tests less 400
one400 <- subset(ke_df, len < 401)
onenuc <- subset(one400, loc == "nucleus")
onemem <- subset(one400, loc == "membrane")
onecyt <- subset(one400, loc =="cytoplasm")
oneoth <- one400[which((one400$loc != "nucleus") & (one400$loc != "membrane") & (one400$loc != "cytoplasm") & (one400$loc != "?")),]
t.test(onenuc$c_ke, onemem$c_ke)



#old spearman rows
vr_med_nucl <- c(3.586, 2.193, 1.756, 1.490, 1.283, 1.112, 0.962, 0.830, 0.707, 0.596, 0.487, 0.361, 0)
vr_count_nuc <- c(328, 315, 281, 297, 272, 260, 259, 256, 240, 198, 216, 239, 163)
vr_count_mem <- c(109, 121, 159, 174, 203, 223, 229, 249, 294, 423, 284, 316, 334)
vr_count_cyt <- c(330, 320, 310, 291, 274, 279, 275, 230, 213, 152, 192, 184, 137)
vr_count_oth <- rep(1000, length(vr_count_mem))
vr_count_oth <- vr_count_oth - vr_count_mem - vr_count_nuc - vr_count_cyt
w_df <- data.frame(med = vr_med_nucl, nuc = vr_count_nuc, mem = vr_count_mem, cyt = vr_count_cyt, oth = vr_count_oth)

zero_ke <- subset(ke_df, t_ke == 0)
zero_r <- zero_ke[sample(1:5413, 1000),]

ggplot(nucletmembr, aes(x = c_ke, col = loc, fill = loc))+
  geom_histogram()+
  facet_grid(loc~.)

ggplot(nucletmembr, aes(x = c_ke, fill = loc))+
  geom_density()+
  facet_grid(loc~.)

ggplot(ss, aes(loc,c_ke))+
  geom_smooth()

t.test(nucl$c_ke, membr$c_ke)
hist(log10(nucl$c_ke), 
     xlab = "Decimal logarithm of the number of KE in sequence", ylab="Number of proteins",
     main = "Distribution of KE in human nuclear proteins normalized by decimal logarithm")
hist(log10(membr$c_ke), 
     xlab = "Decimal logarithm of the number of KE in sequence", ylab="Number of proteins",
     main = "Distribution of KE in human membrane proteins normalized by decimal logarithm")

ggplot(w_df, aes(x = med, y = nuc))+
  geom_point(color = "red", size = 5)+
  scale_fill_manual(values = vr_med_nucl)+
  geom_smooth(method = "lm", se = FALSE, color = "grey")+
  theme(plot.caption=element_text(size=15))+
  scale_x_continuous(name = "Средний процент вхождения KE", breaks = seq(0, 4, 0.5))+
  scale_y_continuous(name = "Количество ядерных белков в ранге")+
  labs(caption = "Рис.2 Зависимость среднего процента вхождения KE в ранг от количества ядерных белков")

ke_df <- subset(ke_df, ke_df$loc != "?")
top100c <- ke_df[order(ke_df$c_ke, decreasing = T),][1:100,]
top100t <- ke_df[order(ke_df$t_ke, decreasing = T),][1:100,]
write.csv(top100c, file="top100поколичеству.csv")
write.csv(top100t, file="top100попроценту.csv")
