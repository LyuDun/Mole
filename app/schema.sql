CREATE TABLE IF NOT EXISTS `mole_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(18) NOT NULL ,
  `product_url` varchar(512) NOT NULL,
  `product_name` varchar(512),
  `product_img` varchar(512),
  `product_variation` varchar(128),
  `product_status` char(2) DEFAULT '00',
  `create_time` DATETIME NOT NULL,
  `update_time` DATETIME,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into mole_product(id, phone_number, product_url, create_time) values(1, '15550309038', 'https://www.sephora.com/product/matte-velvet-skin-blurring-powder-foundation-P443566?skuId=2210037', '2020-01-11 23:54:33');


CREATE TABLE `mole_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(18) NOT NULL ,
  `username` varchar(24) DEFAULT NULL,
  `password` varchar(24) DEFAULT NULL,
  `wechat_id` varchar(30) DEFAULT NULL,
  `wechat_name` varchar(60) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `wechat_notice` char(1) DEFAULT 'N',
  `email_notice` char(1) DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

insert into mole_user (id, phone_number, username, password) values (1, '15550309038', 'admin', 'admin');
