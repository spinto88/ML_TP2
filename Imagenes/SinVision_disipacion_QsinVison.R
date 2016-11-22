oldpar <- par(no.readonly = TRUE)
oldwd <- getwd()
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
#setwd("~/gaming/materias/aprendizaje_automatico/ML_TP2/Imagenes")


ls <- read.csv("../Datos/SinVision_disipacion_QsinVison.csv", header =T)


acum <- matrix(0, nrow=length(ls[,1]),ncol=3)

for (i in seq(2,length(ls[,1]))){
  acum[i,] = acum[i-1,]
  if (ls[i,1] == 0) {acum[i,1] = acum[i,1] + 1}
  if (ls[i,1] == 1) {acum[i,2] = acum[i,2] + 1}
  if (ls[i,1] == 2) {acum[i,3] = acum[i,3] + 1}
}

timesLearn = 5000
halflife = ((timesLearn)*2)/5
disipacion=0.005
b0=-halflife*disipacion
temp = ((1)/(1+exp(-(b0+disipacion*(rev(seq(timesLearn)) ) ) ) ))

plot(temp, type="l", lwd=2,
     xlab="Numero de partidas", ylab="Proporción de partidas ganadas")
legend(length(ls[,1])*5/7,0.6, 
       c("Player 2", "Player 1", "Empates", "Temperatura"),
       lty=c(1,1,1,1),
       lwd=c(2,2,2,2),col=c("red","blue","green","black"), cex=0.7, box.lty=0)
lines(seq(length(ls[,1])),acum[,3]/seq(length(ls[,1])), type="l", lwd=3, col="red")
lines(seq(length(ls[,1])),acum[,2]/seq(length(ls[,1])), lwd=3, col="blue")
lines(seq(length(ls[,1])),acum[,1]/seq(length(ls[,1])), col="green")



par(mar=c(5.1,4.1,3.1,4.1))

par(oldpar)