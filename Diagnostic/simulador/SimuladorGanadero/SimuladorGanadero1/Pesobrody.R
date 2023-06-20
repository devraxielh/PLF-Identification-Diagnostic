pesobrody <- function(genero,raza,t) {
  
  if (genero=='M'){
    AC_M  = c(478,0.920,0.00159)
    BAC_M = c(451,0.918,0.00174)
    BC_M = c(547,0.926,0.00119)
    CAC_M = c(504,0.921,0.00144)
    CC_M = c(492,0.923,0.00154)
    if (raza=='AC'){
      b0 = AC_M[1]
      b1 = AC_M[2]
      b2 = AC_M[3]      
    }
    if (raza=='BAC'){
      b0=BAC_M[1]
      b1=BAC_M[2]
      b2=BAC_M[3]
    }
    if (raza=='BC'){
      b0=BC_M[1]
      b1=BC_M[2]
      b2=BC_M[3]
    }
    if (raza=='CAC'){
      b0=CAC_M[1]
      b1=CAC_M[2]
      b2=CAC_M[3]
    }
    if (raza=='CC'){
      b0=CC_M[1]
      b1=CC_M[2]
      b2=CC_M[3]
    }
    r = b0*(1-b1*exp(-b2*t))
  }else{
    AC_H = c(478,0.920,0.00159)
    BAC_H = c(451,0.918,0.00174)
    BC_H  = c(547,0.926,0.00119)
    CAC_H = c(504,0.921,0.00144)
    CC_H = c(492,0.923,0.00154)
    if (raza=='AC'){
      b0=AC_H[1]
      b1=AC_H[2]
      b2=AC_H[3]
    }
    if (raza=='BAC'){
      b0=BAC_H[1]
      b1=BAC_H[2]
      b2=BAC_H[3]
    }
    if (raza=='BC'){
      b0=BC_H[1]
      b1=BC_H[2]
      b2=BC_H[3]
    }
    if (raza=='CAC'){
      b0=CAC_H[1]
      b1=CAC_H[2]
      b2=CAC_H[3]
    }
    if (raza=='CC'){
      b0=CC_H[1]
      b1=CC_H[2]
      b2=CC_H[3]
    }
    r = b0*(1-b1*exp(-b2*t))
  }
  return(round(r))
}