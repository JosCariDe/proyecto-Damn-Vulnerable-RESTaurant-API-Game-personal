# Ejecutar script para ver la vulnerabilidad 
python3 new_parche_proyecto/levels/lvl_3/scripts/exploit_lvl3.py

# Hacer Parche
sudo cp new_parche_proyecto/levels/lvl_3/fix/update_user_role_service.py app/apis/users/services/update_user_role_service.py 

# Ver el nuevo resultado del script 
python3 new_parche_proyecto/levels/lvl_3/scripts/exploit_lvl3.py

# Quitar Parche (Opcional)
sudo cp new_parche_proyecto/levels/lvl_3/unpatch/update_user_role_service.py app/apis/users/services/update_user_role_service.py 




