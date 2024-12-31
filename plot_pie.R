library('ggplot2')
setwd("C:/Users/34222/Desktop/É³¼¬/")
df <- read.table("./PLOT_SV")
colnames(df) <- c("number","type","group")
df$number <- df$number/10000
df$group <- factor(df$group,levels=c("SV","Gene"))

df <- df[df$type!="Intergenic_region",]

p <- ggplot(df,aes(fill=type, y=number, x=group))
p <- p + geom_bar(position = position_stack(),stat="identity")
p <- p + theme_classic(base_size = 12)
p <- p+ ylab("Number of Sv(10^4)") + xlab("")

#p <- p + geom_text(aes(label = (..count..)/1000, stat="count", vjust = -.5))
pdf("./sv_number_bar.pdf")
p
dev.off()



sum_sv <- sum(df[df$group=="SV","number"])
sum_gene <- sum(df[df$group=="Gene","number"])
df[df$group=="SV","per"] <- df[df$group=="SV","number"]/sum_sv
df[df$group=="Gene","per"] <- df[df$group=="Gene","number"]/sum_gene

#df$number <- df$number*10000
p <- ggplot(df,aes(fill=type, y=per, x=""))
p <- p + geom_bar(position = position_stack(),stat="identity")
p <- p + coord_polar(theta = "y")
p <- p + labs(x = NULL)+ labs(y=NULL)
p <- p + facet_wrap(~group)
p <- p + theme(axis.text = element_blank(),axis.ticks = element_blank(),panel.grid  = element_blank())
p <- p + theme(panel.background = element_blank(),line = element_blank())
p <- p + theme(strip.background = element_rect(color = 'white',fill = 'white'))
p <- p + geom_text(aes(label=scales::percent(per,accuracy = 0.1)),size=1,position=position_stack(vjust = 0.3))

pdf("./sv_number_pie.pdf")
p
dev.off()


