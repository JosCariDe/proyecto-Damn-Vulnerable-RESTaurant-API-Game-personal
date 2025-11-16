# Ejecutar script para ver la vulnerabilidad 
python3 new_parche_proyecto/levels/lvl_4/scripts/exploit_lvl4.py

# Hacer Parche
sudo cp new_parche_proyecto/levels/lvl_4/fix/utils.py app/apis/menu/utils.py 

# Ver el nuevo resultado del script 
python3 new_parche_proyecto/levels/lvl_4/scripts/exploit_lvl4.py

# Quitar Parche (Opcional)
sudo cp new_parche_proyecto/levels/lvl_4/unpatch/utils.py app/apis/menu/utils.py  



