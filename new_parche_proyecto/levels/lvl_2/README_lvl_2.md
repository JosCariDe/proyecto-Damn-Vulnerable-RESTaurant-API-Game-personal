# Ejecutar script para ver la vulnerabilidad 
python3 new_parche_proyecto/levels/lvl_2/script/exploit_level2_idor.py

# Hacer Parche
sudo cp new_parche_proyecto/levels/lvl_2/fix/update_profile_service.py app/apis/auth/services/update_profile_service.py

# Ver el nuevo resultado del script 
python3 new_parche_proyecto/levels/lvl_2/script/exploit_level2_idor.py 

# Quitar Parche (Opcional)
sudo cp new_parche_proyecto/levels/lvl_2/unpatch/update_profile_service.py app/apis/auth/services/update_profile_service.py



