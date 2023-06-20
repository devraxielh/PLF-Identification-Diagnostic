#install.packages("readxl")
#install.packages("reticulate")
#install.packages("data.table", dependencies=TRUE)
library(readxl)
library(reticulate)
library(data.table)
library(stringr)
#py_install("pandas")
#py_install("scipy")
#py_install("openpyxl")

ruta = "/Users/raxielh/SimuladorGanadero/"
source(paste(ruta,"Parametros.R",sep=""))
source(paste(ruta,"Pesobrody.R",sep=""))
source(paste(ruta,"Dataframes.R",sep=""))
source(paste(ruta,"Auxiliares.R",sep=""))

n.animales = round(runif(Cantidad_lotes,Cantidad_min_animales,Cantidad_max_animales))

animales_peso_inicial = c()
detalle_animal = c()
for(a in 1:sum(n.animales)){
  genero = sample(c('H','M'),1)
  raza   = sample(c('AC','BAC','BC','CAC','CC'),1)
  edad   = sample(547:912,1)
  animales_peso_inicial = c(animales_peso_inicial,pesobrody(genero=genero,raza=raza,t=edad))
  detalle_animal = c(detalle_animal,c(paste(genero,raza,edad)))
}
pesos = matrix(animales_peso_inicial, nrow = 1)

asigna = matrix(sample( c(1:Cantidad_lotes, rep(0,Cantidad_de_Potreros-Cantidad_lotes)) ), nrow = 1)

ga.peso = round(runif(Cantidad_de_Potreros, 200, 400))
forraje = matrix(round(runif(Cantidad_de_Potreros, Aforo_min,Aforo_max)), nrow = 1)

asi = asigna[asigna!=0]
ga = ga.peso[asigna!=0]


ganacia_de_peso('Seca',4)
ganacia_de_peso('Lluvia',4)
ganacia_de_peso('Transicion',4)
Calcular_perdida_por_sequia('Seca',4,Perdida_por_sequia)
Calcular_Incremento_por_lluvia('Lluvia',Incremento_por_lluvia)


for(t in 1:Dias){
  Temporada = as.character(df_clima[t,11])
  Mes = as.character(df_clima[t,4])
  
  pe = pesos[t,1:n.animales[1]] + ga[1]/1000
  for (i in 2:length(n.animales)) {
    mi = sum(n.animales[1:(i-1)]) + 1
    mf = mi + n.animales[i]-1
    pe = c(pe, pesos[t,mi:mf] + ga[i]/1000)
  }
  pesos = rbind(pesos, pe)
  
  fo = c()
  for (j in 1:ncol(forraje)) {
    if(asigna[t,j]!=0){
      qlot = asigna[t,j]
      n.qlot = n.animales[qlot]
      if(qlot==1){
        mmi = 1 
        mmf = n.animales[qlot]
      }else{
        mmi = sum(n.animales[1:(qlot-1)]) + 1 
        mmf = sum(n.animales[1:(qlot-1)]) + n.animales[qlot]
      }
      fo = c(fo, forraje[t,j] - 0.12*sum(pesos[t, mmi:mmf]) + forraje[t,j]*(Tasa_crecimiento_pasto-Calcular_perdida_por_sequia(Temporada,j,Perdida_por_sequia) + Calcular_Incremento_por_lluvia(Temporada,Incremento_por_lluvia)) )
    }else{
      fo = c(fo, forraje[t,j] + forraje[t,j]*(Tasa_crecimiento_pasto-Calcular_perdida_por_sequia(Temporada,j,Perdida_por_sequia) + Calcular_Incremento_por_lluvia(Temporada,Incremento_por_lluvia)) )
    }
    
  } 
  forraje = rbind( forraje,fo )
  if(!t%%Rotacion){
    asigna = rbind(asigna,sample( c(1:Cantidad_lotes, rep(0,Cantidad_de_Potreros-Cantidad_lotes)) ) )
  }else{ 
    asigna = rbind(asigna,asigna[t,1:Cantidad_de_Potreros])
  }
  
}






