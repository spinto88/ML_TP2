oldpar <- par(no.readonly = TRUE)
oldwd <- getwd()
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
#setwd("~/gaming/trabajos/conquerClub/SociosPorConveniencia/Imagenes")


ls <- read.csv("../Datos/learningskill.csv", header =T)

sup <- max(ls[,5][ls[,1]<1000])
inf <- min(ls[,6][ls[,1]<1000])

par(mar=c(5.1,4.1,3.1,4.1))

nn <- ls[,4][ls[,1]<1000]
alpha = 0.05
zz <- qt(1 - alpha/2, nn - 1)
aa <- ls[,2][ls[,1]<1000] - zz * ls[,3][ls[,1]<1000]/sqrt(nn)
bb <- ls[,2][ls[,1]<1000] + zz * ls[,3][ls[,1]<1000]/sqrt(nn)


plot(ls[,1][ls[,1]<1000],ls[,5][ls[,1]<1000], type="l",lwd=2
     ,ylab="Trueskill mean"  ,xlab="Games played", ylim=c(inf,sup))
lines(ls[,1][ls[,1]<1000],ls[,6][ls[,1]<1000],lwd=2)
polygon(c(ls[,1][ls[,1]<1000],rev(ls[,1][ls[,1]<1000])),
        c(aa, rev(bb)), 
        col = "black")
polygon(c(ls[,1][ls[,1]<1000],rev(ls[,1][ls[,1]<1000])),
        c(  ls[,2][ls[,1]<1000] - ls[,3][ls[,1]<1000], rev(ls[,2][ls[,1]<1000] + ls[,3][ls[,1]<1000])), 
        col = rgb(0,0,0,0.2))

polygon(c(ls[,1][ls[,1]<1000],rev(ls[,1][ls[,1]<1000])),
        c(  ls[,2][ls[,1]<1000] - 2*ls[,3][ls[,1]<1000], rev(ls[,2][ls[,1]<1000] + 2*ls[,3][ls[,1]<1000])), 
        col = rgb(0,0,0,0.2))


par(new=TRUE)


plot(ls[,1][ls[,1]<1000],ls[,4][ls[,1]<1000], lty=2, ann=F,axes=F, type="l")
mtext("Population Size", side=4, line=3)
axis(4)



setwd(oldwd)
par(oldpar)