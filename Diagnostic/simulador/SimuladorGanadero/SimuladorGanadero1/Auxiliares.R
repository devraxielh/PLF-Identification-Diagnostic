ganacia_de_peso <- function(temporada,potrero,f,s) {
    if (temporada=='Seca'){
      #print(df_potreros[10,potrero])
      if (str_count(df_potreros[10,potrero])<=7){
        d = as.numeric(str_sub(df_potreros[10,potrero],3,5))
        d = sample(round(d/1.2):d,1)
      }else{
        n1 = as.numeric(str_sub(df_potreros[10,potrero],3,5))
        n2 = as.numeric(str_sub(df_potreros[10,potrero],10,12))
        d = sample(n1:n2,1)
      }
    }
    if (temporada=='Lluvia'){
      #print(df_potreros[9,potrero])
      if (str_count(df_potreros[9,potrero])<=7){
        d = as.numeric(str_sub(df_potreros[9,potrero],3,5))
        d = sample(round(d/1.2):d,1)
      }else{
        n1 = as.numeric(str_sub(df_potreros[9,potrero],3,5))
        n2 = as.numeric(str_sub(df_potreros[9,potrero],10,12))
        d = sample(n1:n2,1)
      }
    }
    if (temporada=='Transicion'){
      #print(df_potreros[9,potrero])
      if (str_count(df_potreros[9,potrero])<=7){
        d = as.numeric(str_sub(df_potreros[9,potrero],3,5))
        d = sample(round(d/1.4):round(d/1.2),1)
      }else{
        n1 = as.numeric(str_sub(df_potreros[9,potrero],3,5))
        n2 = as.numeric(str_sub(df_potreros[9,potrero],10,12))
        d = sample(round(n1/1.3):round(n2/1.3),1)
      }
    }

  if(Nesecidad_nutricional*s>f){
    d = d*(f/(Nesecidad_nutricional*s))
  }
  
  
  
  return(d/1000)
}

#ganacia_de_peso('Seca',4)
#ganacia_de_peso('Lluvia',4)
#ganacia_de_peso('Transicion',4)


perdida_epoca_floracion <- function(Mes,potrero,Perdida_por_floracion) {
  Epoca_floracion = df_potreros[8,potrero]
  perdida = 0
  if (str_count(Epoca_floracion)<=6){
    if (Mes==as.numeric(str_sub(Epoca_floracion,3,4))){
      perdida = Perdida_por_floracion
    }
  }else{
    if (Mes==as.numeric(str_sub(Epoca_floracion,3,4))){
      perdida = Perdida_por_floracion
    }
    if (Mes==as.numeric(str_sub(Epoca_floracion,9,10))){
      perdida = Perdida_por_floracion
    }
  }
  return(perdida)
}

#perdida_epoca_floracion(5,2,Perdida_por_floracion)


Calcular_perdida_por_sequia <- function(temporada,potrero,porcentaje_perdida_por_sequia) {
  tolerancia = df_potreros[7,potrero]
  sequia = 0
  if (temporada=='Seca'){
    if (tolerancia=='Alta'){
      sequia = (0.1*porcentaje_perdida_por_sequia)
    }  
    if (tolerancia=='Media'){
      sequia = (0.3*porcentaje_perdida_por_sequia)
    }  
    if (tolerancia=='Media/Baja'){
      sequia = (0.4*porcentaje_perdida_por_sequia)
    }  
    if (tolerancia=='Baja'){
      sequia = (1*porcentaje_perdida_por_sequia)
    }  
  }
  
  return(sequia)
}

#Calcular_perdida_por_sequia('Seca',4,Perdida_por_sequia)


Calcular_Incremento_por_lluvia <- function(temporada,Incremento_por_lluvia) {
  lluvia = 0
  if(temporada == 'Lluvia'){
    lluvia = Incremento_por_lluvia
  }
  if(temporada == 'Transicion'){
    lluvia = 0.5*Incremento_por_lluvia
  }
  return(lluvia)
}

#Calcular_Incremento_por_lluvia('Transicion',Incremento_por_lluvia)

asig = function(x,v,dias_descanso){
  contar = function(y){
    r = sum(y!=0)
    return(r)
  } 
  #x = asigna[1:3,]
  #v = 3
  s = apply(tail(x,v),2,contar)
  posis = which(s==v)
  dias_descanso[posis] = Descanso
  
  
  
  w = c()
  d = dias_descanso
  for(k in 1:Cantidad_de_Potreros){
    a = which.min(d)
    w = c(w,a)
    d[a] = 100
  }
  co = c(sample(1:Cantidad_lotes,Cantidad_lotes), rep(0,Cantidad_de_Potreros-Cantidad_lotes))
  asi_final = rep(0,Cantidad_de_Potreros)
  
  for(l in 1:Cantidad_de_Potreros){
      if(length(co)>1){
        b = co[1]
        asi_final[w[l]] = b
        co = co[-1]
      }else{
        b = co
        asi_final[w[l]] = b
        break
      }
  }
  resul = list(r1 = asi_final, r2 = dias_descanso)
  return(resul)
}


Tasa_crecimiento_forraje = function(j,tasa){
  contar = function(y){
    r = sum(y==0)
    return(r)
  } 
  s = apply( tail(asigna, min(nrow(asigna),dias_desocupado_forraje)),2,contar)
  if(s[j]>= dias_desocupado_forraje){
    tasa = 0.98*tasa
  }else{
    tasa = tasa
  }
  return(tasa)
  
}


  