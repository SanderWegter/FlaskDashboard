DROP TABLE IF EXISTS `groupmembers`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `groupmembers` (
  `uid` int(11) NOT NULL,
  `gid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `groups` (
  `id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user` varchar(128) DEFAULT NULL,
  `pass` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `firstname` varchar(128) DEFAULT NULL,
  `lastname` varchar(128) DEFAULT NULL,
  `lastseen` timestamp NULL DEFAULT NULL,
  `lastip` varchar(40) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `groups` (`id`, `name`) VALUES
(1, 'Admins'),
(2, 'Unassigned');

INSERT INTO `users` (`id`, `user`, `pass`, `email`, `firstname`, `lastname`, `lastseen`, `lastip`, `created`) VALUES
(1, 'admin', '$2b$10$lTsC2XwlSKa0CRdUk5MFBeKKpypjnaaB2hBQaCDaXwoerGWY7Kz3.', 'admin@example.com', 'Admin', '', NOW(), '', NOW());

INSERT INTO `groupmembers` (`uid`, `gid`) VALUES
(1, 1);

ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
