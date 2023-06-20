funcion_potrero = sprintf("Potreros(%s,%s,%s,%s,%s,%s,%s,'%s')",Cantidad_de_Potreros,Area_potreros_min,Area_potreros_max,Max_x,Max_y,Min_y,Min_x,ruta)
py_run_file(paste(ruta,"/Potreros.py",sep=""))
py_run_string(funcion_potrero)

df_clima = read_excel(paste(ruta,"DataIn/Clima.xlsx",sep=""))
df_pasto =read_excel(paste(ruta,"DataIn/Pasto.xlsx",sep=""))
df_potreros = read_excel(paste(ruta,"DataIn/Potreros.xlsx",sep=""))
df_transpose <- transpose(df_potreros)
rownames(df_transpose) <- colnames(df_potreros)
colnames(df_transpose) <- rownames(df_potreros)
df_potreros = df_transpose