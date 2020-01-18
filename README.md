# Mole 
为海淘用户提供到货通知、自动下单等功能

1. apt install redis
2. apt install mysql-server
3. pip3 install -r requirement.txt
4. sudo mysql_secure_installation
5. mysql -uroot -p
6. USE mysql;
7. UPDATE user SET plugin='mysql_native_password' WHERE User='root';
8. FLUSH PRIVILEGES;
9. exit;
10. service mysql restart
11. redis-cli
12. config set requirepass pass
13. config set protected-mode no

