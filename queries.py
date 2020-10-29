# create_f_table = "DROP TABLE IF EXISTS `Frequency`;"\
#                 "CREATE TABLE `Frequency`(`id` INT NOT NULL AUTO_INCREMENT, `timestamp` DATETIME NOT NULL,"\
#                 "`sensor_id` VARCHAR(30) NOT NULL, PRIMARY KEY (`id`));"
#
# create_wd_table = "DROP TABLE IF EXISTS `WeightDistance`;"\
#                 "CREATE TABLE `WeightDistance`(`id` INT NOT NULL AUTO_INCREMENT, `timestamp` DATETIME NOT NULL,"\
#                 "`sensor_id` VARCHAR(30) NOT NULL, `obs_type` INT NOT NULL, `measurement` FLOAT, PRIMARY KEY (`id`));"

add_wd_observation = "INSERT INTO `WeightDistance` (`id`, `timestamp`, `sensor_id`, `obs_type`, `measurement`) VALUES (NULL, %s, %s, %s, %s);"

add_f_observation = "INSERT INTO `Frequency` (`id`, `timestamp`, `sensor_id`) VALUES (NULL, %s, %s);"

get_wd_observation = "SELECT * FROM `WeightDistance` WHERE `sensor_id` = %s AND `timestamp` BETWEEN %s AND %s;"

get_f_observation = "SELECT * FROM `Frequency` WHERE `sensor_id` = %s AND `timestamp` BETWEEN %s AND %s;"

get_wd_count = "SELECT COUNT(*) FROM `WeightDistance` WHERE `sensor_id` = %s AND `timestamp` BETWEEN %s AND %s;"

get_f_count = "SELECT COUNT(*) FROM `Frequency` WHERE `sensor_id` = %s AND `timestamp` BETWEEN %s AND %s;"
