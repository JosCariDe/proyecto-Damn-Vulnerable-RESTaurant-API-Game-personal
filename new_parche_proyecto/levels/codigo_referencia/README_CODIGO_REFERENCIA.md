# Ejecutar script para ver la vulnerabilidad 
python3 new_parche_proyecto/levels/codigo_referencia/scripts/exploit_codigo_referencia.py

# Hacer Parche
sudo cp new_parche_proyecto/levels/codigo_referencia/fix/service.py app/apis/referrals/service.py 

# Ver el nuevo resultado del script 
python3 new_parche_proyecto/levels/codigo_referencia/scripts/exploit_codigo_referencia.py 

# Quitar Parche (Opcional)
sudo cp new_parche_proyecto/levels/codigo_referencia/unpatch/service.py app/apis/referrals/service.py 




