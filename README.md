# Mole 
为海淘用户提供到货通知功能的网站，暂支持网站（sephora.com丝芙兰）

已完成的功能：
- 增删改要爬取的商品
- 注册、登录、个人信息修改管理
- 商品页信息获取、商品是否有货状态监控
- 邮件通知

待完成：
- 网站脚本化部署，当前环境配置很麻烦、或者增加容器

网站页面展示：稍后增加

软件架构如图：   
![image](https://github.com/LvDunn/Mole/blob/master/%E8%BD%AF%E4%BB%B6%E6%9E%B6%E6%9E%84.png)


### 环境配置步骤
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

